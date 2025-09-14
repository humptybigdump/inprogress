
clear all
close all
%% Numerische Bestimmung der Mindest-Transitionszeit, damit maximale Stellgröße ud_max = 90 

% Probiere Transitionszeiten zwischen 0.01 und 0.2 durch, 
% bis ud_max zum ersten mal unter 90 liegt
for T=0.01:0.001:0.2
    t = [0:0.001:T]';
    ud = 10+15*t.^2/T^2-10*t.^3/T^3+ 30*t/T^2-30*t.^2/T^3;
    ud_max = max(ud);
    if ud_max <= 90
        break;
    end
end

T