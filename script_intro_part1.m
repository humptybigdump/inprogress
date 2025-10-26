%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                   Introduction to MATLAB (part 1)                       %
%                             November 2020                               %                      
%   Department of Statistics, Econometrics and Empirical Economics        %
%                           Dr. Jantje Sönksen                            %
%                  jantje.soenksen@uni-tuebingen.de                       %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Start each program with clear and clc
clear % clears the workspace
clc % clears the command window


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Slide 5 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% This is a single-line comment
%{ 
This is a multi-line comment.
With multi-line comments, the %{ and %} operators must appear alone on the
lines that immediately precede and follow the block of help text. Do not 
include any other text on these lines. 

Instead of using multi-line comments like this, you can also just start a 
comment with % and continue writing. Matlab will automatically insert 
linebreaks and begin the next line with %, again.
%}

disp('This comment is printed to the output window');

% Let's define a lengthy scalar named 'a'
a=12345678910.1122334455;
% Use the long format (default)
format long
% This is how 'a' would appear in the command window ('format long' is the
% default setting)
disp(a)
% Now, reduce number of decimal places by changing the format
format short
disp(a)
% Assume we are no longer dealing with a scalar, but with a (1x2) vector
% with elements of a very different magnitude.
b=[12345678910.1122334455 0.001];
% This is how 'b' would appear in the command window:
disp(b)
% If the largest entry of a matrix/vector is larger than or equal to 1000,
% the 'short' ('long') format will scale this number, such that it can be
% written with only one digit before the decimal point. The same scaling is
% applied to the entire matrix. When dealing with values that are of a very
% different magnitude, the 'longG' and 'shortG' formats offer a remedy to
% this problem. 
format shortG
disp(b)

% You can also introduce 'a' in the command window like this
disp(['This is a:  ' num2str(a)]); % num2str turns a number into a string



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Slide 6 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Define matrix A (separating columns with commas)
A=[1, 2; 3, 4];
% Define matrix B (separating columns with blanks)
B=[5 6; 7 8];



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Slide 7 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Read out the (2,1) element of A
a21=A(2,1);
% Replace the (2,1) element of A with 7
A(2,1)=7;
% Read out the first column of A
A_1=A(:,1);
% Read out the first row of A
A1=A(1,:);

% Go back to original A
A=[1, 2; 3, 4];



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Slide 8 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Concatenate A and B horizontally
C=[A,B];
% Concatenate A and B vertically
D=[A;B];
% Check dimensions of C
size_C=size(C);
% Check only the number of rows of C
size_C1=size(C,1);
% Check only the number of columns of C
size_C2=size(C,2);
% Check dimensions of D
size_D=size(D);
% Check only the number of rows of D
size_D1=size(D,1);
% Check only the number of columns of D
size_D2=size(D,2);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Slides 9-10 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Add matrices A and B
sum_AB=A+B;
% Subtract matrices A and B
diff_AB=A-B;
% Multiply matrices A and B. This is a proper matrix multiplication,
% meaning that the (1,1)-element of the resulting matrix is
% A(1,1)*B(1,1)+A(1,2)*B(2,1)=1*5+2*7
mult_AB=A*B;
% Multiply matrices A and B pointwise, meaning that the (1,1)-element of
% the resulting matrix is A(1,1).*B(1,1)=1*5
point_mult_AB=A.*B;

% Compute a^2
a_square=a^2;
% What does it mean if you compute A^2?
A_square=A^2;
% The resulting matrix 'A_square' is actually A*A, meaning that its
% (1,1)-element is A(1,1)*A(1,1)+A(1,2)*A(2,1)=1*1+2*3

% If you want to obtain a matrix in which each element of A is taken to the
% power of 2, you need a point-wise operation:
A_pointsquare=A.^2;
% In 'A_pointsquare', the (1,1)-element results as A(1,1)^2=1^2

