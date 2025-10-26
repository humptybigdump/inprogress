function [Mstore,Mmob,A] = localmatrices(xnod,T,S)
% xnod: coordinates of the three nodes (3x2)
% T: transmissivity in the element [m2/s]
% S: storage coefficient in the element [-]
% A: area of the element [m2]

x1=xnod(1,1);
y1=xnod(1,2);
x2=xnod(2,1);
y2=xnod(2,2);
x3=xnod(3,1);
y3=xnod(3,2);

% determinant of Jacobian
detJ = (x2-x1)*(y3-y1)-(y2-y1)*(x3-x1);
% area of teh element
A = detJ*0.5;
% gradient of shape function
dN = 1/detJ*[y2-y3, y3-y1, y1-y2;...
             x3-x2, x1-x3, x2-x1];

Mstore = S*detJ/24*[2, 1, 1;...
                    1, 2, 1;...  
                    1, 1, 2];     % [m2]
Mmob   = detJ*0.5*dN'*T*dN;        % [m2/s]