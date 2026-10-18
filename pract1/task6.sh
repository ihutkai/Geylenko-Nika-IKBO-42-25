#!/bin/bash
if [ $# -eq 0 ]; then echo "Использование: $0 <каталог>"; exit 1; fi
dir="$1"
if [ ! -d "$dir" ]; then echo "Ошибка: '$dir' — не каталог"; exit 1; fi
find "$dir" -type f \( -name '*.c' -o -name '*.js' -o -name '*.py' \) | while read -r file; do
    first_line=$(head -n 1 "$file")
    case "$file" in
        *.py)
            if [[ "$first_line" =~ ^[[:space:]]*# ]]; then echo "$file — есть комментарий";
            else echo "$file — нет комментария"; fi ;;
        *.c|*.js)
            if [[ "$first_line" =~ ^[[:space:]]*(//|/\*) ]]; then echo "$file — есть комментарий";
            else echo "$file — нет комментария"; fi ;;
    esac
done
