"""Проверки команд и ошибок первого этапа."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from shell import execute


class ShellTests(unittest.TestCase):
    """Проверить диалог без зависимости от графического интерфейса."""

    def test_empty_input(self):
        self.assertEqual(execute("   ").text, "")

    def test_stubs(self):
        for command in ("ls", "cd"):
            with self.subTest(command=command):
                self.assertEqual(
                    execute(f"  {command}   /home  ").text,
                    f"{command}: аргументы = ['/home']",
                )
                self.assertEqual(
                    execute(command).text, f"{command}: аргументы = []"
                )

    def test_invalid_arguments(self):
        for command in ("ls", "cd", "exit"):
            with self.subTest(command=command):
                result = execute(f"{command} a b")
                self.assertTrue(result.text.startswith("Ошибка:"))
                self.assertFalse(result.should_exit)

    def test_unknown_command(self):
        self.assertIn("неизвестная команда", execute("unknown").text)

    def test_exit(self):
        self.assertTrue(execute("exit").should_exit)
        self.assertFalse(execute("exit argument").should_exit)


if __name__ == "__main__":
    unittest.main()
