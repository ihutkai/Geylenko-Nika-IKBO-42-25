#!/bin/bash
# Задача 8. Архивирование файлов по расширению

if [ $# -lt 2 ]; then
    echo "Использование: $0 <каталог> <расширение>"
    exit 1
fi

dir="$1"
ext="$2"

if [ ! -d "$dir" ]; then
    echo "Ошибка: '$dir' — не каталог"
    exit 1
fi

# Ищем файлы
files=$(find "$dir" -type f -name "*.$ext")

if [ -z "$files" ]; then
    echo "Файлов с расширением .$ext не найдено"
    exit 0
fi

# Архивируем
echo "$files" | tar -cf "archive_$ext.tar" -T -

echo "Архив archive_$ext.tar создан"
echo "Файлы:"
echo "$files"
