epsilon = 1;
sigma = .5;
gamma = sqrt(2);
L = 1;

s = 1./(1-L*sigma*gamma/epsilon)

X1=-3:.01:3;
X2=-2:.01:2;
[x1,x2]=meshgrid(X1,X2);
colormap('summer')
contour(x1,x2,max(x1-2,max(x2-1,max(-x1-2,-x2-1))),[0 0])
hold on
%for s=[1.7 5]
%for t=[sigma/(s-1)/log(4) 1/sqrt(2)/log(4)/s]
   t = (epsilon/gamma-L*sigma)/log(4)
   contour(x1,x2,t*log(exp((x1-2)/t)+exp((x2-1)/t)+exp((-x1-2)/t)+exp((-x2-1)/t))-t*s*log(4),[0 0])
%end
hold off
xlabel('x_1')
ylabel('x_2')