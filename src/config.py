"""Чтение и проверка JSON-настроек анализатора зависимостей."""

import json
from dataclasses import dataclass
from pathlib import Path
import re
from urllib.parse import urlparse


class ConfigError(ValueError):
    """Понятная пользователю ошибка конфигурации."""


@dataclass(frozen=True)
class Settings:
    """Пять настраиваемых параметров варианта 6."""

    package: str
    repository: str
    test_mode: bool
    ascii_tree: bool
    max_depth: int


def validate(data) -> Settings:
    """Проверить типы и допустимые значения всех параметров."""
    expected = {"package", "repository", "test_mode", "ascii_tree", "max_depth"}
    if not isinstance(data, dict):
        raise ConfigError("Корень JSON должен быть объектом")
    missing, extra = expected - data.keys(), data.keys() - expected
    if missing or extra:
        raise ConfigError(
            f"Отсутствуют поля: {sorted(missing)}; лишние поля: {sorted(extra)}"
        )
    for key in ("test_mode", "ascii_tree"):
        if type(data[key]) is not bool:
            raise ConfigError(f"{key}: требуется true или false")
    depth = data["max_depth"]
    if type(depth) is not int or depth < 0:
        raise ConfigError("max_depth: требуется целое число не меньше 0")
    package = data["package"]
    if not isinstance(package, str) or not package:
        raise ConfigError("package: требуется непустое имя пакета")
    pattern = r"[A-Z]+" if data["test_mode"] else (
        r"(?:@[a-z0-9][a-z0-9._-]*/)?[a-z0-9][a-z0-9._-]*"
    )
    if not re.fullmatch(pattern, package):
        raise ConfigError("package: недопустимое имя для выбранного режима")
    repository = data["repository"]
    if not isinstance(repository, str) or not repository.strip():
        raise ConfigError("repository: требуется непустой URL или путь")
    if not data["test_mode"]:
        url = urlparse(repository)
        if url.scheme not in ("http", "https") or not url.netloc:
            raise ConfigError("repository: требуется URL http:// или https://")
    return Settings(**data)


def unique_keys(pairs):
    """Не допускать неоднозначные повторяющиеся настройки."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise ConfigError(f"Повторяющийся параметр: {key}")
        result[key] = value
    return result


def load_settings(path: str) -> Settings:
    """Прочитать настройки; тестовый путь считать от папки JSON-файла."""
    try:
        source = Path(path)
        data = json.loads(
            source.read_text(encoding="utf-8-sig"), object_pairs_hook=unique_keys
        )
        settings = validate(data)
        if settings.test_mode:
            test_path = Path(settings.repository)
            if not test_path.is_absolute():
                test_path = source.resolve().parent / test_path
            if not test_path.is_file():
                raise ConfigError(f"repository: тестовый файл не найден: {test_path}")
        return settings
    except (OSError, UnicodeError, ValueError, RecursionError) as error:
        raise ConfigError(f"Ошибка конфигурации '{path}': {error}") from error
