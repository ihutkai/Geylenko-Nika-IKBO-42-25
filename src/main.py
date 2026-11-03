"""Этапы 1–2: настройки и получение прямых зависимостей npm."""

import argparse
from dataclasses import asdict
import sys

from config import ConfigError, load_settings
from registry import RegistryError, get_dependencies


def main() -> int:
    """Прочитать JSON и показать все настройки в формате ключ-значение."""
    parser = argparse.ArgumentParser(description="npm, вариант 6 — этапы 1–2")
    parser.add_argument("--config", default="config.json", help="Путь к JSON")
    parser.add_argument("--stage", type=int, choices=(1, 2), default=2,
                        help="Этап демонстрации (по умолчанию 2)")
    args = parser.parse_args()
    try:
        settings = load_settings(args.config)
    except ConfigError as error:
        print(error, file=sys.stderr)
        return 2
    if args.stage == 1:
        for key, value in asdict(settings).items():
            print(f"{key} = {value}")
        return 0
    if settings.test_mode:
        print("Для этапа 2 укажите test_mode: false. Тестовый граф — этап 3.",
              file=sys.stderr)
        return 2
    try:
        version, dependencies = get_dependencies(settings.repository, settings.package)
    except RegistryError as error:
        print(f"Ошибка получения зависимостей: {error}", file=sys.stderr)
        return 1
    print(f"Пакет: {settings.package}@{version}")
    print(f"Прямые зависимости ({len(dependencies)}):")
    for name, spec in dependencies.items():
        print(f"  {name}: {spec}")
    if not dependencies:
        print("  Нет прямых зависимостей.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
