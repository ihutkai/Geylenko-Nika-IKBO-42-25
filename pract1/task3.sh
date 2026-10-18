#!/bin/bash
# Задача 3. Программа banner — выводит текст в рамке

if [ $# -eq 0 ]; then
    echo "Использование: $0 \"текст для баннера\""
    exit 1
fi

text="$1"
len=${#text}

# Верхняя граница
printf '+'
printf -- '-%.0s' $(seq 1 $((len + 2)))
printf '+\n'

# Строка с текстом
printf '| %s |\n' "$text"

# Нижняя граница
printf '+'
printf -- '-%.0s' $(seq 1 $((len + 2)))
printf '+\n'