% Compute a factorial of 3 (3!=1*2*3)
fac=factorial(3);
% Evaluate the exponential function at 3:
exp_a=exp(3);
% Take the natural logarithm of 3:
ln_3=log(3);
% Take the square root of 3:
sq_3=sqrt(3);
% Transpose A:
A_trans=A';

% How to compute the inverse of A?
% There are different ways of computing an inverse. Matlab offers a
% pre-implemented inv-command, but suggests to use "\" or "/" rather than
% "inv". The (back)slash-operators are implemented for solving systems of
% linear equations and use a different computational approach from "inv".
% This approach makes them faster and numerically more precise.
% In the following lines, I compute the inverse of A using the three
% different alternatives and check the time that was required for each of
% the computations. This is done by using the 'tic' and 'toc' commands
% ('tic' starts a stopwatch and 'toc' stops it). t1, t2, and t3 denote the
% time (in seconds) is takes to execute lines 211, 215, and 219, 
% respectively. The times will vary a bit each time you run the program,
% but in general, you will find that "inv" tends to be the slowest option. 
% See https://de.mathworks.com/help/matlab/ref/inv.html?s_tid=srchtitle for
% details.
% 1st approach:
tic;
A_inv1=inv(A);
t1=toc;
% 2nd approach:
tic;
A_inv3=A\eye(size(A,1));
t3=toc;
% 3rd approach:
tic;
A_inv2=eye(size(A,1))/A;
t2=toc;

disp(' ');
% To show you an alternative to the display-command (%d refers to a numeric
% variable which is t1, t2, or t3, respectively)
fprintf('It takes %d seconds to use the inv-command.\n',t1); 
fprintf('It takes %d seconds to use the second approach.\n',t2); 
fprintf('It takes %d seconds to use the third approach.\n',t3); 



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Slide 12 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Compute the sum of the elements in 'A' (column by column)
sum_sn=sum(A);
% Compute the cumulative sum of the elements in 'A' (again, column by
% column)
cumsum_sn=cumsum(A);
% Read out the diagonal elements of 'A'
diag_A=diag(A);
% Write the entries in b on the main diagonal of a (2X2) matrix
mat_b=diag(b,0);
% Compute the rank of 'A'
rank_A=rank(A);
% Compute the determinant of 'A'
det_A=det(A);
% Compute the eigenvalues of 'A'
eig_A=eig(A);



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Slide 13 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Generate a sequence from 0 to 5 with an incremental value of 1 returns a
% rows vector
seq1_row=0:1:5;
% You can create a column vector by
seq1_col=(0:1:5)';
% If the incremental value is 1, it suffices to use
seq2_row=0:5;
disp(' '); % insert an empty line in the output window
disp(['This is the sequence resulting from 0:1:5:  ' num2str(seq1_row)]);
disp(['This is the sequence resulting from 0:5:    ' num2str(seq2_row)]);

% Construct a sequence starting at 0 and going until 5 in steps of 0.25
seq3_row=0:0.25:5;
% Construct a (5x5) matrix of ones (sidenote: when dealing with a square 
% matrix, it actually suffices to use only ones(5))
mat1=ones(5,5);
% Construct a (5x5) matrix of zeros (sidenote: when dealing with a square 
% matrix, it actually suffices to use only zeros(5))
mat2=zeros(5,5);
% Construct an identity matrix of dimension 5
mat3=eye(5);
% Construct a (10x1) vector of draws from a standard normal distribution
vec1=randn(10,1);
% Construct a (10x1) vector of draws from a standard uniform distribution
vec2=rand(10,1);



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Slide 14 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

vec_sn=randn(100,1); % Draw from standard normal distribution
vec_su=rand(100,1); % Draw from standard uniform distribution
% Compute mean of 'vec_sn'
mean_sn=mean(vec_sn);
% Compute standard deviation of 'vec_sn'
std_sn=std(vec_sn);
% Compute median of 'vec_sn'
median_sn=median(vec_sn);
% Compute 50%-quantile of 'vec_sn'
q50_sn=quantile(vec_sn,0.5);
disp(' ');
fprintf('The median (%d) is identical to the 0.5-quantile (%d).\n',median_sn,...
    q50_sn);  % Note that this lengthy command is stretched over two lines
              % using '...'
              
