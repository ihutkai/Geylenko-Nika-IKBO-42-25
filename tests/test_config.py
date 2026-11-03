"""Проверки каждого параметра первого этапа."""

from contextlib import redirect_stderr
from io import StringIO
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from config import ConfigError, load_settings, validate


class ConfigTests(unittest.TestCase):
    """Проверить настройки, ошибочные значения и запуск CLI."""

    def setUp(self):
        self.data = json.loads((ROOT / "config.json").read_text())

    def test_valid_configs(self):
        self.assertEqual(load_settings(str(ROOT / "config.json")).package, "express")
        self.assertTrue(load_settings(str(ROOT / "examples/test-config.json")).test_mode)

    def test_every_parameter(self):
        cases = {
            "package": ["", "bad name", None, 5],
            "repository": ["", "local.json", None, 5],
            "test_mode": ["false", 0, None],
            "ascii_tree": ["true", 1, None],
            "max_depth": [-1, 1.5, True, "3"],
        }
        for key, values in cases.items():
            for value in values:
                with self.subTest(key=key, value=value):
                    with self.assertRaises(ConfigError):
                        validate({**self.data, key: value})

    def test_fields(self):
        for data in ([], {}, {**self.data, "extra": 1}):
            with self.subTest(data=data), self.assertRaises(ConfigError):
                validate(data)

    def test_depth_zero_and_scoped_name(self):
        self.assertEqual(validate({**self.data, "max_depth": 0}).max_depth, 0)
        self.assertEqual(validate({**self.data, "package": "@scope/name"}).package,
                         "@scope/name")

    def test_files_and_test_mode_names(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "config.json"
            for text in ('{', '{"package":"A","package":"B"}',
                         json.dumps({**self.data, "test_mode": True}),
                         json.dumps({**self.data, "test_mode": True, "package": "A",
                                     "repository": "missing.json"})):
                path.write_text(text, encoding="utf-8")
                with self.subTest(text=text), self.assertRaises(ConfigError):
                    load_settings(str(path))
            with self.assertRaises(ConfigError):
                load_settings(str(path) + "missing")

    def test_cli(self):
        process = subprocess.run([sys.executable, str(ROOT / "src/main.py"),
                                  "--config", str(ROOT / "config.json")],
                                 capture_output=True, text=True)
        self.assertEqual(process.returncode, 0)
        self.assertIn("package = express", process.stdout)
        self.assertEqual(len(process.stdout.splitlines()), 5)
