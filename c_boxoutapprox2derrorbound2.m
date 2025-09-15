% Illustration from the lecture
%
% Oliver Stein: Konvexe Analysis, Karlsruhe Institute of Technology (KIT)
% WiSe 2014/15
%
X1=-3:.01:3;
X2=-2:.01:2;
[x1,x2]=meshgrid(X1,X2);
colormap('summer')
contour(x1,x2,max(x1-2,max(x2-1,max(-x1-2,-x2-1))),[0 0])
hold on
for t=[.323 .51]
   contour(x1,x2,t*log(exp((x1-2)/t)+exp((x2-1)/t)+exp((-x1-2)/t)+exp((-x2-1)/t))-t*log(4),[0 0])
end
hold off
xlabel('x_1')
ylabel('x_2')