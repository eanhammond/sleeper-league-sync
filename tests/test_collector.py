"""Offline tests. Uses invented names and IDs; makes no real Sleeper requests."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "sync_sleeper.py"
spec = importlib.util.spec_from_file_location("sleeper_collector", SCRIPT)
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)


class CollectorTests(unittest.TestCase):
    def test_sanitizes_names_and_slots(self):
        self.assertEqual(collector.clean_text(" **A\nB** <team>"), "A B team")
        self.assertEqual(collector.filled_starters(["1", "0", "2", ""]), ["1", "2"])

    def test_requires_ids_and_checks_numerics(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "Missing SLEEPER_LEAGUE_ID"):
                collector.required_setting("SLEEPER_LEAGUE_ID")
        with mock.patch.dict(os.environ, {"SLEEPER_LEAGUE_ID": "not a number"}):
            with self.assertRaisesRegex(RuntimeError, "numeric Sleeper ID"):
                collector.required_setting("SLEEPER_LEAGUE_ID")

    def test_collects_private_generic_league_and_excludes_reserve(self):
        league_id, user_id = "111222333", "888999"
        routes = {
            "/state/nfl": {"week": 10, "season": "2026"},
            f"/league/{league_id}": {"name": "Demo League", "season": "2026", "scoring_settings": {"rec": 1}},
            f"/league/{league_id}/users": [
                {"user_id": user_id, "display_name": "Team Owner", "metadata": {"team_name": "Eagles"}},
                {"user_id": "333", "display_name": "Other Owner", "metadata": {"team_name": "Ravens"}},
            ],
            f"/league/{league_id}/rosters": [
                {"roster_id": 1, "owner_id": user_id, "players": ["11", "12", "13", "14"],
                 "starters": ["11", "0"], "reserve": ["13"], "taxi": ["14"],
                 "settings": {"wins": 6, "losses": 3, "fpts": 1150, "fpts_decimal": 31, "waiver_position": 4}},
                {"roster_id": 2, "owner_id": "333", "players": ["21"],
                 "starters": ["21"], "settings": {"wins": 3, "losses": 6}},
            ],
            "/players/nfl": {
                "11": {"full_name": "Starting Player", "position": "QB", "team": "BUF"},
                "12": {"full_name": "Bench Player", "position": "RB", "team": "KC"},
                "13": {"full_name": "Reserve Player", "position": "RB", "team": "SEA"},
                "14": {"full_name": "Taxi Player", "position": "WR", "team": "MIN"},
                "21": {"full_name": "Opponent Player", "position": "WR", "team": "DET"},
            },
        }
        for week in (9, 10, 11):
            routes[f"/league/{league_id}/matchups/{week}"] = [
                {"roster_id": 1, "matchup_id": 9, "points": 20, "starters": ["11", "0"]},
                {"roster_id": 2, "matchup_id": 9, "points": 10, "starters": ["21"]},
            ]
            routes[f"/league/{league_id}/transactions/{week}"] = []

        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            latest = root / "data" / "latest"
            latest.mkdir(parents=True)
            (latest / "matchups_week_1.json").write_text("{}")
            with mock.patch.dict(os.environ, {"SLEEPER_LEAGUE_ID": league_id, "SLEEPER_USER_ID": user_id, "REPORT_TIMEZONE": "America/New_York"}), \
                 mock.patch.object(collector, "ROOT", root), \
                 mock.patch.object(collector, "LATEST", latest), \
                 mock.patch.object(collector, "fetch", side_effect=lambda path, required=True: routes.get(path)):
                collector.collect()
            summary = json.loads((latest / "summary.json").read_text())
            my_team = summary["my_team"]
            self.assertEqual(my_team["team_name"], "Eagles")
            self.assertEqual(len(my_team["starters"]), 1)
            self.assertEqual(my_team["empty_starter_slots"], 1)
            self.assertEqual(my_team["bench"], ["Bench Player (RB / KC)"])
            self.assertEqual(my_team["reserve"], ["Reserve Player (RB / SEA)"])
            self.assertEqual(my_team["taxi"], ["Taxi Player (WR / MIN)"])
            self.assertFalse((latest / "matchups_week_1.json").exists())
            self.assertEqual(summary["weeks_requested"], [9, 10, 11])
            self.assertNotIn("weeks_fetched", summary)
            self.assertEqual(summary["matchups_fetched_weeks"], [9, 10, 11])
            self.assertEqual(summary["transactions_fetched_weeks"], [9, 10, 11])
            self.assertIn("## Eagles", (latest / "overview.md").read_text())
            self.assertEqual(json.loads((latest / "league.json").read_text())["scoring_settings"]["rec"], 1)

    def run_collect(self, routes, league_id, user_id):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        latest = root / "data" / "latest"
        latest.mkdir(parents=True)
        with mock.patch.dict(os.environ, {"SLEEPER_LEAGUE_ID": league_id, "SLEEPER_USER_ID": user_id, "REPORT_TIMEZONE": "America/New_York"}), \
             mock.patch.object(collector, "ROOT", root), \
             mock.patch.object(collector, "LATEST", latest), \
             mock.patch.object(collector, "fetch", side_effect=lambda path, required=True: routes.get(path)):
            collector.collect()
        directory = json.loads((latest / "player_directory.json").read_text())
        return json.loads((latest / "summary.json").read_text()), (latest / "overview.md").read_text(), directory

    def test_playoff_bye_has_no_opponent_and_ties_and_defenses(self):
        league_id, user_id = "444555666", "777"
        routes = {
            "/state/nfl": {"week": 15, "season": "2026"},
            f"/league/{league_id}": {"name": "Playoff League", "season": "2026"},
            f"/league/{league_id}/users": [
                {"user_id": user_id, "display_name": "Bye Team"},
                {"user_id": "2", "display_name": "Eliminated Team"},
                {"user_id": "3", "display_name": "Playoff A"},
                {"user_id": "4", "display_name": "Playoff B"},
            ],
            f"/league/{league_id}/rosters": [
                {"roster_id": 1, "owner_id": user_id, "players": ["11"], "starters": ["11"],
                 "settings": {"wins": 10, "losses": 3, "ties": 1, "fpts": 1500}},
                {"roster_id": 2, "owner_id": "2", "players": [], "settings": {"wins": 2, "losses": 12}},
                {"roster_id": 3, "owner_id": "3", "players": [], "settings": {"wins": 10, "losses": 4, "fpts": 1600}},
                {"roster_id": 4, "owner_id": "4", "players": [], "settings": {"wins": 8, "losses": 6}},
            ],
            "/players/nfl": {
                "11": {"full_name": "Starting Player", "position": "QB", "team": "BUF"},
                "PHI": {"first_name": "Philadelphia", "last_name": "Eagles", "position": "DEF", "team": "PHI"},
            },
        }
        for week in (14, 15, 16):
            routes[f"/league/{league_id}/matchups/{week}"] = [
                {"roster_id": 1, "matchup_id": None, "points": 0, "starters": ["11"]},
                {"roster_id": 2, "matchup_id": None, "points": 0},
                {"roster_id": 3, "matchup_id": 1, "points": 0},
                {"roster_id": 4, "matchup_id": 1, "points": 0},
            ]
        summary, overview, directory = self.run_collect(routes, league_id, user_id)
        self.assertEqual(directory["PHI"]["position"], "DEF")
        bye = summary["my_matchups"]["15"]
        self.assertIsNone(bye["opponent"])
        self.assertFalse(bye["has_matchup"])
        self.assertIn("Week 15: no matchup", overview)
        self.assertNotIn("vs Eliminated Team", overview)
        # 10-3-1 (10.5) ranks ahead of 10-4 (10.0) despite fewer points.
        standings = summary["standings_by_record_then_points"]
        self.assertEqual(standings[0]["team_name"], "Bye Team")
        self.assertIn("**Record:** 10–3–1", overview)
        self.assertIn("Playoff A (Playoff A): 10–4;", overview)



if __name__ == "__main__":
    unittest.main()
