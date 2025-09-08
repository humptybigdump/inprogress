"""
% =========================================================================
% deconvolution(x,yext,dt,theta,sigma,n_g,choice,submean,firstzero,
%               zerobefore,nreal)
%
% Non-negative deconvolution with geostatistical regularization
% The data must be continuous with regular time spacing
%
% O.A. Cirpka, M.N. Fienen, M. Hofer, E. Hoehn, A. Tessarini, R. Kipfer, 
% P.K. Kitanidis: Analyzing bank filtration by deconvoluting times series of 
% electric conductivity, Ground Water 45(3): 318-328, 2007, 
% doi:10.1111/j.1745-6584.2006.00293.x.
%
% input arguments:
% -----------------------------------------------------------------------------    
% x       input signal
% yext    output signal (must have the same length as x)
% dt      time increment [T]
% theta   slope of the variogram [T^-3]
% sigma   epistemic error
% n_g     length of the transfer function
% choice  string determining the method:
%         'smooth':    smooth estimate with fixed variogram slope
%         'condreal':  conditional realizations with fixed variogram slope
%         'est_theta': conditional realizations, variogram slope estimated by 
%                      expectation-maximization method
% submean Boolean whether to subtract the means of the input and output signals
%         (recommended for natural-tracer signals)
% firstzero Boolean whether the first value of the transfer Funtion must be 0 
% zerobefore Boolean whether the signals are zero before the measurements
%            (this can be used for the deconvolution of artificial-tracer data)
% nreal   number of realizations
%
% output:
% -----------------------------------------------------------------------------    
% variable    length     meaning
% -----------------------------------------------------------------------------    
% g_est       ng         estimated transfer function [T^-1]
% std_g       ng         standard dev. of estimation for g [T^-1]
% y_sim       n_obs-ng+1 simulated output signal
% theta       1          slope of the variogram [T^-3]
% sigma       1          updated epsitemic error 
%
% In case of conditional realizations, g_est and c_sim 2-D are
% arrays (columns are individual realizations)
%    
% (c) Olaf A. Cirpka, University of Tuebingen, 2025
"""
import numpy as np


