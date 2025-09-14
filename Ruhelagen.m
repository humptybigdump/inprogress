%% Solve - geschlossene Lösung der Ruhelage (Computeralgebra)
% automnomes System (kein Eingang)
syms x1e;
syms x2e;

[x1e,x2e]=solve(x1e*x2e-x1e,3*x1e-2*x2e+x1e^2-2*x2e^2)


%% Fsolve - numerische Berechnung der Ruhelage
% verschiedene Lösungen für verschiedene Startwerte
xe1 = fsolve(@kessel_ruhelagen_fkt,[0.1; 0.8])
xe2 = fsolve(@kessel_ruhelagen_fkt,[0.0; 3.0])
xe3 = fsolve(@kessel_ruhelagen_fkt,[0.5;10.0])


%% Trim - numerische Berechnung der Ruhelage für Simulink-Modell
[X,U,Y,DX]=trim('bihammer_simulink',[],0.5,[],[],1,[])

%% Solve - geschlossene Berechnnung der Ruhelagenmannigfaltigkeit
% system mit Eingang u
syms x1;
syms x2;
syms u;
erg = solve(-x1+x1*u,-x2+u+x2*u);
erg.x1
erg.x2

%% Linearisierung in Zustandsraumdartsellung 

% symbolische Jacobi-Matrizen per Computeralgebra
syms x1 x2 u;
f = [-x1+x1*u; -x2+u+x2*u]; 
x = [x1 x2];
h = [x2^3; x1+x2];
A = jacobian(f,x)
B = jacobian(f,u)
C = jacobian(h,x)
D = jacobian(h,u)

% numerische Jacobi-Matrizen durch Einsetzen von Werten in die symbolischen
% Jacobi-Matrizen
An = subs(A, {x1,x2,u}, {0, 1, 0.5})
Bn = subs(B, {x1,x2,u}, {0, 1, 0.5})
Cn = subs(C, {x1,x2,u}, {0, 1, 0.5})
Dn = subs(D, {x1,x2,u}, {0, 1, 0.5})


%% Linearisierung E/A-Dgl.
syms theta  theta_d theta_dd;
syms p p_d p_dd;
syms F;
syms M m l c gamma g J;

f1 =           (M+m) * p_dd - m*l*cos(theta) * theta_dd + c*p_d+m*l*sin(theta)*theta_d^2 - F
f2 = -m*l*cos(theta) * p_dd + (J+m*l^2)      * theta_dd + gamma*theta_d - m*g*l*sin(theta) - 0

A_2 = [diff(f1,p_dd) diff(f1,theta_dd); diff(f2,p_dd) diff(f2,theta_dd)]
A_1 = [diff(f1,p_d) diff(f1,theta_d); diff(f2,p_d) diff(f2,theta_d)]
A_0 = [diff(f1,p) diff(f1,theta); diff(f2,p) diff(f2,theta)]

% Ruhelage einsetzen:
A_2 = subs(A_2, {p p_d theta  theta_d }, [p 0 0 0]) 
A_1 = subs(A_1, {p p_d theta  theta_d }, [p 0 0 0]) 
A_0 = subs(A_0, {p p_d theta  theta_d }, [p 0 0 0]) 


%% linmod - Linearisierung Simulink-Modell
% Linearisiert System und gibt Zusdtandsraumbeschreibung zurück
[A,B,C,D] = linmod('bihammer_simulink',[0;1],0.5)

% Liefert für das bereits lineare System Zusdtandsraumbeschreibung 
[A,B,C,D] = linmod('signalflussplan1');








