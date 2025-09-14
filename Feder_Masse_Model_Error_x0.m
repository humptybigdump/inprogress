function Feder_Masse_Model_Error_x0 = Feder_Masse_Model_Error_x0( theta )
  
    global u; % gemessener Eingang (arbeitspunktbereinigt)
    global y; % gemessener Ausgang (arbeitspunktbereinigt)
    global t; % Messzeitpunkte
    
    k = theta(1);
    m = theta(2);
    c = theta(3);
    x_0 = [theta(4); theta(5)];
    
    system = ss([0 1; -k/m -c/m], [0; 1/m], [1 0], 0);
    y_sim = lsim(system, u, t, x_0); 
    e_N = y - y_sim;
    Feder_Masse_Model_Error_x0 = e_N'*e_N;
end

