function [xme]=Lokale_Massenmatrix(rho,l1,A);

xme=zeros(4);
l12=l1*l1;
konst=rho*l1*A/420;
xme(1,1)=156;    xme(1,2)=22*l1;   xme(1,3)=54;      xme(1,4)=-13*l1;
                 xme(2,2)=4*l12;   xme(2,3)=13*l1;   xme(2,4)=-3*l12;
                                   xme(3,3)=156;     xme(3,4)=-22*l1;
                                                     xme(4,4)= 4*l12;

for i=1:4,
    for j=i:4,
        xme(j,i)=xme(i,j);
    end;
end;
xme=konst*xme;
