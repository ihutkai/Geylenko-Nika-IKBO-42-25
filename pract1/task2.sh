#!/bin/bash
# Задача 2. 5 наибольших портов из /etc/protocols
grep -v '^#' /etc/protocols | sort -nr | head -n 5 | awk '{print $1, $2}'