% Now, concatenate 'vec_sn' and 'vec_su' to check their covariance and
% correlation matrices
cov_dat=cov([vec_sn,vec_su]);
corr_dat=corr([vec_sn,vec_su]);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Slide 15 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Use a seed to draw from a N(0,1) distribution, run code several times and
% compare means
seed=1234;
rng(seed); % Set the seed
normal_vec=randn(100,1);
disp(['This is the mean: ' num2str(mean(normal_vec))])
% If you want to return to a time-dependent seed
rng(sum(clock)) % Make the seed time-varying, again
normal_vec=randn(100,1);
disp(['This is the mean: ' num2str(mean(normal_vec))])



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Slide 16-17 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Define g and h and read out their first elements
g=[5;8];
h=[7;8];
g1=g(1); % it suffices to use g(1) instead of g(1,1) because dimensions are 
         % unambigious
h1=h(1);

disp(' ');
disp(['Are ' num2str(g1) ' and ' num2str(h1) ' equal? (0: no, 1: yes):    '...
    num2str(g1==h1)]);
disp(['Are ' num2str(g1) ' and ' num2str(h1) ' equal? (0: no, 1: yes):    '...
    num2str(eq(g1,h1))]);
disp(['Are ' num2str(g1) ' and ' num2str(h1) ' unequal? (0: no, 1: yes):  '...
    num2str(g1~=h1)]);
disp(['Are ' num2str(g1) ' and ' num2str(h1) ' unequal? (0: no, 1: yes):  '...
    num2str(ne(g1,h1))]);
disp(['Is ' num2str(g1) ' larger than ' num2str(h1) '? (0: no, 1: yes):   '...
    num2str(g1>h1)]);
disp(['Is ' num2str(g1) ' larger than ' num2str(h1) '? (0: no, 1: yes):   '...
    num2str(gt(g1,h1))]);
disp(['Is ' num2str(g1) ' smaller than ' num2str(h1) '? (0: no, 1: yes):  '...
    num2str(g1<h1)]);
disp(['Is ' num2str(g1) ' smaller than ' num2str(h1) '? (0: no, 1: yes):  '...
    num2str(lt(g1,h1))]);
disp(['Is ' num2str(g1) ' larger than or equal to ' num2str(h1) '? (0: no, 1: yes):   '...
    num2str(g1>=h1)]);
disp(['Is ' num2str(g1) ' larger than or equal to ' num2str(h1) '? (0: no, 1: yes):   '...
    num2str(ge(g1,h1))]);
disp(['Is ' num2str(g1) ' smaller than or equal to ' num2str(h1) '? (0: no, 1: yes):  '...
    num2str(g1<=h1)]);
disp(['Is ' num2str(g1) ' samller than or equal to ' num2str(h1) '? (0: no, 1: yes):  '...
    num2str(le(g1,h1))]);

% Check whether g<=h and g>=h
check_val=(g<=h) & (g>=h);



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Slide 18 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% For task 1) use M1=A and M2=B;
M1=A;
M2=B;

if size(M1,2)==size(M2,1)
    res_mult=M1*M2;
    disp(' ');
    disp('This is the result of the if-statement');
    disp(res_mult);
else
    disp('Matrices not conformable');
end

% For task 2) use M1=C and M2=A;
M1=C;
M2=A;

if size(M1,2)==size(M2,1)
    res_mult=M1*M2;
    disp(' ');
    disp('This is the result of the if-statement');
    disp(res_mult);
else
    disp('Matrices not conformable');
end



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Slide 19-21 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Task: Create (1x7) vector W using a for-loop
W=ones(1,7); % initialize W
for i=2:1:7 % tell Matlab to start loop at 2, increase in each step by 1,
            % and stop at 7
    W(i)=2*W(i-1); % compute each element of W as twice the previous value
