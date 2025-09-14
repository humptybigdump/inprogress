function dy = Ritz_ausMAPLE_Beidseitig(t,y,E,I0,mu0,l,N)

switch N

    case 0
dy(1) = y(2);
t1 = l ^ 2;
t2 = t1 ^ 2;
t7 = pi ^ 2;
t8 = t7 ^ 2;
dy(2) = -0.1e1 / t2 * E * I0 * y(1) * t8 / mu0;

    case 1
dy(1) = y(2);
t2 = pi ^ 2;
t3 = t2 ^ 2;
t4 = E * I0 * t3;
t6 = l ^ 2;
t7 = t6 ^ 2;
t8 = 0.1e1 / t7;
t10 = 0.1e1 / mu0;
dy(2) = -t4 * y(1) * t8 * t10;
dy(3) = y(4);
dy(4) = -0.16e2 * t4 * y(3) * t8 * t10;

    case 2
dy(1) = y(2);
t2 = pi ^ 2;
t3 = t2 ^ 2;
t4 = E * I0 * t3;
t6 = l ^ 2;
t7 = t6 ^ 2;
t8 = 0.1e1 / t7;
t10 = 0.1e1 / mu0;
dy(2) = -t4 * y(1) * t8 * t10;
dy(3) = y(4);
dy(4) = -0.16e2 * t4 * y(3) * t8 * t10;
dy(5) = y(6);
dy(6) = -0.81e2 * t4 * y(5) * t8 * t10;


%    case 3
    
%    case 4

      
        end

dy = dy';
        
        
        
        
        
        
        
        
        