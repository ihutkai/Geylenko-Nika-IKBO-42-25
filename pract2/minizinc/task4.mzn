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
    "Билет: ", show(d1), show(d2), show(d3),
    show(d4), show(d5), show(d6), "\n",
    "Сумма первых трёх: ", show(sum3), "\n",
    "Сумма последних трёх: ", show(d4 + d5 + d6), "\n"
];