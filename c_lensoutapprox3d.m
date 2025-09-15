X1=-3:.05:3;
X2=-2:.05:2;
[x1,x2]=meshgrid(X1,X2);
colormap('summer')
surf(x1,x2,max(0.1*(x1.^2+(x2-1.5).^2-25/4),0.05*(x1.^2+(x2+15/4).^2-289/16)))
s=1.5;
shading('interp')
xlabel('x_1')
ylabel('x_2')
alpha(.5) % needs OpenGL
pause
hold on
for t=[.5]
   surf(x1,x2,t*log(exp(0.1*(x1.^2+(x2-1.5).^2-25/4)/t)+exp(0.05*(x1.^2+(x2+15/4).^2-289/16)/t))-s*t*log(2))
   shading('interp')
   alpha(.5)
end
hold off
hold on
surf(x1,x2,0*x1+0*x2)
hold off


