#!/bin/bash
# Задача 5. Регистрация пользовательской команды

if [ $# -eq 0 ]; then
    echo "Использование: $0 <файл>"
    exit 1
fi

src="$1"

# Проверяем, что файл существует
if [ ! -f "$src" ]; then
    echo "Ошибка: файл '$src' не найден"
    exit 1
fi

# Даём права на исполнение
chmod +x "$src"

# Копируем в /usr/local/bin (нужен sudo)
sudo cp "$src" /usr/local/bin/

echo "Команда '$src' зарегистрирована в /usr/local/bin"
