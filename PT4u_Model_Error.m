function PT4_Model_Error = PT4_Model_Error( theta )
  
    global u;               % gemessener Eingang (arbeitspunktbereinigt)
    global y;               % gemessener Ausgang (arbeitspunktbereinigt)
    global t;               % Messzeitpunkte
    
    K = theta(1);           % Verstärkung 
    b1 = theta(2);          % Verstärkung b1
    T1 = theta(3);          % Zeitkonstante 1
    T2 = theta(4);          % Zeitkonstante 2   
    T3 = theta(5);          % Zeitkonstante 3
    T4 = theta(6);          % Zeitkonstante 4
    
    x_0 = [0; 0; 0; 0];        % Anfangswerte auf 0 geschätzt
    
    
    % Bestimmung des Zustandsraummodells ausgehend von der DGL und den Parametern
    A = [0 1 0 0; 0 0 1 0; 0 0 0 1; -1/T4 -T1/T4 -T2/T4 -T3/T4];
    B = [0 0 0 1]';
    C = [K/T4 b1*K/T4 0 0];
    D = 0;
    system = ss(A,B,C,D);
    
    % Simulation und Fehlerberechnung
    y_sim = lsim(system, u, t, x_0); 
    e_N = y - y_sim;
    PT4_Model_Error = e_N'*e_N;
end

