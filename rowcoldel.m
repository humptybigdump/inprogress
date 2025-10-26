function Mmod=rowcoldel(M,which,symmetric)
% mex function ROWCOLDEL                                           
% Usage within MATLAB:                                             
% Mmod=rowcoldel(M,which,symmetric)                                
% deletes rows and columns of a sparse matrix by inserting         
% zero entries into the corresponding off-diagonals and            
% unity entries into the main diagonal                             
% M : real, sparse matrix                                          
% which: vector of indices of the rows and columns to be deleted   
% symmetric: flag which indicates whether M has symmetric structure
%         Note 0 => asymmetric structure, 1=> symmetric.           
% mexFunction is the gateway routine for the MEX-file.            
% returns the modied matrix                                        

% compile within MATLAB by: mex -O rowcoldel.c                     
% requires a valid C-compiler and correct setting in mexopts.sh    
