% function name
% short description what such a function does

function  y = function1(x,x0,N)
x = upsample(x,N);
y = abs(x).^2 + x0;
end

