%% Aufgabe 3e: Entwurf eines P-Reglers

% Gegeben ist die Strecke dx/dt = -x^2 + u und der Regler u = -k * (x - sin(t))

tspan = [0 10];
x0 = 0;
k = 2.225;
[t,x] = ode45(@(t,x) -x^2 - k*(x-sin(t)), tspan, x0);

plot(t,x,'-o')