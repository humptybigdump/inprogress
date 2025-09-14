function PT2_Model_Error = PT2_Model_Error( theta )
  
    global u;               % gemessener Eingang (arbeitspunktbereinigt)
    global y;               % gemessener Ausgang (arbeitspunktbereinigt)
    global t;               % Messzeitpunkte
    
    K = theta(1);           % Verstärkung 
    T1 = theta(2);          % Zeitkonstante 1
    T2 = theta(3);          % Zeitkonstante 2   
    
    x_0 = [0; 0];        % Anfangswerte auf 0 geschätzt
    
    
    % Bestimmung des Zustandsraummodells ausgehend von der DGL und den Parametern
    A = [0 1; -1/T2 -T1/T2];
    B = [0 K/T2]';
    C = [1 0];
    D = 0;
    system = ss(A,B,C,D);
    
    % Simulation und Fehlerberechnung
    y_sim = lsim(system, u, t, x_0); 
    e_N = y - y_sim;
    PT2_Model_Error = e_N'*e_N;
end

