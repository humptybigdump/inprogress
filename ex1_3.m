%% Exercise 1.3

%% Part 1: Create a sequence

seq1 = -3:0.1:5;
% Maybe you want to check the first five values in your array:
seq1(1:5)

%% Part 2: Create an exponential sequence 

format short e %% format the output to be more readable
e = -3:5;
seq2 = 10.^e;
format default %% back to default format

%% Part 3: Compute sum

u = 1:100;
v = 101 - u;
% alternative: v = 100:-1:1;
result_part3 = u*v';

%% Part4: Compute sum over vector elements
result_part4 = sum(u.*v);

% Note: the results for part3 and part4 are identical
u*v' == sum(u.*v)
