% Demos: perturbation theory of linear systems
% 
% Tested with Octave 7.3 and Matlab r2023b
%
% (c) 2016-2024 dominik.goeddeke@ians.uni-stuttgart.de

A=[1.2969 0.8648; 0.2161 0.1441]
b=[0.8642; 0.1440]
A \ b

bb = [0.86419999; 0.14400001];
A \ bb

As=single(A)
bs=single(b)
As \ bs

norm(A,inf)
norm(inv(A),inf)
cond(A,inf)

eps
eps('single')

