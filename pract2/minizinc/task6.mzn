% Задача 6. Зависимости пакетов

% foo: 1 = версия 1.0.0, 2 = версия 1.1.0
var 1..2: foo;

% target: 1 = версия 1.0.0, 2 = версия 2.0.0
var 1..2: target;

% Установлены ли left и right
var bool: left;
var bool: right;

% shared:
% 0 = не установлен
% 1 = версия 1.0.0
% 2 = версия 2.0.0
var 0..2: shared;

% root требует foo ^1.0.0:
% обе доступные версии foo подходят.

% root требует target ^2.0.0
constraint target == 2;

% foo 1.1.0 требует left и right.
% При foo 1.0.0 они не нужны.
constraint left = (foo == 2);
constraint right = (foo == 2);

% shared устанавливается, если нужны left или right
constraint (shared > 0) = (left \/ right);

% left требует shared >=1.0.0
constraint left -> (shared >= 1);

% right требует shared <2.0.0
% Среди доступных версий подходит только shared 1.0.0
constraint right -> (shared == 1);

% shared 1.0.0 требует target ^1.0.0
constraint (shared == 1) -> (target == 1);

% У foo 1.0.0, shared 2.0.0 и обеих версий target
% дополнительных зависимостей нет.

solve satisfy;

output [
    "foo = ",
    if fix(foo) == 1 then "1.0.0" else "1.1.0" endif,
    "\n",

    "target = ",
    if fix(target) == 1 then "1.0.0" else "2.0.0" endif,
    "\n",

    "left = ",
    if fix(left) then "1.0.0" else "не установлен" endif,
    "\n",

    "right = ",
    if fix(right) then "1.0.0" else "не установлен" endif,
    "\n",

    "shared = ",
    if fix(shared) == 0 then "не установлен"
    elseif fix(shared) == 1 then "1.0.0"
    else "2.0.0"
    endif,
    "\n"
];
