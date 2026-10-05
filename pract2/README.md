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
