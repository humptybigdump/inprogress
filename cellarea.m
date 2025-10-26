function [area,porarea]=cellarea(net,ntube,nsec,poros)

% % old version by Olaf
% area=zeros(ntube,nsec);
% for ii=1:ntube
%     for jj=1:nsec
%         A = abs(polyarea(...
%             [net.x(ii,jj) net.x(ii,jj+1) net.x(ii+1,jj+1) net.x(ii+1,jj) net.x(ii,jj)],...
%             [net.y(ii,jj) net.y(ii,jj+1) net.y(ii+1,jj+1) net.y(ii+1,jj) net.y(ii,jj)]));
%         area(ii,jj)=A;
%     end
% end
% area=reshape(area,ntube*nsec,1);
% porarea=poros*area;

% new version by Wolfgang - faster by factor 2 orders of magnitude ;)
nel = ntube*nsec;
area = abs(polyarea(...
  [reshape(net.x(1:end-1,1:end-1),nel,1) reshape(net.x(1:end-1,2:end),nel,1) reshape(net.x(2:end,2:end),nel,1) reshape(net.x(2:end,1:end-1),nel,1) reshape(net.x(1:end-1,1:end-1),nel,1)],...
  [reshape(net.y(1:end-1,1:end-1),nel,1) reshape(net.y(1:end-1,2:end),nel,1) reshape(net.y(2:end,2:end),nel,1) reshape(net.y(2:end,1:end-1),nel,1) reshape(net.y(1:end-1,1:end-1),nel,1)],...
  2));
area=reshape(area,ntube*nsec,1);
porarea=poros*area;
