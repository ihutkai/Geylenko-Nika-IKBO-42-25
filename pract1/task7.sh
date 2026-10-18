#!/bin/bash
# Задача 7. Поиск файлов-дубликатов

if [ $# -eq 0 ]; then
    echo "Использование: $0 <каталог>"
    exit 1
fi

dir="$1"

if [ ! -d "$dir" ]; then
    echo "Ошибка: '$dir' — не каталог"
    exit 1
fi

# Собираем хеши всех файлов
find "$dir" -type f -exec md5sum {} \; | sort > /tmp/hashes.txt

# Находим повторяющиеся хеши
duplicates=$(awk '{print $1}' /tmp/hashes.txt | uniq -d)

if [ -z "$duplicates" ]; then
    echo "Дубликатов не найдено"
    exit 0
fi

# Для каждого повторяющегося хеша выводим файлы
echo "$duplicates" | while read -r hash; do
    echo "Дубликаты (хеш: $hash):"
    grep "^$hash" /tmp/hashes.txt | awk '{$1=""; print "  " $0}'
    echo ""
done

rm -f /tmp/hashes.txt
