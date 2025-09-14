function [idx,D] = nearest_neighbor (Q,R)
% function [idx,D] = nearest_neighbor (Q,R)
%
% This function interprets Q and R as two sets of d-dimensional row vectors
% and calculates for each point in Q its closest neighbor in R (with
% respect to the Euclidean distance). 
% Output: vectors idx and D, where each entry correponds to one point in Q.
%   idx: indices from those points in R assigned to the points in Q.
%   D:   euclidian distance between matched points.
%
% Based on an implementation by Yi Cao at Cranfield University on 25 March 2008
% Adapted by Martin Lauer at Karlsruhe Institute of Technology 

[N,M] = size(Q); % N: number of points in Q, M: length of descriptor vector
L = size(R,1);   % L: number of points in R

% Initialize idx and D
idx = zeros(N,1);
D = idx;

% Iterate over each point in Q
for k=1:N
    d = zeros(L,1);
    % compute squared Euclidian distance between point k from Q 
    % and all points in R
    for t=1:M
        d = d+(R(:,t)-Q(k,t)).^2;  % calculate squared Euclidean distances
    end
    [D(k), idx(k)] = min(d);  % find closest point
end
D = sqrt(D);
end
