function [ s ] = func_seq( start_val,inc_val,max_val )
% This function generates a sequence

% Define the length of the resulting sequence
l=(max_val-start_val)/inc_val+1;
% If l should be an integer, reduce it to the next integer (e.g., if
% l=12.9, then we would use l=12)
l=floor(l);
s=zeros(l,1); % initialize sequence vector
s(1)=start_val;
for i=2:l
    s(i)=s(i-1)+inc_val;
end
end
