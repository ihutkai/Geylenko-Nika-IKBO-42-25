"""Получение метаданных npm через HTTP без менеджеров пакетов."""

import json
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


class RegistryError(ValueError):
    """Ошибка сети или формата ответа реестра."""


def parse_metadata(data, package: str) -> tuple[str, dict[str, str]]:
    """Проверить ответ версии npm и извлечь поле dependencies."""
    if not isinstance(data, dict) or data.get("name") != package:
        raise RegistryError("Неверный ответ: имя пакета не совпадает")
    version = data.get("version")
    if not isinstance(version, str) or not version:
        raise RegistryError("В ответе отсутствует версия пакета")
    dependencies = data.get("dependencies", {})
    if not isinstance(dependencies, dict):
        raise RegistryError("Поле dependencies должно быть объектом")
    if any(not isinstance(name, str) or not name or
           not isinstance(spec, str) or not spec
           for name, spec in dependencies.items()):
        raise RegistryError("Неверное имя или диапазон версии зависимости")
    return version, dict(sorted(dependencies.items()))


def get_dependencies(repository: str, package: str):
    """Получить прямые рабочие зависимости версии latest HTTP-запросом."""
    url = repository.rstrip("/") + "/" + quote(package, safe="@") + "/latest"
    request = Request(url, headers={"Accept": "application/json"})
    try:
        with urlopen(request, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))
    except HTTPError as error:
        if error.code == 404:
            raise RegistryError(f"Пакет '{package}' не найден (HTTP 404)") from error
        raise RegistryError(f"Ошибка реестра HTTP {error.code}") from error
    except (URLError, OSError, UnicodeError, ValueError) as error:
        raise RegistryError(f"Не удалось прочитать метаданные: {error}") from error
    return parse_metadata(data, package)
