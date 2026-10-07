% packages.mzn

int: n;                       % Количество пакетов
set of int: PACKAGES = 1..n;

% depends[i,j] = true, если пакет i требует пакет j
array[PACKAGES, PACKAGES] of bool: depends;

% Пакеты, которые требуется установить
set of PACKAGES: requested;

% Решение: какие пакеты устанавливаются
array[PACKAGES] of var bool: installed;

constraint forall(i in requested)(
    installed[i]
);

constraint forall(i, j in PACKAGES)(
    (installed[i] /\ depends[i,j]) -> installed[j]
);

% Выбираем минимальный набор установленных пакетов
solve minimize sum(i in PACKAGES)(bool2int(installed[i]));

output [
    "Установленные пакеты: ",
    show([i | i in PACKAGES where fix(installed[i])])
];