% MATLAB script for plotting the Fourier series of the clocked voltages of
% Exercise 4 Power Electronics
% Written by M.Sc. Simon Frank, May 2021, Elektrotechnisches Institut (ETI)
% Last revision: Simon Frank, 13th June 2023


%% ***General parameters***
f = 20e3;                       % Clocking frequency
T = 1/f;                        % Switching period
t = 0:T/1000:2*T;               % Array for the timescale
UDC1 = 400;                     % Input voltage
UDC2 = 50;                      % Output voltage
k = 7;                          % Number of investigated harmonics


%% ***Calculation of the coefficients***
%% Alternating clocking

ak_alt = zeros(1,k);                                % array for the Fourier coefficients a_k
bk_alt = zeros(1,k);                                % axis symmetry -> all b_k are zero

% positive output voltage
if UDC2 > 0
    d_alt = UDC2/UDC1;  
    for i=1:k
        ak_alt(i) = 2*sin(d_alt*i*pi)/(i*pi);       % calculate the Fourier coefficients with equation 97 in solution, normalized to U_DC1
    end
a0_alt = 2*d_alt;                                   % DC-Offset see equation 100 in solution (normalized to U_DC1)
% negative output voltage
else
    d_alt = -UDC2/UDC1;   
    for i=1:k
        ak_alt(i) = 2*sin(-d_alt*i*pi)/(i*pi);       % calculate the Fourier coefficients with equation 97 in solution, normalized to U_DC1
    end
    a0_alt = -2*d_alt; 
end

%ak = [0.637 0 -0.212 0 0.127 0 -0.091];     % Coefficients from exercise solution for d=0.5
%bk = [0 0 0 0 0 0 0];                       % Coefficients from exercise solution for d=0.5

%% Simultaneous Clocking
d_sim = (UDC2/UDC1+1)*0.5;                          % duty cycle, see equation 64 in task b) of the solution
ak_sim = zeros(size(k));                            % array for the Fourier coefficients a_k
for i=1:k
    ak_sim(i) = 2*sin(d_sim*i*2*pi)/(i*pi);         % calculate the Fourier coefficients a_k with equation 84, normalized to U_DC1
end
bk_sim = zeros(size(k));                        
for i=1:k
    bk_sim(i) = 2*(1-cos(d_sim*i*2*pi))/(i*pi);     % calculate the Fourier coefficients b_k with equation 86, normalized to U_DC1
end
a0_sim = 2*(2*d_sim-1);                             % DC-Offset see equation 87 (normalized to U_DC1)

%ak = [-0.637 0 0.212 0 -0.127 0 0.091];         % Coefficients from exercise solution
%bk = [0.637 0.637 0.212 0 0.127 0.212 0.091];   % Coefficients from exercise solution

%% ***Plotting***
%% Alternating clocking
% Plot the individual sine / cosine functions of the Fourier series
f_alt = zeros(size(ak_alt,2)+size(bk_alt,2),size(t,2));
for i=1:size(ak_alt,2)
     f_alt(i,:)=ak_alt(i)*cos(i*t*2*pi/T);
end
for i=1:size(bk_alt,2)
     f_alt(i+size(ak_alt,2),:)=bk_alt(i)*sin(i*t*2*pi/T);
end
figure
for i=1:size(ak_alt,2)+size(bk_alt,2)
     plot(t,f_alt(i,:),':');
     hold on;
end

% Plot the resulting Fourier series
f_res_alt = zeros(1,size(t,2));
for i=1:size(ak_alt,2)
    f_res_alt = f_alt(i,:)+f_res_alt;
end
for i=size(ak_alt,2)+1:size(ak_alt,2)+size(bk_alt,2)
    f_res_alt = f_alt(i,:)+f_res_alt;
end
f_res_alt = a0_alt/2+f_res_alt;
plot(t,f_res_alt);
hold on;

% Plot the squarewave of the clocked voltage
if UDC2 > 0
    f_square_alt = (square((t+d_alt*T/2)*2*pi/T,d_alt*100)+1)/2;
else
    f_square_alt = (square((t-d_alt*T/2)*2*pi/T,(1-d_alt)*100)-1)/2;
end

plot(t,f_square_alt);

% Plot settings
title('Alternating Clocking')
xlabel('time in s')
ylabel('normalized harmonics')
xlim([0 t(length(t))])
ylim([-1.2 1.2])
hold off;

%% Simultaneous clocking
% Plot the individual sine / cosine functions of the Fourier series
f_sim = zeros(size(ak_sim,2)+size(bk_sim,2),size(t,2));
for i=1:size(ak_sim,2)
     f_sim(i,:)=ak_sim(i)*cos(i*t*2*pi/T);
end
for i=1:size(bk_sim,2)
     f_sim(i+size(ak_sim,2),:)=bk_sim(i)*sin(i*t*2*pi/T);
end
figure
for i=1:size(ak_sim,2)+size(bk_sim,2)
     plot(t,f_sim(i,:),':');
     hold on;
end

% Plot the resulting Fourier series
f_res_sim = zeros(1,size(t,2));
for i=1:size(ak_sim,2)
    f_res_sim = f_sim(i,:)+f_res_sim;
end
for i=size(ak_sim,2)+1:size(ak_sim,2)+size(bk_sim,2)
    f_res_sim = f_sim(i,:)+f_res_sim;
end
f_res_sim = a0_sim/2+f_res_sim;
plot(t,f_res_sim);
hold on;

% Plot the squarewave of the clocked voltage
f_square_sim = square(t*2*pi/T,d_sim*100);
plot(t,f_square_sim);

% Plot settings
title('Simultaneous Clocking')
xlabel('time in s')
ylabel('normalized harmonics')
xlim([0 t(length(t))])
ylim([-1.2 1.2])
