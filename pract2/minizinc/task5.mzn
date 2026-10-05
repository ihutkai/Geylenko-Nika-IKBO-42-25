% Задача 5. Зависимости пакетов

% Версии пакетов (реальные номера, не индексы)
array[1..6] of float: menu_versions     = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5];
array[1..5] of float: dropdown_versions = [1.8, 2.0, 2.1, 2.2, 2.3];
array[1..2] of float: icons_versions    = [1.0, 2.0];

% Переменные — индексы выбранных версий
var 1..6: menu;
var 1..5: dropdown;
var 1..2: icons;

% Ограничения из графа зависимостей

% menu 1.1.0, 1.2.0, 1.3.0 (индексы 2,3,4) зависят от dropdown 2.x (индексы 2..5)
constraint (menu == 2 \/ menu == 3 \/ menu == 4) -> (dropdown >= 2);

% menu 1.4.0, 1.5.0 (индексы 5,6) зависят от dropdown 1.8.0 (индекс 1)
constraint (menu == 5 \/ menu == 6) -> (dropdown == 1);

% root зависит от любой версии menu и icons — автоматически, дополнительных ограничений не надо
% dropdown зависит от любой версии icons — тоже автоматически

solve satisfy;

output [
  "menu = " ++ show(menu_versions[menu]) ++ "\n",
  "dropdown = " ++ show(dropdown_versions[dropdown]) ++ "\n",
  "icons = " ++ show(icons_versions[icons]) ++ "\n"
];