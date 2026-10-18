"""Исполнение стартового скрипта с комментариями Python."""

from pathlib import Path

from shell import execute


def run_startup(path: str, write) -> bool:
    """Вывести диалог скрипта; вернуть True при выполнении exit."""
    try:
        lines = Path(path).read_text(encoding="utf-8-sig").splitlines()
    except (OSError, UnicodeError) as error:
        write(f"Ошибка чтения стартового скрипта '{path}': {error}")
        return False
    for number, line in enumerate(lines, start=1):
        command = line.partition("#")[0].strip()
        if not command:
            continue
        write(f"$ {command}")
        result = execute(command)
        if result.text:
            write(result.text)
        if result.text.startswith("Ошибка:"):
            write(f"Ошибка исполнения скрипта '{path}', строка {number}.")
        if result.should_exit:
            return True
    return False
