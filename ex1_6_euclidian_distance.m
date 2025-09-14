% solution exercise 1.6
function [d] = ex1_6_euclidian_distance(u, v)
% Compute the euclidian distance between two vectors u and v
d = sqrt(sum((u - v).^2));

end