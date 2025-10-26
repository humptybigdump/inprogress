%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                   Introduction to MATLAB (part 2)                       %
%                             November 2020                               %                      
%   Department of Statistics, Econometrics and Empirical Economics        %
%                           Dr. Jantje Sönksen                            %
%                  jantje.soenksen@uni-tuebingen.de                       %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Start each program with clear and clc
clear % clears the workspace
clc % clears the command window
close all % to close all windows that include graphs

% Re-initialize A and B
A=[1 2; 3 4];
B=[5 6; 7 8];


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Slide 24 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Call function for X=A and Y=B. M1 denotes the result from the matrix
% multiplictaion and M2 refers to point-wise multiplictaion
[M1,M2]=func_matmult(A,B);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Slide 25 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Write a function that computes m*A+n*B. As the function has a different
% workspace from this script, A and B must be handed as input arguments too
w_res=func_weightmult(1,1,A,B);

% Write a function that generates a sequence. Call it for a sequence that
% starts at 0, increases in steps of 3 and does not get larger than 9
seq=func_seq( 0,3,9 );


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Slide 26 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Save A in different formats
save('A.mat','A');
save('A.txt','A','-ascii');
csvwrite('A.csv','A');
%xlswrite('A.xls','A');
% Read A back into program
clear('A');
load('A.mat');


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Slide 27-29 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% This is a very basic plot
seed = 1234;
rng(seed); % Set the seed
figure;
x=(1901:2000)';
y=randn(100,1);
handle=plot(x,y,'--r'); % I choose a dashed red line
xlabel('year'); % Define the label of the x-axis
ylabel('value'); % Define the label of the y-axis
title('some important series'); % Choose a title
saveas(handle,'firstplot.eps','epsc'); % Save plot as .eps


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Slide 30 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Use the subplot command
figure;
subplot(2,1,1) % Use a subplot command to align plots vertically (1st plot)
x=(1901:2000)';
y=randn(100,1);
handle=plot(x,y,'--r'); % Choose a dashed red line
xlabel('year');
ylabel('value');
title('some important series');
subplot(2,1,2) % Use a subplot command to align plots vertically (2nd plot)
x=(1901:2000)';
y=randn(100,1);
handle=plot(x,y,'b'); % Choose a blue line
xlabel('year');
ylabel('value');
title('some important series');


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Slide 31 %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% plot density of standard normal distribution and kernel density in one
% graph
% Compute kernel density estimates
[f,xi]=ksdensity(y);
xn=normpdf(xi,0,1);
figure;
handle=plot(xi',f','b',xi',xn','r');
set(handle(1),'Linewidth',3); % Change linewidth of first density
set(handle(2),'Linewidth',2); % Change linewidth of second density
leg_handle=legend('kernel','N(0,1) pdf','Location','Northwest'); % Position
                              % legend
set(leg_handle,'FontSize',12); % Set fontsize in legend
xlabel('x','Fontsize',14); % Specify label of x-axis
ylabel('(kernel) density','Fontsize',14); % Specify label of y-axis
axis([-5 5, 0 0.5]); % Choose starting and end points of axes
set(gca,'FontSize',12); % Choose fontsize of axes