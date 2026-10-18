"""Параметры командной строки и конфигурация TOML."""

import argparse
from dataclasses import dataclass
from pathlib import Path
import tomllib


@dataclass(frozen=True)
class Settings:
    """Итоговые пути после применения приоритетов."""

    vfs_path: str = "examples/vfs.json"
    startup_script: str | None = None
    config_path: str | None = None


def load_settings(argv=None) -> Settings:
    """Прочитать TOML, затем переопределить значения аргументами запуска."""
    parser = argparse.ArgumentParser(description="Эмулятор оболочки, вариант 6")
    parser.add_argument("--vfs", help="Путь к JSON VFS")
    parser.add_argument("--startup", help="Путь к стартовому скрипту")
    parser.add_argument("--config", help="Путь к конфигурации TOML")
    args = parser.parse_args(argv)
    data = {}
    if args.config is not None:
        try:
            text = Path(args.config).read_text(encoding="utf-8-sig")
            data = tomllib.loads(text)
        except (OSError, UnicodeError, tomllib.TOMLDecodeError) as error:
            parser.error(f"Ошибка чтения конфигурации: {error}")
        for key, value in data.items():
            if key not in ("vfs_path", "startup_script"):
                parser.error(f"Неизвестный параметр конфигурации: {key}")
            if not isinstance(value, str) or not value.strip():
                parser.error(f"Параметр {key} должен быть непустой строкой")
    return Settings(
        vfs_path=args.vfs if args.vfs is not None
        else data.get("vfs_path", "examples/vfs.json"),
        startup_script=args.startup if args.startup is not None
        else data.get("startup_script"),
        config_path=args.config,
    )
