"""Проверки приоритетов и ошибок конфигурации."""

from contextlib import redirect_stderr
from io import StringIO
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from config import load_settings
from startup import run_startup


class ConfigurationTests(unittest.TestCase):
    """Проверить конфигурацию и выполнение скриптов без GUI."""

    def test_defaults(self):
        self.assertEqual(load_settings([]).vfs_path, "examples/vfs.json")

    def test_file_and_cli_priority(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "config.toml"
            path.write_text(
                'vfs_path = "file.json"\nstartup_script = "file.txt"',
                encoding="utf-8",
            )
            settings = load_settings(["--config", str(path)])
            self.assertEqual(settings.vfs_path, "file.json")
            settings = load_settings([
                "--config", str(path), "--vfs", "cli.json",
                "--startup", "cli.txt",
            ])
            self.assertEqual(settings.vfs_path, "cli.json")
            self.assertEqual(settings.startup_script, "cli.txt")

    def test_bad_configurations(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "config.toml"
            for content in ('vfs_path = [', 'vfs_path = 3', 'other = 1'):
                path.write_text(content, encoding="utf-8")
                with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
                    load_settings(["--config", str(path)])
            path.unlink()
            with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
                load_settings(["--config", str(path)])

    def test_script_comments_errors_and_exit(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "startup.txt"
            path.write_text(
                '# comment\n\nls /home # comment\nunknown\nexit\nls',
                encoding="utf-8",
            )
            output = []
            self.assertTrue(run_startup(str(path), output.append))
            self.assertEqual(output[0], "$ ls /home")
            self.assertTrue(any("строка 4" in line for line in output))
            self.assertEqual(output[-1], "$ exit")
            output.clear()
            self.assertFalse(run_startup(str(path) + "missing", output.append))
            self.assertIn("Ошибка чтения", output[0])
