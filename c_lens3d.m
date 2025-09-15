X1=-3:.05:3;
X2=-2:.05:2;
[x1,x2]=meshgrid(X1,X2);
colormap('summer')
surf(x1,x2,max(0.1*(x1.^2+(x2-1.5).^2-25/4),0.05*(x1.^2+(x2+15/4).^2-289/16)))
shading('interp')
xlabel('x_1')
ylabel('x_2')
pause
hold on
surf(x1,x2,0*x1+0*x2)
hold off
