% Aufgabe zu Kalman Zerlegung (https://bilder.buecher.de/zusatz/25/25501/25501847_lese_1.pdf)

A = [0 0 1 0; 0 0 0 1; 0 -0.88 -1.9 0.0056; 0 21.5 3.9 -0.14]
b = [0 0 0.3 -0.62]'
c = [0 1 0 0]
d = 0

sys = ss(A,b,c,d)


% Steuerbarkeit
Q_S = ctrb(A,b);
dim_controllable_subspace = rank(Q_S)
controllability = (length(A) == dim_controllable_subspace)

% Beobachtbarkeit
Q_B = obsv(A,c);
dim_observable_subspace = rank(Q_B)
obervability = (length(A) == dim_observable_subspace)

%% Kalman Zerlegung

[min_sys, U] = minreal(sys)

% Teilsystem min_sys mit allen steuer- und beobachtbaren Moden:
A_SB = min_sys.A;
b_SB = min_sys.B;
c_SB = min_sys.C;
d_SB = min_sys.D;


% Steuerbarkeit nach Kalman Zerlegung fuer Teilsystem (muss steuerbar sein)
Q_S_SB = ctrb(A_SB,b_SB);
dim_controllable_subspace_SB = rank(Q_S_SB)
controllability_min = (length(A_SB) == dim_controllable_subspace_SB)

% Beobachtbarkeit nach Kalman Zerlegung fuer Teilsystem (muss beobachtbar sein)
Q_B_SB = obsv(A_SB,c_SB);
dim_observable_subspace_SB = rank(Q_B_SB)
obervability = (length(A_SB) == dim_observable_subspace_SB)

% Gesamtsystem, das zusaetzlich die nicht steuerbaren bzw, nicht
% beobachtbaren Moden als zusaetzliche Zustandsgroessen enthaelt:

A_T = U*A*U'
b_T = U*b
c_T = c*U'
d_T = d

% Systemmatrix Gesamtsystem A_T enthält jetzt A_SB als linke obere Blockmatrix
A_SB
A_T
b_SB
b_T
c_SB
c_T

% Beobachter könnte hier nur für den beobachtbaren Teil erstellt werden
% System ist allerdings nicht detektierbar, also nicht alle
% nicht-beobachtbaren Moden sind stabil. Hier unbebachtbare Mode mit
% Eigenwert == 0 (Integrator) 