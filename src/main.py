"""Этап 1: консольный прототип с JSON-конфигурацией."""

import argparse
from dataclasses import asdict
import sys

from config import ConfigError, load_settings


def main() -> int:
    """Прочитать JSON и показать все настройки в формате ключ-значение."""
    parser = argparse.ArgumentParser(description="npm, вариант 6 — этап 1")
    parser.add_argument("--config", default="config.json", help="Путь к JSON")
    args = parser.parse_args()
    try:
        settings = load_settings(args.config)
    except ConfigError as error:
        print(error, file=sys.stderr)
        return 2
    for key, value in asdict(settings).items():
        print(f"{key} = {value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
