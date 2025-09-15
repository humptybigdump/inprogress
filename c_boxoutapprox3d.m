% Illustration from the lecture
%
% Oliver Stein: Konvexe Analysis, Karlsruhe Institute of Technology (KIT)
% WiSe 2014/15
%
X1=-3:.05:3;
X2=-2:.05:2;
[x1,x2]=meshgrid(X1,X2);
colormap('summer')
surf(x1,x2,max(x1-2,max(x2-1,max(-x1-2,-x2-1))))
shading('interp')
xlabel('x_1')
ylabel('x_2')
alpha(.5) % needs OpenGL
pause
for t=[.5 .7]
   hold on
   colormap('summer')
   surf(x1,x2,t*log(exp((x1-2)/t)+exp((x2-1)/t)+exp((-x1-2)/t)+exp((-x2-1)/t))-t*log(4))
   shading('interp')
   alpha(.5)
   hold off
   pause
end
hold on
surf(x1,x2,0*x1+0*x2)
hold off
