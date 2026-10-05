# Практическое занятие №2. Менеджеры пакетов

**Студент:** Гейленко Ника  
**Группа:** ИКБО-42-25  
**Дата:** 05.10.2026

## Задача 1. Служебная информация о пакете matplotlib

**Условие:** вывести служебную информацию о пакете matplotlib (Python). Разобрать основные элементы содержимого файла со служебной информацией из пакета. Как получить пакет без менеджера пакетов, прямо из репозитория?

**Команда:**

    pip show matplotlib

**Результат:**

![Результат задачи 1](screenshots/task1_pract2.png)

### Разбор основных полей

| Поле | Значение | Что значит |
|------|----------|-----------|
| Name | matplotlib | Имя пакета |
| Version | 3.11.2 | Версия (semver: MAJOR.MINOR.PATCH) |
| Summary | Python plotting package | Краткое описание |
| Home-page | https://matplotlib.org | Сайт проекта |
| Author | John D. Hunter, Michael Droettboom | Авторы |
| License | PSF-подобная | Свободная лицензия |
| Location | /home/nika/venv/lib/python3.14/site-packages | Путь установки |
| Requires | contourpy, cycler, fonttools, kiwisolver, numpy, packaging, pillow, pyparsing, python-dateutil | Зависимости |

### Как получить пакет без менеджера пакетов

**Способ 1 — скачать tarball с PyPI:**

1. Открыть https://pypi.org/project/matplotlib/#files
2. Скачать `.tar.gz` файл нужной версии
3. Распаковать: `tar -xzf matplotlib-*.tar.gz`

**Способ 2 — клонировать с GitHub:**

    git clone https://github.com/matplotlib/matplotlib.git

Оба способа дают исходный код пакета, который можно собрать вручную, без pip.

---

## Задача 2. Служебная информация о пакете express

**Условие:** вывести служебную информацию о пакете express (JavaScript). Разобрать основные элементы содержимого файла со служебной информацией из пакета. Как получить пакет без менеджера пакетов, прямо из репозитория?

**Команда:**

    npm view express name version description license homepage repository.url

**Результат:**

![Результат задачи 2](screenshots/task2_pract2.png)

### Разбор основных полей (package.json)

| Поле | Значение | Что значит |
|------|----------|-----------|
| name | express | Имя пакета |
| version | 5.2.1 | Версия (semver: MAJOR.MINOR.PATCH) |
| description | Fast, unopinionated, minimalist web framework | Краткое описание |
| license | MIT | Свободная лицензия |
| homepage | https://expressjs.com/ | Сайт проекта |
| repository.url | git+https://github.com/expressjs/express.git | Репозиторий на GitHub |

### Как получить пакет без менеджера пакетов

**Способ 1 — скачать tarball из npm-реестра:**

    npm view express dist.tarball
    # выведет URL, например:
    # https://registry.npmjs.org/express/-/express-5.2.1.tgz

    curl -O https://registry.npmjs.org/express/-/express-5.2.1.tgz
    tar -xzf express-5.2.1.tgz

**Способ 2 — клонировать с GitHub:**

    git clone https://github.com/expressjs/express.git

Оба способа дают исходный код пакета, который можно использовать без npm.

---

## Задача 3. Граф зависимостей matplotlib и express

**Условие:** сформировать graphviz-код и получить изображения зависимостей matplotlib и express.

### Граф зависимостей matplotlib

**DOT-код:**

    digraph matplotlib_deps {
        rankdir=LR;
        node [shape=box, style=filled, fillcolor=lightblue];
        matplotlib -> contourpy;
        matplotlib -> cycler;
        matplotlib -> fonttools;
        matplotlib -> kiwisolver;
        matplotlib -> numpy;
        matplotlib -> packaging;
        matplotlib -> pillow;
        matplotlib -> pyparsing;
        matplotlib -> python_dateutil [label="python-dateutil"];
    }

**Генерация:**

    dot -Tpng matplotlib_deps.dot -o matplotlib_deps.png

**Изображение:**

![matplotlib dependencies](screenshots/matplotlib_deps.png)

### Граф зависимостей express

**DOT-код:**

    digraph express_deps {
        rankdir=LR;
        node [shape=box, style=filled, fillcolor=lightgreen];
        express -> qs;
        express -> depd;
        ...
    }

**Генерация:**

    dot -Tpng express_deps.dot -o express_deps.png

**Изображение:**

![express dependencies](screenshots/express_deps.png)

---

## Задача 4. Счастливые билеты (MiniZinc)

**Условие:** решить на MiniZinc задачу о счастливых билетах. Добавить ограничение на то, что все цифры билета должны быть различными (all_different). Найти минимальное решение для суммы 3 цифр.

**Код (lucky_ticket.mzn):**

    include "alldifferent.mzn";

    var 0..9: d1;
    var 0..9: d2;
    var 0..9: d3;
    var 0..9: d4;
    var 0..9: d5;
    var 0..9: d6;

    constraint d1 + d2 + d3 = d4 + d5 + d6;
    constraint alldifferent([d1, d2, d3, d4, d5, d6]);

    var 0..27: sum3 = d1 + d2 + d3;
    solve minimize sum3;

    output [
        "Билет: ", show(d1), show(d2), show(d3), show(d4), show(d5), show(d6), "\n",
        "Сумма первых трёх: ", show(sum3), "\n",
        "Сумма последних трёх: ", show(d4 + d5 + d6), "\n"
    ];

**Команда запуска:**

    minizinc lucky_ticket.mzn

**Результат:**

![Результат задачи 4](screenshots/task4_pract2.png)

Билет `620431`, сумма первых трёх = сумма последних трёх = 8. Все цифры разные.


---

## Задача 5. Зависимости пакетов (menu/dropdown/icons)

**Условие:** решить на MiniZinc задачу о зависимостях пакетов для рисунка.

**Код (task5.mzn):**

    % Задача 5. Зависимости пакетов

    array[1..6] of float: menu_versions     = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5];
    array[1..5] of float: dropdown_versions = [1.8, 2.0, 2.1, 2.2, 2.3];
    array[1..2] of float: icons_versions    = [1.0, 2.0];

    var 1..6: menu;
    var 1..5: dropdown;
    var 1..2: icons;

    constraint (menu == 2 \/ menu == 3 \/ menu == 4) -> (dropdown >= 2);
    constraint (menu == 5 \/ menu == 6) -> (dropdown == 1);

    solve satisfy;

    output [
      "menu = " ++ show(menu_versions[menu]) ++ "\n",
      "dropdown = " ++ show(dropdown_versions[dropdown]) ++ "\n",
      "icons = " ++ show(icons_versions[icons]) ++ "\n"
    ];

**Результат:**

![Результат задачи 5](screenshots/task5_pract2.png)

### Пояснение

Зависимости из графа:
- `menu 1.1.0, 1.2.0, 1.3.0` → зависят от `dropdown 2.x`
- `menu 1.4.0, 1.5.0` → зависят от `dropdown 1.8.0`
- `root` → зависит от любой версии `menu` и `icons`
- `dropdown` → зависит от любой версии `icons`

MiniZinc нашёл одно из решений: `menu 1.0`, `dropdown 1.8`, `icons 1.0`.
