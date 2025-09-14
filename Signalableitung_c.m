omega=2;
Amp = 3;
phi = 0;
t=0:0.1:10;
u=zeros(1,length(t));
A=[0 1;-omega^2 0]; 
B=[0;0]; 
C=[1 0;0 1;-omega^2 0]; 
D=zeros(3,1); 
sys=ss(A,B,C,D);
x_0 = [Amp*sin(phi); Amp*omega*cos(phi)];
lsim(sys,u,t,x_0)