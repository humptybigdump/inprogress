
% Zeitkntinuierliches System
%sys_cont_zpk = zpk([1], [2 3], 1)
%sys_cont = tf(sys_cont_zpk)
sys_cont = tf([1],[1 5 6])

%Anzeige Pol-Nullstellen
zpk(sys_cont)

% Generieren des zeitdiskreten Ersatzsystems
% Abtastzeit T_A = 0.25, zeor-order-hold
T_A = 0.1
sys_disk = c2d(sys_cont, T_A, 'zoh')
d2c(sys_disk,'zoh')

% Angenommen man würde das z-Modell mit leichter Abweichung (5%) der Parameter
% schätzen
[num,den] = tfdata(sys_disk);
num{1}(2) = num{1}(2) * 1.05
den{1}(2) = den{1}(2) * 1.05


% und daraus wieder das zeitkoninuierliche System ermitteln
sys_disk_abweichung = tf(num,den,T_A)
sys_cont_abweichung = d2c(sys_disk_abweichung,'zoh')

%Anzeige Pol-Nullstellen
zpk(sys_cont_abweichung)


%Ergebnis: zusätzliche Nullstelle, Pole verschoben, einer instabil

