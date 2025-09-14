function zero=epsilon1(eps)
global smi;
zero=-smi+2*(1-eps^2)^2/(pi*eps*sqrt(1-eps^2+(4*eps/pi)^2));
end