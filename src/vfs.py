"""Загрузка виртуальной файловой системы без записи на диск."""

import base64
import binascii
import json
from dataclasses import dataclass
from pathlib import Path


class VFSError(ValueError):
    """Ошибка чтения или структуры JSON VFS."""


@dataclass
class VirtualFileSystem:
    """Каталоги и содержимое файлов, хранящиеся исключительно в памяти."""

    directories: set[str]
    files: dict[str, bytes]


def decode_file(node: dict, path: str) -> bytes:
    """Проверить и декодировать текстовый или двоичный файл."""
    if set(node) != {"type", "encoding", "content"}:
        raise VFSError(f"Неверные поля файла {path}")
    content = node["content"]
    if not isinstance(content, str):
        raise VFSError(f"Содержимое {path} должно быть строкой")
    if node["encoding"] == "utf-8":
        return content.encode("utf-8")
    if node["encoding"] == "base64":
        try:
            return base64.b64decode(content, validate=True)
        except (ValueError, binascii.Error) as error:
            raise VFSError(f"Неверный base64 в {path}") from error
    raise VFSError(f"Неизвестная кодировка файла {path}")


def read_node(node, path: str, vfs: VirtualFileSystem) -> None:
    """Проверить узел дерева и добавить его в модель в памяти."""
    if not isinstance(node, dict):
        raise VFSError(f"Узел {path} должен быть объектом")
    if node.get("type") == "file":
        vfs.files[path] = decode_file(node, path)
        return
    if node.get("type") != "directory":
        raise VFSError(f"Неверный тип узла {path}")
    if set(node) != {"type", "children"}:
        raise VFSError(f"Неверные поля каталога {path}")
    children = node["children"]
    if not isinstance(children, dict):
        raise VFSError(f"children каталога {path} должен быть объектом")
    vfs.directories.add(path)
    for name, child in children.items():
        if not name or name in (".", "..") or "/" in name or "\\" in name:
            raise VFSError(f"Недопустимое имя узла: {name!r}")
        if any(ord(character) < 32 for character in name):
            raise VFSError("Имя узла содержит управляющий символ")
        read_node(child, path.rstrip("/") + "/" + name, vfs)


def unique_object(pairs):
    """Запретить повторяющиеся ключи, чтобы не терять узлы JSON."""
    result = {}
    for key, value in pairs:
        if key in result:
            raise VFSError(f"Повторяющийся ключ JSON: {key}")
        result[key] = value
    return result


def load_vfs(path: str) -> VirtualFileSystem:
    """Прочитать JSON один раз; не распаковывать и не менять источник."""
    try:
        text = Path(path).read_text(encoding="utf-8-sig")
        node = json.loads(text, object_pairs_hook=unique_object)
        if not isinstance(node, dict) or node.get("type") != "directory":
            raise VFSError("Корень VFS должен быть каталогом")
        vfs = VirtualFileSystem(set(), {})
        read_node(node, "/", vfs)
        return vfs
    except (OSError, UnicodeError, ValueError, RecursionError) as error:
        raise VFSError(f"Ошибка загрузки VFS '{path}': {error}") from error
