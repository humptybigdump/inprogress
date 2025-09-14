"""
Uebung 3.0: Ausgabemodul

Das Modul erhält als Eingabe Parameter 1-2 Sätze (t, x, dx, ddx)

Autor: Mark-Patrick Mühlhausen

Datum: 2025-08-07
"""
import matplotlib.pyplot as plt

def plotDiagrams(name,t1,x1,dx1,ddx1,t2=None,x2=None,dx2=None,ddx2=None):
    
    if not t2 is None:
        plt.figure()
        plt.plot(t1,x1,'k-',t2,x2,'r.',linewidth=4)
        plt.title('Lageaenderung des Stopfens',fontsize=25)
        plt.xlabel('Zeit [s]',fontsize=22)
        plt.ylabel('Position [m]',fontsize=22)
        plt.tick_params(axis='both', which='major', labelsize=15)
        plt.legend(['Analytisch','Gekoppelt'])
        plt.xlim([0,1])
        plt.ylim([0,1])
        plt.grid(True)
        #plt.show()
        
        plt.savefig(name+'_t_x.png',dpi=300)
        
        plt.figure()    
        plt.plot(t1,dx1,'k-',t2,dx2,'r.',linewidth=4)
        plt.title('Lageaenderung des Stopfens',fontsize=25)
        plt.xlabel('Zeit [s]',fontsize=22)
        plt.ylabel('Geschwindigkeit [m/s]',fontsize=22)
        plt.tick_params(axis='both', which='major', labelsize=15)
        plt.legend(['Analytisch','Gekoppelt'])
        plt.xlim([0,1])
        plt.ylim([-4,8])
        plt.grid(True)
        
        plt.savefig(name+'_t_v.png',dpi=300)
        
        plt.figure()    
        plt.plot(t1,ddx1,'k-',t2,ddx2,'r.',linewidth=4)
        plt.title('Lageaenderung des Stopfens',fontsize=25)
        plt.xlabel('Zeit [s]',fontsize=22)
        plt.ylabel('Beschleunigung [m/s2]',fontsize=22)
        plt.tick_params(axis='both', which='major', labelsize=15)
        plt.legend(['Analytisch','Gekoppelt'])
        plt.xlim([0,1])
        plt.ylim([-200,300])
        plt.grid(True)
        
        plt.savefig(name+'_t_a.png',dpi=300)
    else:   
        plt.figure()    
        plt.plot(t1,x1,'k-',linewidth=4)
        plt.title('Lageaenderung des Stopfens',fontsize=25)
        plt.xlabel('Zeit [s]',fontsize=22)
        plt.ylabel('Position [m]',fontsize=22)
        plt.tick_params(axis='both', which='major', labelsize=15)
        plt.legend(['Analytisch'])
        plt.xlim([0,1])
        plt.ylim([0,1])
        plt.grid(True)
        
        plt.savefig(name+'_t_x.png',dpi=300)
        
        plt.figure()    
        plt.plot(t1,dx1,'k-',linewidth=4)
        plt.title('Lageaenderung des Stopfens',fontsize=25)
        plt.xlabel('Zeit [s]',fontsize=22)
        plt.ylabel('Geschwindigkeit [m/s]',fontsize=22)
        plt.tick_params(axis='both', which='major', labelsize=15)
        plt.legend(['Analytisch'])
        plt.xlim([0,1])
        plt.ylim([-4,8])
        plt.grid(True)
        
        plt.savefig(name+'_t_v.png',dpi=300)
        
        plt.figure()    
        plt.plot(t1,ddx1,'k-',linewidth=4)
        plt.title('Lageaenderung des Stopfens',fontsize=25)
        plt.xlabel('Zeit [s]',fontsize=22)
        plt.ylabel('Beschleunigung [m/s2]',fontsize=22)
        plt.tick_params(axis='both', which='major', labelsize=15)
        plt.legend(['Analytisch'])
        plt.xlim([0,1])
        plt.ylim([-200,300])
        plt.grid(True)
        
        plt.savefig(name+'_t_a.png',dpi=300)