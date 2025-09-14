% clean all variables from workspace
clearvars; 
% close all open figures
close all; 
% clear command line
clc
fprintf('hello, I am Yajian Gao\n')
%test start of Matlab
a=[1,2,3];
A=[1, 2, 3;4, 5, 6; 7,8 ,9; 10,11,12; 13,14,15];
% dot product
(a*transpose(A));
%index from 1 rather than 0, different from numpy
A(1,1);
%second column
A(:,2);
%fourth row
A(4,:);
% By typing v=startvalue:increment:endvalue 
% you can create a vector with regular spaced entries. 
% Create a vector and then the same matrix as in 
% Exercise 1.1 by using reshape.

fprintf('create a vector')
a=1:1:15;
A_re=reshape(a, [5,3]);


%now you could play with matrix A. Delete the fifth row of your
% matrix A, Delete the fifth row of your matrix. 
% This can be done by assigning [] to it.
% Now add a fourth column to your matrix 
% which has the same entries as the second column.
%delete fifth row
A(5,:)=[];
%Add fourth column:
A=[A A(:,2)];

%Matrix with zeros:
   Z = zeros(4,4);
%Matrix with ones:
   O = ones(4,4);
%Matrix with random numbers between 0 and 1:
   R = rand(4,4);
%Matrix with random numbers between a and b:
   a=3
   b=5
   Ri = randi([a,b],4,4);

sin_value=sin(R);

%You can add or multiply a single number or 
% even apply a function like sin to a matrix. 
% The operation will be applied to each element. 
% If you have two matrices, you can multiply them if 
% their dimensions agree. Which rules must be fullfilled 
% for the dimension of each matrix?

A=[1,2;2,1];
B=[5,6;7,8];
%matrix multiplication:
A*B
%Element-wise multiplication:
A.*B

%transpose
A'

%To calculate the inverse of a matrix its determinant 
% cannot be 0. Find out the determinant with det(A). 
% If it is not equal to zero, calculate inv(A). 
% What kind of matrix results if you multiply A 
% with its inverse?
det(A)
inv(A)
A*inv(A)
eye(2,2)


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%Find out how to determine the eigenvectors and -values of 
%a matrix by using the function eig. What are the eigenvectors 
%and -values of your matrix A?

fprintf('Eigenvalues e_val:')
e_val=eig(A);
fprintf('Eigenvalues E_val and eigenvectors E_vec:')
[E_vec,E_val] = eig(A);
E_vec(1,:)*E_vec(2,:)'

[E_vec,E_val]=eig(A'*A);
E_vec(1,:)*E_vec(2,:)'


fprintf('get some rest and an espresso, prepare energy for the next things.')


%%%%% rectangular diagnal matrix and inverse
C=[1,0,0,0;0,2,0,0;0,0,3,0]
C1=[1,0,0;0,1/2,0;0,0,1/3;0,0,0]
C1*C



