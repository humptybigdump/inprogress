import numpy as np
import matplotlib.pyplot as plt


# Forward Model for VES
# Usage for two layer model:
#  apparent_resistivity = VESForward_RD([res1 res2 res3 thick1 thick2], VectorABHalf)
def VESForward_RD(Params,VectorABHalf):
    

    ParameterLength = len(Params)
    if ParameterLength % 2 == 1:
        r = Params[0:int((ParameterLength+1)/2)]                   # resistivities
        t = Params[int((ParameterLength+1)/2):ParameterLength]     # thickness
        s = VectorABHalf
    
        ls = len(s)
        u = np.zeros(ls)
        rho_semu = np.zeros(ls)
    
        for ii in range(1,ls+1):
            q = 13
            f = 10
            m = 4.438
            x = 0
            e = np.exp(np.log(10)/(2*m))
            h = 2 * q - 2
            u[ii-1] = s[ii-1]*np.exp(-f*np.log(10)/m-x)
            l = len(r)
            n = 1
    
            li = n + h
            a = np.zeros(li)
        
            for i in range(1,li):
                w = l
                T = r[l-1]
            
                while w > 1:
                    w = w-1
                    aa = np.tanh(t[w-1]/u[ii-1])
                    T = (T+r[w-1]*aa)/(1+T*aa/r[w-1])
        
                a[i-1] = T
                u[ii-1] = u[ii-1]*e    
        
            i = 1
            rho_a = 105*a[i-1]-262*a[i+1]+416*a[i+3]-746*a[i+5]+1605*a[i+7]
            rho_a = rho_a-4390*a[i+9]+13396*a[i+11]-27841*a[i+13]
            rho_a = rho_a+16448*a[i+15]+8183*a[i+17]+2525*a[i+19]
            rho_a = (rho_a+336*a[i+21]+225*a[i+23])/10000;
            rho_semu[ii-1] = rho_a
    else:
        print('Params must be odd number (first resistivities, then layer thickness.')
        rho_semu = 0;
              
    return rho_semu


