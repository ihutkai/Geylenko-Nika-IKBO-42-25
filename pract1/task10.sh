#!/bin/bash
# Задача 10. Пустые текстовые файлы в директории

if [ $# -eq 0 ]; then
    echo "Использование: $0 <каталог>"
    exit 1
fi

dir="$1"

if [ ! -d "$dir" ]; then
    echo "Ошибка: '$dir' — не каталог"
    exit 1
fi

files=$(find "$dir" -type f -name '*.txt' -empty)

if [ -z "$files" ]; then
    echo "Пустых текстовых файлов не найдено"
else
    echo "$files"
fi