# =============================================================================
# Main Function to Estimate zero-Order Reaction Rate
# =============================================================================
def deconvolution(x,yext,dt,theta,sigma,n_g,choice,submean,firstzero,
                  zerobefore,nreal=100):
    import scipy.linalg as la
    from scipy.linalg import toeplitz
    
    # consider only part of the output signal where the response is complete
    if zerobefore:
       y = yext
    else:
       y = yext[(n_g-1):]
    
    if submean:
       ymean=np.mean(y)
       y = y - ymean
       x -= np.mean(x)

    # construction of Jacobian
    if zerobefore:
       r = np.zeros(n_g)
       r[0] = x[0]
       J = dt*toeplitz(x,r)
    else:
       J =dt*toeplitz(x[n_g-1:],x[n_g-1::-1])
    
    # generalized covariance matrix of transfer function without theta
    G = toeplitz(np.arange(n_g*dt, 0, -dt))
        
    
    # =========================================================================
    # Inverse kernel: smooth geostatistical inversion with non-negativity
    #                 constraint
    # =========================================================================
    def smooth(theta,dt,y,J,sigma, G, firstzero):
        n_g = J.shape[1]
        # vector of indices
        ii = range(n_g)
        # generalized covariance matrix of production rate without theta
        Grr = G*theta
        # inverse of that
        iGrr=la.inv(Grr)
        # vector of entries affected by Lagrange multipliers
        if firstzero:
           hL = [0]
           nL = 1         
        else:
           hL=[]
           # numer of Lagrange multipliers
           nL=0
        hLold = [1]
        
        while hL != hLold:
            JiR  = J.T /sigma**2
            JiRJ = JiR @ J
            u = np.ones((n_g,1))
            umat=np.block([[np.block([JiRJ+iGrr,JiRJ@u])],\
                           [np.block([u.T@JiRJ,u.T@JiRJ@u])]]);
            urhs=np.block([[JiR @ y[:,None]],[u.T @ JiR @ y[:,None]]])
            umat2 = np.block([[np.block([JiRJ,JiRJ@u])],\
                             [np.block([u.T@JiRJ,u.T@JiRJ@u])]]);
            if nL==0:
               imat = la.inv(umat)
               sol = imat @ urhs
               g_est = sol[0:n_g]+sol[n_g]
               hLkeep = []
            else:
               Lmat=np.eye((n_g+1))
               Lmat[-1,:]=1
               Lmat=Lmat[:,hL]
               if Lmat.ndim==1:
                  Lmat=Lmat[:,None]
               mat = np.block([[umat,Lmat],[Lmat.T,np.zeros((nL,nL))]])
               imat = la.inv(mat)
               rhs = np.block([[urhs],[np.zeros((nL,1))]])
               sol = imat @ rhs
               g_est =sol[0:n_g]+sol[n_g]
               g_est[hL]=0
               nu = sol[n_g+1:]
               # detect which Lagrange multipliers to keep
               if firstzero:
                  hLkeep = [0] + np.array(hL)[nu[:,0]<0].tolist()
               else:
                  hLkeep = np.array(hL)[nu[:,0]<0].tolist()
            # check Lagrange multipliers
            hLold=hL
            # Lagrange multipliers to be added
            hLadd=np.array(ii)[g_est[:,0]<0]
            hL=list(set(hLkeep).union(hLadd))
            nL=len(hL)
            y_sim = J @ g_est
            sigma = np.sqrt(sum((y_sim[:,0]-y)**2)/(len(y)-n_g+nL-1))
                   
        # conditional covariance matrix of tansfer function
        mat2=np.zeros((n_g+1+nL,n_g+1+nL))
        mat2[0:n_g+1,0:n_g+1]=umat2;
        Cgg_ext = (imat @ mat2 @ imat)[0:n_g+1,0:n_g+1]
        A = np.ones((n_g,n_g+1))
        A[0:n_g,0:n_g]=np.eye(n_g)
        Cgg=A @ Cgg_ext @ A.T
        Cgg[hL,:]=0
        Cgg[:,hL]=0
        print(f'number of Lagrange multipliers: {nL}')
    
        return sigma, g_est[:,0], Cgg, y_sim
    
    # =========================================================================
    # Inverse kernel: geostatistical inversion by cokriging with non-negativity
    #                 constraint - conditional realizations
    # =========================================================================
    def condreal(theta,dt,y,J,sigma, G, firstzero,nreal):
        # update epistemic error
        sigma = smooth(theta,dt,y,J,sigma, G, firstzero)
        sigma=sigma[0]
        n_obs, n_g = J.shape[0], J.shape[1]
        # vector of indices
        ii = range(n_g)
        # generalized covariance matrix of production rate without theta
        Grr = G*theta
        # lower Cholesky decomposition
        C = la.cholesky(Grr,lower=True)
        # inverse of that
        iGrr=la.inv(Grr)
        # initialize ensembles
        g_all=np.zeros((n_g,nreal))
        y_sim_all=np.zeros((n_obs,nreal))
        
        for ireal in range(nreal):
            print(f'realization: {ireal+1}')
            repeat = True
            while repeat:
                # zero.mean unconditional realization
                g_uc = C @ np.random.randn(n_g,1)
                # add random measurement error to Z
                Zuc = y + sigma*np.random.randn(n_obs)
                # vector of entries affected by Lagrange multipliers
                if firstzero:
                   hL = [0]
                   # numer of Lagrange multipliers
                   nL = 1         
                else:
                   hL=[]
                   # numer of Lagrange multipliers
                   nL=0
                hLold = [1]
                # iteration counter
                iter = 0
                # maximum number of iterations
                maxiter = 100
                
                while hL != hLold and iter<maxiter:
                    JiR  = J.T / sigma**2
                    JiRJ = JiR @ J
                    u = np.ones((n_g,1))
                    umat=np.block([[np.block([JiRJ+iGrr,JiRJ@u])],\
                                   [np.block([u.T@JiRJ,u.T@JiRJ@u])]]);
                    urhs=np.block([[JiR @ Zuc[:,None]-JiRJ@g_uc],\
                                   [u.T @ JiR @ Zuc[:,None]-u.T@JiRJ@g_uc]])
                    if nL==0:
                       imat = la.inv(umat)
                       sol = imat @ urhs
                       g_all[:,ireal] = (sol[0:n_g]+sol[n_g]+g_uc).flatten()
                       hLkeep = []
                    else:
                       Lmat=np.eye((n_g+1))
                       Lmat[-1,:]=1
                       Lmat=Lmat[:,hL]
                       if Lmat.ndim==1:
                          Lmat=Lmat[:,None]
                       Lrhs=-g_uc[hL]
                       mat = np.block([[umat,Lmat],[Lmat.T,np.zeros((nL,nL))]])
                       imat = la.inv(mat)
                       rhs = np.block([[urhs],[Lrhs]])
                       sol = imat @ rhs
                       g_all[:,ireal] =(sol[0:n_g]+sol[n_g]+g_uc).flatten()
                       g_all[hL,ireal]=0
                       nu = sol[n_g+1:]
                       # detect which Lagrange multipliers to keep
                       if firstzero:
                          hLkeep = [0] + np.array(hL)[nu[:,0]<0].tolist()
                       else:
                          hLkeep = np.array(hL)[nu[:,0]<0].tolist()
                    # check Lagrange multipliers
                    hLold=hL
                    # Lagrange multipliers to be added
                    hLadd=np.array(ii)[g_all[:,ireal]<0]
                    hL=list(set(hLkeep).union(hLadd))
                    nL=len(hL)
                    iter += 1
                if iter<maxiter: 
                   repeat= False
                else:
                   print(f'repeat realization {ireal+1}')
            # solve the advection-dispersion equation with high resolution
            y_sim_all[:,ireal] = J @ g_all[:,ireal]
        g_mean = np.mean(g_all,axis=1)
        Cgg = (g_all-g_mean[:,None]@np.ones((1,nreal))) @ \
              (g_all-g_mean[:,None]@np.ones((1,nreal))).T /nreal 
    
        return sigma, g_all, Cgg, y_sim_all

    # =========================================================================
    # Inverse kernel: geostatistical inversion by cokriging with non-negativity
    #                 or non-positivity constraint - conditional realizations
    #                 with estimation of variogram slope
    # =========================================================================
    def esttheta(theta,dt,y,J,sigma, G, firstzero,nreal):
        # from scipy.optimize import least_squares
        from scipy.optimize import minimize
        thetaold=theta*2
        while abs(thetaold-theta)/thetaold >0.01:
            sigma, g_all, Cgg, y_sim = condreal(theta,dt,y,J,sigma, G, 
                                                firstzero,nreal)
            def sumprob(lnthetadt,g_all):
                thetadt = np.exp(lnthetadt)
                lnp = 0
                ng, nreal = g_all.shape
                for ireal in range(nreal):
                    # nnz = sum(prod_all[:,ireal]!=0)
                    lnp += 0.5*(ng-1)*np.log(4*np.pi*thetadt) \
                        + np.sum(np.diff(g_all[:,ireal])**2) *.25/thetadt
                return lnp
            result = minimize(sumprob,np.log(theta*dt),
                              args=(g_all),method='Nelder-Mead')
            thetaold=theta*1.0
            theta = np.exp(result.x[0])/dt
            print(f'new theta = {theta}')
        return sigma, g_all, Cgg, y_sim, theta


    
    print(' ')
    match choice:
        case 'smooth':
            # perform cokriging estimate
            sigma, g_est, Cgg, y_sim = smooth(theta,dt,y,J,sigma, G, firstzero)
            if submean:
               y_sim += ymean
            print('Method of Choice: Smooth Estimate with Fixed Slope')
            print(f'Epistemic error: {sigma:.3g}')
        case 'condreal':
            sigma, g_est, Cgg, y_sim = condreal(theta,dt,y,J,sigma, G, firstzero,nreal)
            if submean:
               y_sim += ymean
            print('Method of Choice: Conditional Realizations with Fixed Variogram-Slope')
            print(f'Epistemic error: {sigma:.3g}')
        case 'est_theta':
            sigma, g_est, Cgg, y_sim, theta = esttheta(theta,dt,y,J,sigma, G, firstzero,nreal)
            if submean:
               y_sim += ymean
            print('Method of Choice: Conditional Realizations - Estimate Variogram-Slope')
            print(f'Epistemic error: {sigma:.3g}')
        
    print(f'Slope of variogram: {theta:.3g}')
    
    # propagate uncertainty of rate back to concentrations
    Cyy   = J @ Cgg @ J.T
    std_y = np.sqrt(Cyy.diagonal())
    std_g = np.sqrt(np.diag(Cgg))

    return g_est, std_g, y_sim, std_y, theta, sigma

