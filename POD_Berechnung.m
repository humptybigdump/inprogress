clear all;
close all;
clc;

%% fetch data

folder_name = "POD_Data";

if ~exist(strcat(pwd, "/", "Data"), "dir")
    url = "https://bwsyncandshare.kit.edu/s/ZWiDsYTYskW6jAb/download/POD_Data.zip";
    zip_name = strcat(folder_name, ".zip");
    zip_path = strcat(pwd, "/", zip_name);

    outfile = websave(zip_path, url);
    unzip(zip_name);
    delete(zip_name);
end


%% Snapshot POD 

clear;

skip_nodes=1; 

velocitydata='Data/VelData.mat'
load(velocitydata);


[X_size,Y_size,tsteps]=size(U_3D);

%% Zeitliche Mittelung und deren Substraktion von dein einzelnen Feldern
U_3D_sum=zeros(X_size,Y_size);
V_3D_sum=zeros(X_size,Y_size);
for i=1:tsteps
  U_3D_sum=U_3D_sum+U_3D(:,:,i);
  V_3D_sum=V_3D_sum+V_3D(:,:,i);
    
end
U_3D_mean=U_3D_sum/tsteps;
V_3D_mean=V_3D_sum/tsteps;
figure
quiver(xx,yy,U_3D_mean,V_3D_mean);
axis equal
title('U-mean')

    
for i=1:tsteps
  U_3D(:,:,i)=U_3D(:,:,i)-U_3D_mean;
  V_3D(:,:,i)=V_3D(:,:,i)-V_3D_mean;
%   disp('dada')
end


%% Eigenwertproblem
% Schreibe alle Geschwindigkeitsfelder in 2D Matrix
U=nan(X_size*Y_size,tsteps);
for i=1:tsteps
    u_temp=U_3D(:,:,i);    
    v_temp=V_3D(:,:,i);
    U(1:X_size*Y_size,i)=u_temp(:);
    U(X_size*Y_size+1:X_size*Y_size*2,i)=v_temp(:);
end


disp('Erstelle R')
R=transpose(U)*U;
% R = codistributed(R);
disp('Fertig mit R: Starte Eigenvektorberechnung')
% break
% return
%% Eigenvektorberechnung
tic
[Eigenvect,lambda]=eig(R);
toc

disp('Fertig mit Eigenvektorberechnung')



for i=1:tsteps
vektlambda(i)=lambda(i,i);
end

lambda1=sort(vektlambda);

% Normiere Eigenwerte
lambda_2=lambda1(end:-1:1);
lambdamagnitude=sum(abs(lambda1));
lambda_2=lambda_2./lambdamagnitude;


%% Drehe um. Größter EV nach vorne
if vektlambda==lambda1
Eigenvect=Eigenvect(:,end:-1:1);
else 
    disp('Achtung. EW waren nach eig() bereits so sortiert, dass der groesste EW vorne Stand. Kein Drehen notwendig')
end

%% Umrechnung der Moden in "Pseudo-Geschwindigkeitsfelder"
%Dieser Schritt ist nur bei der Snapshot POD notwendig. Bei der direct POD
%nicht.

    psi=U*Eigenvect;
    for i_psi=1:length(psi(1,:))
    psi(:,i_psi)=psi(:,i_psi)./norm(psi(:,i_psi));
    end
    
%% Wichtungskoeffizienten
a=nan(tsteps,tsteps);

disp('Berechne a_i')
   for i=1:tsteps
       a(:,i)=transpose(psi)*U(:,i);
%        disp(num2str(i))
   end
save('Data/POD_Results.mat','xx','yy','psi','lambda','lambda_2','a')



