z = -2; 
p = [-2, -4]; 
k = 3; 
sys   = zpk(z,p,k)
% Kuerzen von Nullstelle und Polstelle
sys1 = minreal(sys)
z  = -2.001; 
sys   = zpk(z,p,k) % hier wird nicht gekuerzt
sys1 = minreal(sys,0.01) % hier wird wieder gekuerzt