end
disp(' ');
disp(['This is W from first for-loop:   ' num2str(W)]);

% As the loop-variable 'i' is increased by 1, it suffices to use
W=ones(1,7); % initialize W
for i=2:7 % tell Matlab to start loop at 2, increase in each step by 1,
            % and stop at 7
    W(i)=2*W(i-1); % compute each element of W as twice the previous value
end
disp(['This is W from second for-loop:  ' num2str(W)]);

% Task: Create (1x7) vector W using a while-loop
W=ones(1,7); % initialize W
i=2; % Initialize 'i' as 2
while i<=7 % tell Matlab to terminate loop when i exceeds 7
    W(i)=2*W(i-1); % compute each element of W as twice the previous value
    i=i+1; % increase 'i' by 1 after each loop
end
disp(['This is W from while-loop:       ' num2str(W)]);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Task: Write time in matrix using a for-loop
time_mat=zeros(10,6); % Initialize matrix

% For-loop
for i=1:10 % loop starts at 1, increases by 1 (omitted), and stops at 10
    time_mat(i,:)=clock;
end
format longG; % Advisable to use more decimal places as time barely differs

disp(' ');
disp('This is the time matrix computed using a for-loop: ');
disp(time_mat);

% Task: Write time in matrix using a while-loop
time_mat=zeros(10,6); % Initialize matrix

% While-loop
i=1; % start loop at 1
while i<11 % continue loop as long as i is smaller than 11
    time_mat(i,:)=clock;
    i=i+1; % increase 'i' by 1 in each interation
end

disp(' ');
disp('This is the time matrix computed using a while-loop: ');
disp(time_mat);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Task: Draw from standard normal distribution and set all values <0 to 0

sn_draws=randn(500,1);
sn_draws=sort(sn_draws); % sort values
    
new_sn=zeros(size(sn_draws)); % initialize vector of zeros with same 
                              % dimension as vector of standard normal
                              % draws

% For-loop
for i=1:size(sn_draws,1) % loop starts at 1, increases by 1, and stops at 500
    if sn_draws(i)>=0 % the draws from the standard normal are only written 
                      % in 'new_sn' if they are positive
        new_sn(i)=sn_draws(i);
    end
end

disp(' ');
disp(['This is the mean of new_sn (for-loop):   ' num2str(mean(new_sn)) ]);

% While-loop
new_sn=sn_draws;

i=1; % loop starts at 1
while sn_draws(i)<0 % loop stops when sorted entries in sn_draws are no
                    % longer negative
    new_sn(i)=0; % replace negative numbers by 0
    i=i+1; % loop variable is increased by 1
end

disp(['This is the mean of new_sn (while-loop): ' num2str(mean(new_sn)) ]);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Task: Compute sum of entries 

% Construct the sequence
dat_vec=1:100000;

% Compute sum of entries using for-loop
sum1=0; % Initialize sum as 0
tic;
for i=1:size(dat_vec,2) % start loop at 1, increase i by 1 in each step,
                        % and stop at i=100,000
    sum1=sum1+dat_vec(i);
end
time1=toc;
disp(' ');
tech1='for-loop'; % Another way of writing comments flexibly
fprintf('A %s takes %dsec to compute the sum of entries (%d).\n'...
    ,tech1,time1,sum1);


% Compute sum of entries using while-loop
sum2=0; % Initialize sum as 0
tic;
i=1; % start loop at 1
while i<=size(dat_vec,2) % stop loop when i exceeds 100,000
    sum2=sum2+dat_vec(i);
    i=i+1; % increase i by 1
end
time2=toc;
tech2='while-loop';
fprintf('A %s takes %dsec to compute the sum of entries (%d).\n'...
    ,tech2,time2,sum2);

% Compute sum of entries using an inner product
tic;
sum3=dat_vec*ones(size(dat_vec'));
time3=toc;
tech3='inner product';
fprintf('An %s takes %dsec to compute the sum of entries (%d).\n'...
    ,tech3,time3,sum3);

