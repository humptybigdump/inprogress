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
pause
hold on
surf(x1,x2,0*x1+0*x2)
hold off

