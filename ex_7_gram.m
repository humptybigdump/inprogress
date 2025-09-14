(*
Computeralgebra, SS25

gram.m

Berechne Gram-Determinante einer Matrix
*)

(* ***

<<ex_7_gram.m

mat//MatrixForm

Det[mat]

*** *)

dim = 10;
mat = {};
For[i=1,i<=dim,i++,
    row = {};
    For[j=1,j<=dim,j++,
	row = Join[row,{v[i,j]}];
    ];
    mat = Join[mat,{row}];
];


