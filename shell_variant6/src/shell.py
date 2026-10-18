"""Команды первого этапа эмулятора оболочки."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CommandResult:
    """Текст результата и признак завершения приложения."""

    text: str = ""
    should_exit: bool = False


def execute(line: str) -> CommandResult:
    """Разделить строку по пробелам и выполнить команду первого этапа."""
    parts = line.split()
    if not parts:
        return CommandResult()
    command, *arguments = parts
    if command == "exit":
        if arguments:
            return CommandResult("Ошибка: exit не принимает аргументы.")
        return CommandResult(should_exit=True)
    if command in ("ls", "cd"):
        if len(arguments) > 1:
            return CommandResult(
                f"Ошибка: {command} принимает не более одного аргумента."
            )
        return CommandResult(f"{command}: аргументы = {arguments!r}")
    return CommandResult(f"Ошибка: неизвестная команда: {command}")
