function K=randomK(nx,dx,lx,ang,sigY,Ctype,Kg)
% ============== BEGIN AUTO-COVARIANCE BLOCK ======================================
nx_ex=nx+round(5*lx./dx);
% total number of nodes
ntot=prod(nx_ex);

% Define the physical grid
% Grid in Physical Coordinates
[X,Y]=meshgrid(-nx_ex(1)/2*dx(1):dx(1):(nx_ex(1)-1)/2*dx(1),...
               -nx_ex(2)/2*dx(2):dx(2):(nx_ex(2)-1)/2*dx(2));
% Rotation into Longitudinal/Transverse Coordinates
X2= cos(ang)*X + sin(ang)*Y;
Y2=-sin(ang)*X + cos(ang)*Y;
      
H=sqrt((X2/lx(1)).^2+(Y2/lx(2)).^2);


disp([datestr(clock) ': Calculate Auto-Covariance']);

% Covariance Matrix of Log-Conductivities
if (Ctype==1)
   RYY=sigY*exp(-abs(H));
else
   RYY=sigY*exp(-H.^2);
end

% ============== END AUTO-COVARIANCE BLOCK ========================================

% ============== BEGIN POWER-SPECTRUM BLOCK =======================================
% Fourier Transform (Origin Shifted to Node (1,1))
% Yields Power Spectrum of the field
SYY=fftn(fftshift(RYY))/ntot;
% Remove Imaginary Artifacts
SYY=abs(SYY);SYY(1,1)=0;
% ============== END POWER-SPECTRUM BLOCK =========================================

% ============== BEGIN FIELD GENERATION BLOCK =====================================
% Generate the fields
disp([datestr(clock) ': Generate Random Field']);
% Generate a field of random real numbers,
% transform the field into the spectral domain,
% and evaluate the corresponding phase-spectrum.
% This random phase-spectrum and the given power spectrum
% define the Fourier transform of the random autocorrelated field.
ran=sqrt(SYY).*(1i*randn(size(SYY))+randn(size(SYY)));
% Backtransformation into the physical coordinates
K=Kg*exp(real(ifftn(ran*ntot)));
K=K(1:nx(2),1:nx(1));
