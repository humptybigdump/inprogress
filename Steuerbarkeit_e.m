A=[0,-4;-2,-2];
B=[1;1];
C=[0,1];
D=0;
sys=ss(A,B,C,D)

% Kalman-Kriterium fuer Steuerbarkeit:
rank(ctrb(sys))
% Kalman-Kriterium fuer Beobachtbarkeit:
rank(obsv(sys))

% PBH (Hautus) fuer Steuerbarkeit:
rank([2*eye(2)-A, B])
rank([-4*eye(2)-A, B])

% PBH (Hautus) fuer Beobachtbarkeit (Dualitaet nutzen):
rank([2*eye(2)-A', C'])
rank([-4*eye(2)-A, C'])

% Gram'sches Kriterium Steuerbarkeit:
rank(gram(sys,'c'))

% Gram'sches Kriterium Beobachtbarkeit:
rank(gram(sys,'o'))