%% Exercise 1.5

x = -10:0.1:10;
y = sinc(x);
plot(x, y, 'r-');

% optionally: add grid
grid on

hold on
plot(x, 1./(x*pi), 'k:');
plot(x, -1./(x*pi), 'k:');

% set axis limits with a tuple of 4 values:
% lower limit of xaxis, upper limit of xaxis, lower limit of yaxis, upper
% limit of yaxis
axis([-10 10 -1.5 1.5])

% add blue cross
plot(0,0,'b+')