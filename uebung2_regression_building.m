% ALLE 10
eval(gaitfindobj_callback('CE_Alle_ZR'));

% Typ
% {'Artificial Neural Networks'}
set_textauswahl_listbox(gaitfindobj('CE_Regression_Typ'),{'Artificial Neural Networks'});eval(gaitfindobj_callback('CE_Regression_Typ'));

% Ausgangsgröße Regression
% {'Energy'}
set_textauswahl_listbox(gaitfindobj('CE_Regression_Output'),{'Energy'});eval(gaitfindobj_callback('CE_Regression_Output'));

% Verfahren
% {'Artificial Neural Networks'}
set_textauswahl_listbox(gaitfindobj('CE_Spezielle_Verfahren'),{'Artificial Neural Networks'});eval(gaitfindobj_callback('CE_Spezielle_Verfahren'));

% Neuronales Netz: Typ
% {'Feedforwardnet (MLP)'}
set_textauswahl_listbox(gaitfindobj('CE_NN_Typ'),{'Feedforwardnet (MLP)'});eval(gaitfindobj_callback('CE_NN_Typ'));

%% Regression,  Data-Mining,  Entwurf und Anwendung 
eval(gaitfindobj_callback('MI_Regression_EnAn'));

% Verfahren
% {'Artificial Neural Networks'}
set_textauswahl_listbox(gaitfindobj('CE_Spezielle_Verfahren'),{'Polynom'});eval(gaitfindobj_callback('CE_Spezielle_Verfahren'));

%% Regression,  Data-Mining,  Entwurf und Anwendung 
eval(gaitfindobj_callback('MI_Regression_EnAn'));

