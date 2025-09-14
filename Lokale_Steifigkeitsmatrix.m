function [xke]=Lokale_Steifigkeitsmatrix(E,l1,Jp);

xke=zeros(4);
l12=l1*l1; l13=l12*l1;
konst=2*E*Jp/l13;
xke(1,1)=6;       xke(1,2)=3*l1;    xke(1,3)=-6;      xke(1,4)= 3*l1;
                  xke(2,2)=2*l12;   xke(2,3)=-3*l1;   xke(2,4)= l12;
                                    xke(3,3)= 6;      xke(3,4)=-3*l1;
                                                      xke(4,4)= 2*l12;

for i=1:4,
   for j=i:4,
       xke(j,i)=xke(i,j);
   end;
end;
xke=konst*xke;
