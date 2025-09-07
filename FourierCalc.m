% Script for the Fourier calculation of the output current waveform
% Basic frequency modulation assumed
% written by: Simon Frank, July 2022

I_amp = 41.11;                                                  % Maximum value output current
beta = 2*pi/3;                                                  % Angle of the basic frequency modulation

% Functions for the a_k coefficients 
f1a = @(t,k) (I_amp/(beta/2)*t).*cos(k*t);
f2a = @(t,k) I_amp.*cos(k*t);
f3a = @(t,k) (I_amp-I_amp/(beta/2)*(t-beta)).*cos(k*t);
f4a = @(t,k) -I_amp.*cos(k*t);
f5a = @(t,k) (I_amp/(beta/2)*(t-5/2*beta)-I_amp).*cos(k*t);

% Functions for the b_k coefficients
f1b = @(t,k) (I_amp/(beta/2)*t).*sin(k*t);
f2b = @(t,k) I_amp.*sin(k*t);
f3b = @(t,k) (I_amp-I_amp/(beta/2)*(t-beta)).*sin(k*t);
f4b = @(t,k) -I_amp.*sin(k*t);
f5b = @(t,k) (I_amp/(beta/2)*(t-5/2*beta)-I_amp).*sin(k*t);

% Plotting for debugging
% fplot(@(x) f1a(x,1),[0 beta/2]);
% hold on;
% fplot(@(x) f2a(x,1),[beta/2 beta]);
% hold on;
% fplot(@(x) f3a(x,1),[beta 2*beta]);
% hold on;
% fplot(@(x) f4a(x,1),[2*beta 5/2*beta]);
% hold on;
% fplot(@(x) f5a(x,1),[5/2*beta 2*pi]);

% Calculate a_k coeffients 
for k=1:17
    a_k(k) = 1/pi*(integral(@(t) f1a(t,k),0,beta/2)...
        + integral(@(t) f2a(t,k),beta/2,beta)...
        + integral(@(t) f3a(t,k),beta,2*beta)...
        + integral(@(t) f4a(t,k),2*beta,5/2*beta)...
        + integral(@(t) f5a(t,k),5/2*beta,2*pi));
end

% Calculate b_k coeffients 
for k=1:17
    b_k(k) = 1/pi*(integral(@(t) f1b(t,k),0,beta/2)...
        + integral(@(t) f2b(t,k),beta/2,beta)...
        + integral(@(t) f3b(t,k),beta,2*beta)...
        + integral(@(t) f4b(t,k),2*beta,5/2*beta)...
        + integral(@(t) f5b(t,k),5/2*beta,2*pi));
end

% Calculate c_k coeffients 
c_k = sqrt(a_k.^2 + b_k.^2);