% Задача 5. Зависимости пакетов

% Доступные версии пакетов
array[1..6] of float: menu_versions =
    [1.0, 1.1, 1.2, 1.3, 1.4, 1.5];

array[1..5] of float: dropdown_versions =
    [1.8, 2.0, 2.1, 2.2, 2.3];

array[1..2] of float: icons_versions =
    [1.0, 2.0];

% Индексы выбранных версий
var 1..6: menu;
var 1..5: dropdown;
var 1..2: icons;

% menu 1.0.0 требует dropdown 1.8.0
constraint (menu == 1) -> (dropdown == 1);

% menu 1.1.0–1.5.0 требуют dropdown 2.x
constraint (menu >= 2) -> (dropdown >= 2);

% dropdown 2.x требует icons 2.0.0
constraint (dropdown >= 2) -> (icons == 2);

% root требует icons 1.0.0
constraint icons == 1;

solve satisfy;

output [
    "menu = " ++ show(menu_versions[menu]) ++ "\n",
    "dropdown = " ++ show(dropdown_versions[dropdown]) ++ "\n",
    "icons = " ++ show(icons_versions[icons]) ++ "\n"
];
