function [ZVFdu, ZVFdy] = zvf(Ordnung, T_filter, T_A, Eingangssignal)
% Erstellung eines ZVF in Abhaengigkeit der Ordnung des Modells, der Filterkonstante des ZVF und der Abtastzeit
if Ordnung == 2
    f = [1/T_filter^3, 3/T_filter^2, 3/T_filter^1];
elseif Ordnung == 3
    f = [1/T_filter^4, 4/T_filter^3, 6/T_filter^2, 4/T_filter^1];
elseif Ordnung == 4
    f = [1/T_filter^5, 5/T_filter^4, 10/T_filter^3, 10/T_filter^2, 5/T_filter^1];
end

A = zeros(Ordnung+1,Ordnung+1);
b = zeros(Ordnung+1,1);
C = eye(Ordnung+1);
d = 0;

A(end,:) = -f;
b(end,1) = f(1);

for i = 1:Ordnung
    A(i,i+1) = 1;
end

ZVF = ss(A,b,C,d);

% zeitdiskrete Realisierung des ZVF fuer Eingang
if Eingangssignal == 2
    ZVFdu = c2d(ZVF, T_A, 'foh');   %'foh' wegen Annahme u ist glatt (sinus)
else
    ZVFdu = c2d(ZVF, T_A, 'zoh');   %'zoh' wegen Annahme u ist stueckweise konstant
end

% zeitdiskrete Realisierung des ZVF fuer Ausgang
ZVFdy = c2d(ZVF, T_A, 'foh');       %'foh' wegen Annahme y ist glatt

end

