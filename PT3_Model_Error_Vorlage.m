function PT3_Model_Error = PT3_Model_Error( theta )
  
    global u;       % gemessener Eingang (arbeitspunktbereinigt)
    global y;       % gemessener Ausgang (arbeitspunktbereinigt)
    global t;       % Messzeitpunkte
    
    % Erstellen Sie mit den übergebenen Parametern ein Zustandsraummodell und simulieren den Ausgang y.
    % Die Anfangswerte werden hier nicht mitgesch
    system = ss(A,B,C,D);
    y_sim = 
    
    % Berechnen Sie den Fehler zwischen dem gemessenen Ausgang (wurde ganz am Anfang mit den 
    % richtigen Parametern simuliert) und dem hier simulierten Ausgang
    e_N = 
    
    % Rückgabe des quadratischen Fehlers für die Optimierung
    PT3_Model_Error = 
end

