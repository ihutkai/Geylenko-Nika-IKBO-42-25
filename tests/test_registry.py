"""Проверки HTTP и разбора npm-метаданных без реального интернета."""

from io import BytesIO
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from registry import RegistryError, get_dependencies, parse_metadata


class RegistryTests(unittest.TestCase):
    """Проверить метаданные, пустые зависимости и ошибки сети."""

    def test_dependencies_and_ignored_dev(self):
        version, deps = parse_metadata({"name": "example", "version": "1.0.0",
                                      "dependencies": {"z": "^2", "a": "~1"},
                                      "devDependencies": {"test": "*"}}, "example")
        self.assertEqual(version, "1.0.0")
        self.assertEqual(list(deps), ["a", "z"])
        self.assertNotIn("test", deps)

    def test_no_dependencies(self):
        self.assertEqual(parse_metadata({"name": "x", "version": "1"}, "x")[1], {})

    def test_invalid_metadata(self):
        cases = [[], {}, {"name": "x"},
                 {"name": "x", "version": "1", "dependencies": []},
                 {"name": "x", "version": "1", "dependencies": {"a": 1}}]
        for data in cases:
            with self.subTest(data=data), self.assertRaises(RegistryError):
                parse_metadata(data, "x")

    @patch("registry.urlopen")
    def test_http_and_scoped_package(self, fetch):
        fetch.return_value = BytesIO(json.dumps({"name": "@s/p", "version": "1",
                                                "dependencies": {"a": "*"}}).encode())
        self.assertEqual(get_dependencies("https://registry.npmjs.org/", "@s/p")[1],
                         {"a": "*"})
        self.assertEqual(fetch.call_args.args[0].full_url,
                         "https://registry.npmjs.org/@s%2Fp/latest")

    @patch("registry.urlopen")
    def test_network_errors(self, fetch):
        for error in (HTTPError("url", 404, "missing", {}, None),
                      HTTPError("url", 503, "unavailable", {}, None),
                      URLError("connection failed"), TimeoutError()):
            fetch.side_effect = error
            with self.subTest(error=error), self.assertRaises(RegistryError):
                get_dependencies("https://example.org", "x")

    @patch("registry.urlopen")
    def test_invalid_json(self, fetch):
        fetch.return_value = BytesIO(b"not json")
        with self.assertRaises(RegistryError):
            get_dependencies("https://example.org", "x")
