% This is some code to show you how you should structure your main script
% [lastname][NN]_DSPO_Workshop[X].m, with the example starting from line 5.


%% Workshop 1


%% Exercise 1

% Task a)
% Input parameters
x = -10:1:10;                                                              % comment 1
x0 = 15;                                                                   % comment 2
N = 4;
y = function1(x,x0,N);                                                     % here we use the self-written function "function1"


% Task b)
fy=abs(fftshift(fft(y)));                                                  % compute fast fourier transform (fft)


% Task c)
% single plot
figure
plot(y), title('title'), xlabel('x-axis label'), ylabel('y-axis label')

% multiple plots
figure, tiledlayout(1,2)
nexttile, plot(y), title('time-domain')
nexttile; plot(fy), grid on, title('fourier transform')


%% Exercise 2 (And so on...)