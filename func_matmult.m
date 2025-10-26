function [ mult1,mult2 ] = func_matmult( X,Y )
% This function performsthe matrix multiplications. "mult1" results from a
% standard matrix multiplication, whilst "mult2" refers to an element-wise
% multiplication of X and Y

mult1=X*Y;
mult2=X.*Y;
end

