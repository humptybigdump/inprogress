function [xk,xm]=Globale_Matrix(kmax,imax,xke,xme);

xk=zeros(imax); xm=zeros(imax);

for k=1:kmax
  k2=2*k;
  ic=[k2-1 k2 k2+1 k2+2];
  xm(ic,ic)=xm(ic,ic)+xme;
  xk(ic,ic)=xk(ic,ic)+xke;
end
