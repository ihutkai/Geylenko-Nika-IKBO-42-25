"""Ограниченный по глубине обход графа DFS через стек, без рекурсии."""

from dataclasses import dataclass, field
import json
from pathlib import Path
import re

from config import unique_keys
from registry import get_dependencies


class GraphError(ValueError):
    """Ошибка структуры тестового графа или выбранного пакета."""


@dataclass
class GraphResult:
    """Построенный граф, минимальные глубины, порядок DFS и найденные циклы."""

    depths: dict[str, int]
    edges: dict[str, list[str]] = field(default_factory=dict)
    order: list[str] = field(default_factory=list)
    cycles: list[list[str]] = field(default_factory=list)


def load_test_graph(path: Path) -> dict[str, list[str]]:
    """Прочитать граф: имя пакета из A–Z → список имён зависимостей."""
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"),
                          object_pairs_hook=unique_keys)
    except (OSError, UnicodeError, ValueError, RecursionError) as error:
        raise GraphError(f"Ошибка тестового репозитория: {error}") from error
    if not isinstance(data, dict):
        raise GraphError("Тестовый репозиторий должен быть объектом JSON")
    for name, dependencies in data.items():
        if not re.fullmatch(r"[A-Z]+", name):
            raise GraphError(f"Недопустимое имя тестового пакета: {name!r}")
        if not isinstance(dependencies, list):
            raise GraphError(f"Зависимости {name} должны быть списком")
        if any(not isinstance(dep, str) or dep not in data
               for dep in dependencies):
            raise GraphError(f"Зависимости {name} ссылаются на неизвестный пакет")
        if len(set(dependencies)) != len(dependencies):
            raise GraphError(f"Повтор зависимости в пакете {name}")
    return {name: sorted(deps) for name, deps in data.items()}


def find_cycles(edges: dict[str, list[str]]) -> list[list[str]]:
    """Найти циклы по рёбрам к активному пути, используя итеративный DFS."""
    colors, cycles = {}, []
    for start in sorted(edges):
        if colors.get(start):
            continue
        colors[start] = 1
        path = [start]
        positions = {start: 0}
        stack = [(start, iter(edges.get(start, [])))]
        while stack:
            node, children = stack[-1]
            child = next(children, None)
            if child is None:
                stack.pop()
                path.pop()
                positions.pop(node)
                colors[node] = 2
            elif colors.get(child) == 1:
                cycles.append(path[positions[child]:] + [child])
            elif not colors.get(child):
                colors[child] = 1
                positions[child] = len(path)
                path.append(child)
                stack.append((child, iter(edges.get(child, []))))
    return cycles


def build_graph(root: str, max_depth: int, neighbors) -> GraphResult:
    """Обойти DFS; повторно расширять узел только при более коротком пути."""
    result = GraphResult(depths={root: 0})
    stack = [(root, 0)]
    expanded = {}
    while stack:
        node, depth = stack.pop()
        if depth > result.depths[node]:
            continue
        if node not in result.edges:
            result.edges[node] = []
            result.order.append(node)
        if depth >= max_depth or expanded.get(node, max_depth + 1) <= depth:
            continue
        children = sorted(neighbors(node))
        result.edges[node] = children
        expanded[node] = depth
        for child in reversed(children):
            child_depth = depth + 1
            if child_depth < result.depths.get(child, max_depth + 1):
                result.depths[child] = child_depth
                stack.append((child, child_depth))
    result.cycles = find_cycles(result.edges)
    return result


def analyze(settings, config_path: str) -> GraphResult:
    """Выбрать тестовый файл или npm; кэшировать ответы внутри одного запуска."""
    if settings.test_mode:
        path = Path(settings.repository)
        if not path.is_absolute():
            path = Path(config_path).resolve().parent / path
        graph = load_test_graph(path)
        if settings.package not in graph:
            raise GraphError(f"Пакет {settings.package} отсутствует в тестовом графе")
        return build_graph(settings.package, settings.max_depth, graph.__getitem__)
    cache = {}

    def neighbors(package):
        if package not in cache:
            _, dependencies = get_dependencies(settings.repository, package)
            cache[package] = list(dependencies)
        return cache[package]

    return build_graph(settings.package, settings.max_depth, neighbors)


def print_graph(result: GraphResult, max_depth: int) -> None:
    """Показать список связей, глубины и циклы; без визуализации этапа 5."""
    print(f"Граф зависимостей: максимальная глубина = {max_depth}")
    print("Порядок DFS: " + ", ".join(result.order))
    print(f"Пакетов: {len(result.depths)}")
    for name in sorted(result.depths):
        depth = result.depths[name]
        children = result.edges[name]
        if depth == max_depth:
            detail = "достигнут предел глубины, зависимости не запрашивались"
        else:
            detail = ", ".join(children) if children else "нет зависимостей"
        print(f"  {name} (глубина {depth}) -> {detail}")
    print("Циклы в исследованной части графа:")
    if not result.cycles:
        print("  не обнаружены")
    for cycle in result.cycles:
        print("  " + " -> ".join(cycle))
