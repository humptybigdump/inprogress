%% Exercise 1.4

%% Plot the sinc function
x = -10:0.1:10;
y = sinc(x);
plot(x, y, 'r-');

% optionally: add grid
grid on

%% Add functions
hold on
plot(x, 1./(x*pi), 'k:');
plot(x, -1./(x*pi), 'k:');

% set axis limits with a tuple of 4 values:
% lower limit of xaxis, upper limit of xaxis, lower limit of yaxis, upper
% limit of yaxis
axis([-10 10 -1.5 1.5])

%% Add blue cross
plot(0,0,'b+')


%% if you want to create new plots, use the command ...
hold off