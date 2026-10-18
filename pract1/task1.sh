#!/bin/bash
# Задача 1. Список имён пользователей из /etc/passwd
grep -o '^[^:]*' /etc/passwd | sort
