%% MODELING AND SIMULATION - POOL EXERCISE 5
% Models with distributed parameters - FEM
clearvars; close all; clc

%% b) Parameters and Resolution

% length of the beam, normal force, Young's Modulus
L = 'fill in!';
F = 'fill in!';
E = 'fill in!';

% number of FEs and nodes and length of one element
n_elements = 'fill in!';
n_nodes = 'fill in!';
l_e = 'fill in!';

%% c) Analytic Solution

% declaration and definition of symbolic/continuous functions
syms x u_analytic(x) A(x) sigma_analytic(x)
A(x) = 'fill in!';
sigma_analytic(x) = 'fill in!';

% definition of the ODE, displacment BC and solving with dsolve()
ode = 'fill in!' == 'fill in!';
bc = 'fill in!' == 'fill in!';
u_analytic(x) = 'fill in!';

%% d) Shape Function

% definition of N_e as a symbolic function
syms x_e N_e(x_e)
N_e(x_e) = 'fill in!';

% definition of B_e as numeric values
B_e = 'fill in!';

% material stiffness
C = 'fill in!';

%% e) Node Locations and Cross Section

% location of nodes, as, bs and element centers as vectors
x_nodes = 'fill in!';
x_a = 'fill in!';
x_b = 'fill in!';
x_elementcenters = 'fill in!';

% vector of cross sectional area for every element A_e
A_e = zeros(n_elements, 1);
for element = 1:n_elements
    A_e(element) = 'fill in!';
end

%% f) Local Stiffness Matrices

% definition of a cell array containing all local stiffnes matrices
K_e = cell(n_elements, 1);
for element=1:n_elements
   K_e{element} = 'fill in!';
end

%% g) Gather Matrices and Global Stiffness Matrix

% definition of a cell array containing all gather matrices
L_e = cell(n_elements, 1);
for element=1:n_elements
   L_e{element} = zeros(2, n_nodes);
   'fill in!';
end

% definition of the global stiffness matrix
K = zeros(n_nodes, n_nodes);
for element=1:n_elements
    K = 'fill in!';
end

%% h) Partitioning

% known forces and displacements
f_F = 'fill in!';
u_E = 'fill in!';

% gather matrices for partitioning
L_E = 'fill in!';
L_F = 'fill in!';

% partitioning the global stiffness matrix
K_EE = 'fill in!';
K_FE = 'fill in!';
K_EF = 'fill in!';
K_FF = 'fill in!';

%% i) Solving for Displacements, Forces and Stresses

% unknown forces and displacements
u_F = 'fill in!';
f_E = 'fill in!';

% vectors u and f
u = 'fill in!';
f = 'fill in!';

% calculating the stress in each element
sigma = zeros(n_elements, 1);
for element=1:n_elements
    sigma(element) = 'fill in!';
end

%% Plots
figure;
tiledlayout(2,1);

% displacements
nexttile
hold on
fplot(u_analytic(x), [0 L], 'r');
plot(x_nodes, u, 'b')
title('Displacement u');
xlabel('x in m');
ylabel('u(x) in m');
legend('analytic', 'FEM')

% stresses
nexttile
hold on
fplot(sigma_analytic(x), [0 L], 'r');
scatter(x_elementcenters, sigma, 'b', '.')
title('Stress \sigma');
xlabel('x in m');
ylabel('\sigma(x) in Pa');
legend('analytic', 'FEM')