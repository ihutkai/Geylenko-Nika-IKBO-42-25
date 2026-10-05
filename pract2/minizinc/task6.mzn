% Задача 6. Зависимости пакетов

array[1..2] of float: foo_versions    = [1.0, 1.1];
array[1..2] of float: target_versions = [1.0, 2.0];

var 1..2: foo;
var 1..2: target;

% root требует foo ^1.0.0 (1.x.x)
constraint foo >= 1;

% root требует target ^2.0.0 (2.x.x)
constraint target == 2;

% Если foo = 1.1.0 (индекс 2), то нужны left и right → shared 1.0.0 → target 1.0.0
% Но target уже 2.0.0 → конфликт. Значит, foo не может быть 2.
constraint foo == 1;

solve satisfy;

output [
  "foo = " ++ show(foo_versions[foo]) ++ "\n",
  "target = " ++ show(target_versions[target]) ++ "\n",
  "shared = не устанавливается (конфликт)\n"
];