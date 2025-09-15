X1=-3:.01:3;
X2=-2:.01:2;
[x1,x2]=meshgrid(X1,X2);
colormap('summer')
contour(x1,x2,max(0.1*(x1.^2+(x2-1.5).^2-25/4),0.05*(x1.^2+(x2+15/4).^2-289/16)),[0 0])
s=1.5;
hold on
for t=[.99 .9 .5 .1]
   contour(x1,x2,t*log(exp(0.1*(x1.^2+(x2-1.5).^2-25/4)/t)+exp(0.05*(x1.^2+(x2+15/4).^2-289/16)/t))-s*t*log(2),[0 0])
end
hold off
xlabel('x_1')
ylabel('x_2')
grid

