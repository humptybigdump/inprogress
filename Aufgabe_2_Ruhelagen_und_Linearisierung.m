%% Aufgabe 2: Ruhelagen und Linearisierung

%% Berechnen der Ruhelagenmenge des Systems in Abhängigkeit von x1e und x2e
syms x1e x2e x3e x4e u1e u2e y1e y2e
e = solve([0 == x3e + (x3e - x2e)*u2e;                              ...
           0 == u2e;                                                ...
           0 == -x1e^2 + u1e + x1e*u2e;                             ...
           0 == -x4e - x2e*x1e^2 + x2e*u1e + (x3e + x1e*x2e)*u2e;   ...
           y1e == x1e + 0.5*x2e^2;                                  ...
           y2e == x2e],                                             ...
        [x3e x4e u1e u2e y1e y2e]);
    
 % solve ..., [x1e, x2e x3e x4e u1e u2e y1e y2e]  liefert nur die Nullruhelage

 
%% Linearisieren des Systems 
syms x1 x2 x3 x4 u1 u2 y1 y2
f = [x3 + (x3 - x2)*u2; u2; -x1*x1 + u1 + x1*u2; -x4 - x2*x1*x1 + x2*u1 + (x3 + x1*x2)*u2];
x = [x1 x2 x3 x4];
u = [u1 u2];
h = [x1 + 0.5*x2^2; x2];

A = jacobian(f,x);
B = jacobian(f,u);
C = jacobian(h,x);
D = jacobian(h,u);

% Ruhelagenmenge einsetzen
A = subs(A, {x1, x2, x3, x4, u1, u2}, {x1e, x2e, e.x3e, e.x4e, e.u1e, e.u2e})
B = subs(B, {x1, x2, x3, x4, u1, u2}, {x1e, x2e, e.x3e, e.x4e, e.u1e, e.u2e})
C = subs(C, {x1, x2, x3, x4, u1, u2}, {x1e, x2e, e.x3e, e.x4e, e.u1e, e.u2e})
D = subs(D, {x1, x2, x3, x4, u1, u2}, {x1e, x2e, e.x3e, e.x4e, e.u1e, e.u2e})

% Einsetzen der konkreten Ruhelage (z.B. Nullruhelage)
x1e_wert = 0;                                        % Hier können die Werte für die Ruhelagen 
x2e_wert = 0;                                        % von x1e und x2e festgelegt werden

An = (subs(A, {x1e, x2e}, {x1e_wert, x2e_wert}))
Bn = (subs(B, {x1e, x2e}, {x1e_wert, x2e_wert}))
Cn = (subs(C, {x1e, x2e}, {x1e_wert, x2e_wert}))
Dn = (subs(D, {x1e, x2e}, {x1e_wert, x2e_wert}))
