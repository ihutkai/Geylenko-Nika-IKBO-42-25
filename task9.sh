#!/bin/bash
# Задача 9. Замена 4 пробелов на табуляцию

if [ $# -lt 2 ]; then
    echo "Использование: $0 <входной_файл> <выходной_файл>"
    exit 1
fi

input="$1"
output="$2"

if [ ! -f "$input" ]; then
    echo "Ошибка: файл '$input' не найден"
    exit 1
fi

sed 's/    /\t/g' "$input" > "$output"

echo "Файл '$output' создан"
