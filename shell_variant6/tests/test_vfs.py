"""Проверки загрузки дерева, двоичных данных и неизменности источника."""

import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from vfs import VFSError, load_vfs

EXAMPLES = Path(__file__).resolve().parents[1] / "examples"


class VFSTests(unittest.TestCase):
    """Проверить реальные примеры VFS и повреждённые данные."""

    def test_minimal(self):
        vfs = load_vfs(str(EXAMPLES / "minimal.json"))
        self.assertEqual(vfs.directories, {"/"})
        self.assertEqual(vfs.files, {})

    def test_binary_and_text(self):
        vfs = load_vfs(str(EXAMPLES / "vfs.json"))
        self.assertEqual(vfs.files["/data.bin"], bytes([0, 1, 2, 3, 255]))
        self.assertIn("Привет", vfs.files["/hello.txt"].decode("utf-8"))

    def test_deep(self):
        vfs = load_vfs(str(EXAMPLES / "deep.json"))
        self.assertIn("/home/user/docs", vfs.directories)
        self.assertIn("/home/user/docs/notes.txt", vfs.files)

    def test_bad_examples(self):
        for name in ("missing.json", "bad-json.json", "bad-vfs.json",
                     "bad-base64.json"):
            with self.subTest(name=name), self.assertRaises(VFSError):
                load_vfs(str(EXAMPLES / name))

    def test_source_is_not_modified(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "vfs.json"
            original = (EXAMPLES / "vfs.json").read_bytes()
            path.write_bytes(original)
            vfs = load_vfs(str(path))
            vfs.files["/hello.txt"] = b"changed only in memory"
            self.assertEqual(path.read_bytes(), original)
            self.assertEqual(list(Path(folder).iterdir()), [path])

    def test_invalid_nodes(self):
        invalid = [
            {"type": "file", "encoding": "utf-8", "content": "root"},
            {"type": "directory", "children": {"..": {}}},
            {"type": "directory", "children": {"a/b": {}}},
            {"type": "directory", "children": {"file": {
                "type": "file", "encoding": "unknown", "content": "x"}}},
        ]
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "bad.json"
            for node in invalid:
                path.write_text(json.dumps(node), encoding="utf-8")
                with self.subTest(node=node), self.assertRaises(VFSError):
                    load_vfs(str(path))

    def test_duplicate_keys(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "duplicate.json"
            path.write_text('{"type":"directory","children":{},'
                            '"children":{}}', encoding="utf-8")
            with self.assertRaises(VFSError):
                load_vfs(str(path))
