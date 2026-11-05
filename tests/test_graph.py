"""Проверки итеративного DFS, глубины, циклов и тестовых репозиториев."""

from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from config import load_settings
from graph import GraphError, analyze, build_graph, load_test_graph


class GraphTests(unittest.TestCase):
    """Проверить графы без необходимости доступа в интернет."""

    def test_diamond_and_dfs_order(self):
        graph = {"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}
        result = build_graph("A", 3, graph.__getitem__)
        self.assertEqual(result.order, ["A", "B", "D", "C"])
        self.assertEqual(result.depths, {"A": 0, "B": 1, "C": 1, "D": 2})
        self.assertEqual(result.edges["C"], ["D"])
        self.assertEqual(result.cycles, [])

    def test_depth_limit(self):
        graph = {"A": ["B"], "B": ["C"], "C": []}
        calls = []
        def neighbors(node):
            calls.append(node)
            return graph[node]
        result = build_graph("A", 1, neighbors)
        self.assertEqual(result.depths, {"A": 0, "B": 1})
        self.assertEqual(calls, ["A"])
        calls.clear()
        self.assertEqual(build_graph("A", 0, neighbors).depths, {"A": 0})
        self.assertEqual(calls, [])

    def test_cycle_and_self_loop(self):
        graph = {"A": ["B"], "B": ["C"], "C": ["A"]}
        self.assertEqual(build_graph("A", 5, graph.__getitem__).cycles,
                         [["A", "B", "C", "A"]])
        self.assertEqual(build_graph("A", 2, lambda name: ["A"]).cycles,
                         [["A", "A"]])

    def test_shorter_path_reexpands_node(self):
        graph = {"A": ["B", "Z"], "B": ["C"], "C": ["X"],
                 "X": ["Y"], "Z": ["X"], "Y": []}
        result = build_graph("A", 3, graph.__getitem__)
        self.assertEqual(result.depths["X"], 2)
        self.assertEqual(result.depths["Y"], 3)
        self.assertEqual(result.edges["X"], ["Y"])

    def test_long_chain_without_recursion(self):
        def neighbors(node):
            return [str(int(node) + 1)] if int(node) < 1500 else []
        self.assertEqual(len(build_graph("0", 1501, neighbors).depths), 1501)

    def test_invalid_test_graphs(self):
        cases = ['[]', '{', '{"a":[]}', '{"A":["B"]}',
                 '{"A":"B"}', '{"A":["A","A"]}', '{"A":[],"A":[]}']
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "graph.json"
            for text in cases:
                path.write_text(text, encoding="utf-8")
                with self.subTest(text=text), self.assertRaises(GraphError):
                    load_test_graph(path)

    def test_root_not_found(self):
        settings = load_settings(str(ROOT / "examples/test-config.json"))
        from dataclasses import replace
        with self.assertRaises(GraphError):
            analyze(replace(settings, package="Z"), str(ROOT / "examples/test-config.json"))

    @patch("graph.get_dependencies")
    def test_real_provider_cache(self, fetch):
        from dataclasses import replace
        settings = replace(load_settings(str(ROOT / "config.json")),
                           package="a", max_depth=4)
        graph = {"a": {"b": "*", "z": "*"}, "b": {"c": "*"},
                 "c": {"x": "*"}, "z": {"x": "*"}, "x": {"y": "*"}, "y": {}}
        fetch.side_effect = lambda repo, name: ("1", graph[name])
        result = analyze(settings, "unused.json")
        self.assertEqual(result.depths["y"], 3)
        self.assertEqual(sum(call.args[1] == "x" for call in fetch.call_args_list), 1)

    def test_cli_stage3(self):
        process = subprocess.run([sys.executable, str(ROOT / "src/main.py"),
                                  "--stage", "3", "--config",
                                  str(ROOT / "examples/cycle-config.json")],
                                 capture_output=True)
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertIn(b"A -> B -> C -> A", process.stdout)
