function V_kanonisch_Model_Error = V_kanonisch_Model_Error( theta )
  
    global y1                          % gemessener Ausgang 1 (arbeitspunktbereinigt)
    global y2                          % gemessener Ausgang 2 (arbeitspunktbereinigt) 
    global K11 T11 K22 T22 K12 K21     % global, damit auch in Simulink identisch 
    
    % Parameter
    K11 = theta(1);             
    T11 = theta(2);
    K22 = theta(3);
    T22 = theta(4);
    K12 = theta(5);
    K21 = theta(6);
   
    
    % Simulation mit Hilfe des Simulink-Modells
    simOut = sim('Parameteridentifikation_Mehrgroessensystem_V_kanonisch','StartTime','0','StopTime','1000','FixedStep','0.1','SimulationMode','normal','AbsTol','1e-5',...
            'SaveOutput','on','OutputSaveName','yout','SaveFormat','Dataset');
    outputs = simOut.get('yout');
    y1_sim = (outputs{1}.Values); 
    y1_sim = y1_sim.Data;
    y2_sim = (outputs{2}.Values); 
    y2_sim = y2_sim.Data;
    
    % Fehlerberechnung 
    e_N1 = y1 - y1_sim;
    e_N2 = y2 - y2_sim;
    V_kanonisch_Model_Error = e_N1'*e_N1 + e_N2'*e_N2;
end