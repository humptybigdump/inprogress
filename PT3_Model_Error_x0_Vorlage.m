function PT3_Model_Error_x0 = PT3_Model_Error_x0( theta )
  
    global u; % gemessener Eingang (arbeitspunktbereinigt)
    global y; % gemessener Ausgang (arbeitspunktbereinigt)
    global t; % Messzeitpunkte
    
    % Erstellen Sie mit den übergebenen Parametern ein Zustandsraummodell und simulieren den Ausgang y.
    % Berücksichtigen Sie hier explizit den Anfangswert bei der Simulation des Ausgangs, welcher im Parametersatz
    % theta ist, welcher der Funktion übergeben wird.
    system = ss(A,B,C,D);
    y_sim = 
    
    % Berechnen Sie den Fehler zwischen dem gemessenen Ausgang (wurde ganz am Anfang mit den 
    % richtigen Parametern simuliert) und dem hier simulierten Ausgang
    e_N = 
    
    % Rückgabe des quadratischen Fehlers für die Optimierung
    PT3_Model_Error_x0 = 
end

