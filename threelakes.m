% Sulfate in a series of three lakes
clear variables
close all
clc
% volumes
V = [1000;500;1700]; % [m3]
% discharge
Q = 500; % [m3/s]
% rate coefficients of first-order decay
lambda = [0.1;2;0.01];% [1/d]
% concentration in the inflow
cin=1000; % [mg/L = g/m3]

% 1a: Residence times
tau = V/Q;
for ii=1:3
    fprintf('residence time of lake %i: %g d\n',[ii,tau(ii)])
end

% Part 1: Prior to remediation
disp('Part 1: Prior to Remediation')
% 1b: ODE system
% dcdt = K*c + s
K = [-lambda(1)-1/tau(1),                   0,                    0; ...
               +1/tau(2), -lambda(2)-1/tau(2),                    0; ...
                       0,            1/tau(3), -lambda(3)-1/tau(3)];
s = [cin/tau(1); 0; 0];

c0 = zeros(3,1);

[T,C]=ode15s(@lakeode,[0 10*max(tau)],c0,[],lambda,tau,cin);
plot(T,C);
xlabel('t [d]')
ylabel('c [mg/L]')

% 1c: steady-state concentrations
c_ss = -K\s;
for ii=1:3
    fprintf('steady-state conc. in lake %i: %g mg/L\n',[ii,c_ss(ii)])
end
hold on
plot(max(T)*ones(3,1),c_ss,'kx')
hold off
legend('lake 1','lake 2','lake 3','Location','best')

% Part 2: With remediation in the inflow
disp('Part 2: With Remediation in the Inflow')
% 2a: new ODE system
% compute first-order decay coeff in the inflow
% exp(-kin*1day) = 0.925
kin=-log(0.925); % [1/d]

[Tnew,Cnew]=ode15s(@lakeode_new,[0 10*max(tau)],c_ss,[],lambda,tau,cin,kin);

% 2b: plot the results
figure(2)
cin_new=cin*exp(-kin*Tnew);
plot(Tnew,[cin_new,Cnew]);
xlabel('t [d]')
ylabel('c [mg/L]')

% 2c: time to reach target concentration
c_std = 250;
t_rem = zeros(3,1);

for ii=1:3
    t_rem(ii)=interp1(Cnew(:,ii),Tnew,c_std);
    fprintf('time to reach 250 mg/L in lake %i: %gd\n',[ii,t_rem(ii)])
end
hold on
plot(t_rem,c_std*ones(3,1),'xk')
hold off
legend('inflow','lake 1','lake 2','lake 3','Location','best')

% ODE function of the original problem
function dcdt=lakeode(t,c,lambda,tau,cin)
dcdt=zeros(size(c));

dcdt(1) = -lambda(1)*c(1) + (cin -c(1))/tau(1);
dcdt(2) = -lambda(2)*c(2) + (c(1)-c(2))/tau(2);
dcdt(3) = -lambda(3)*c(3) + (c(2)-c(3))/tau(3);
end

% ODE function of the problem with remediation in the inflow
function dcdt=lakeode_new(t,c,lambda,tau,cin,kin)
dcdt=zeros(size(c));
cin_new=cin*exp(-kin*t);

dcdt(1) = -lambda(1)*c(1) + (cin_new -c(1))/tau(1);
dcdt(2) = -lambda(2)*c(2) + (c(1)-c(2))/tau(2);
dcdt(3) = -lambda(3)*c(3) + (c(2)-c(3))/tau(3);

end