%set number of iterations
I=200;
% set number of copies
K = 10000;
d = [];
%initialize lookup table
m(1,:) = [1 0];
m(2,:) = [0 1];
m(3,:) = [-1 0];
m(4,:) = [0 -1];
for i=1:K
	%initialize position for i-th copy
        p(1,:)=[0 0];
        for j=1:I-1
		k=ceil(4*rand);
                p(j+1,:) = p(j,:)+m(k,:);
        end
        d = [d p];
end
rho = sqrt(d(:,1:2:end).^2+d(:,2:2:end).^2);
rhom = mean(rho,2);
rhost = std(rho,1,2);
for i=1:I
% rhom(i) = mean(bootstrp(200,@mean,rho(i,:)));
 rhod(i) = std(bootstrp(200,@mean,rho(i,:)));
end
figure(1)
errorbar(log(rhom')./log([1:I]),rhod./rhom'./log([1:I]));
for i=1:I/2
 prob0(i) = length(find(rho(2*i-1,:)==0))/K;
 dprob0(i) = std(bootstrp(200,@count0,rho(2*i-1,:)))/K;
end
figure(2)
errorbar([1:2:I],log(prob0),dprob0./prob0,'.')
figure(3)
errorbar([1:2:I],-2*log(prob0)./log([1:2:I]),-2*dprob0./prob0./log([1:2:I]),'.')
% One can improve the statistics by considering also the returns to 1, 2 etc.
% The time series will however become shorter!
% Cross-correlations.
for i=1:I
 for j=1:I
	 Xrho(i,j) = mean((rho(i,:)-rhom(i)).*(rho(j,:)-rhom(j)))/(rhost(i)*rhost(j));
	 dXrho(i,j) = std((rho(i,:)-rhom(i)).*(rho(j,:)-rhom(j)))/(rhost(i)*rhost(j))/sqrt(K-1); 
 end
end
for n=3:100
  l = [0:I-n]';
  cut = length(Xrho(n:end,n));
  if I-n>50
     l=[0:50]';
	 cut = n+50;
  end
	 s = @(x)sum((Xrho(n:cut,n)-abs(x(3))*exp(-l/abs(x(1)))-(1-abs(x(3)))*exp(-l/(abs(x(1))+abs(x(2))))).^2./dXrho(n:cut,n).^2)/(cut);
	 x=[10,10,0.5];
  [x,fval] = fminsearch(s,x);
  [x,fval] = fminsearch(s,x);
  [x,fval] = fminsearch(s,x);
	 tau(n) = x(1);
	 tau1(n) = x(2);
	 A(n) = x(3);
  Xi(n) = fval;
end

	 for i=1:I
           for j=1:K
             p=[0 0];	     
     	     for k=1:i
             	 int=ceil(4*rand);
                 p = p + m(int,:);
             end
	   rtmp(j) = sqrt(p(1)^2 + p(2)^2);
           end
	   rnew(i) = mean(rtmp);
	   rnewst(i) = std(rtmp)/sqrt(K-1);
         end
