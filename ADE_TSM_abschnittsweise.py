# -*- coding: utf-8 -*-
"""
Created on Sun Aug 24 11:10:30 2025

@author: Pauline Fesser & Lena Oker
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from scipy.linalg import inv
from scipy.stats import qmc
from invlap import invlap

# Einlesen txt Datei der Tracerdaten
data = pd.read_csv('tracerdaten_cor.txt',delimiter=';')

# zugegebene Masse [mg]
m = 15000

# Abstände zwischen den Messstellen [m]
xall = (420, 1300, 1710, 990)

# ADE Fit (Advektions Dispersions Gleichung)
# Vorbereitung Ergebnis array 
var_c   = np.full(4,np.nan)     # Varianz der Parameter
bestpar = np.full((4,3),np.nan) # beste Schätzung der 3 Parameter (v=Fließgeschwindigkeit, D=Dispersionskoeffizient, rec=Wiederfindung)
std_par = np.full((4,3),np.nan) # Standardabweichung dieser Parameter

# Transferfunktion
def g(T, x, v, D, rec):
    T = np.array(T, dtype=float)    # Zeit als numpy-array (floats)
    g_mod = np.zeros_like(T)        # array, um Transferfunktion zu speichern (anfangs 0)
    mask = T > 0                    # nur T > 0 verwenden
    g_mod[mask] = rec * (x / (2 * np.sqrt(np.pi * D * (T[mask]**3)))) * \
                   np.exp(-((x - v*T[mask])**2) / (4 * D * T[mask]))
    return g_mod                    # Rückgabe der Transferfunktion

# Residuenfunktion
def residuals(par, cup, x, t, data, dt):
    v, D, rec = par                                     # Parameter
    g_mod = g(t, x, v, D, rec)                          # Transferfunktion
    cdown = np.convolve(g_mod, cup, mode='full') * dt   # unterstromige Durchbruchskurve cdown aus Faltung von g und cup 
    cdown = cdown[:len(data)]                           # Ergebnis der Faltung auf Länge der Originaldaten anpassen
    return cdown - data                                 # Differenz zwischen Modell und Messdaten  (Residuen)

# Berechnung Durchfluss M1 mit nulltem Moment
t = np.array(data.iloc[:,1])*3600   # Zeit in Sekunden
cmeas = np.array(data.iloc[:,2])    # gemessene Leitfähigkeitszeitreihe M1
dt = t[1]-t[0]                      # zeitlicher Abstand zwischen den Messpunkten
m0 = np.sum(cmeas)*dt               # 0. Moment 
Q = m/m0                            # Durchfluss an M1

print(f'Q aus BTC1: {Q:.3f} m³/s')

# gemeinsamen plot für ADE und TSM vorbereiten
fig, axes = plt.subplots(2, 2, figsize=(15,10))  # 4 Subplots (2x2)
axes = axes.flatten()  

# Vorbereitung Ergebnisausgabe ADE Parameter 
ade_results = []

# Schleife für alle 4 Messtellen
for MS in range(4):
    print(f"\nParameter Messstelle {MS+1}")
    if MS == 0:                                     # Sonderfall für M1 (Inputsignal = Dirac-Impuls)
        tin = t
        cin = np.zeros_like(t)
        cin[0] = m / Q / dt                         # Dirac-Puls als Input
    else:
        tin = t
        cin = data.iloc[:, MS+1].to_numpy()         # Inputsignal: oberstromige Messstelle
    tout = t; cout = data.iloc[:,MS+2].to_numpy()   # Outputsignal: unterstromig benachbarte Messstelle    
    x = xall[MS]                                    # Abstände zwischen den Messstellen

    # Berechnung Momente
    m0in = sum(cin)*dt; m0out = sum(cout)*dt        # nulltes Moment
    mu_in  = sum(cin*tin)*dt/m0in                   # erstes Moment (Fließzeit)
    mu_out = sum(cout*tout)*dt/m0out
    var_in  = sum(cin*(tin-mu_in)**2)*dt/m0in       # zweites zentriertes Moment (Varianz der Fließzeit)
    var_out = sum(cout*(tout-mu_out)**2)*dt/m0out

    recov = m0out/m0in                              # Wiederfindung
    v = x/(mu_out - mu_in)                          # Fließgeschwindigkeit
    D = 0.5*(var_out - var_in)/x * v**3             # Dispersionskoeffizient
    Q = m/m0out                                     # Durchfluss

    # Startparameter für den Fit (leicht veränderte Parameter aus den Momenten)
    x0 = [v*1.1, D*0.5, recov]
   
    # Funktion, welche für die Parameter die Residuenfunktion aufruft
    func = lambda par: residuals(par, cin, x, t, cout, dt)
    
    # Minimierung der Summe der quadrierten Residuen
    result = least_squares(func, x0)
    par = result.x          # beste Parameter
    bestpar[MS, :] = par    # Speichern der besten Parameter

    # Varianzschätzung
    SSE = 2 * result.cost                            # Summe der Fehlerquadrate (Gesamtabweichung zwischen Modell und Messdaten)
    var_c[MS] = SSE / (len(cout) - len(par))         # Residuenvarianz (Abweichung der Messwerte vom Modell)
    Cpp = var_c[MS] * inv(result.jac.T @ result.jac) # Kovarianzmatrix der geschätzten Parameter
    std_par[MS, :] = np.sqrt(np.diag(Cpp))           # Standardabweichung der Parameter
    
    # Ausgabe der ADE-Parameter
    print(f"σ Messungen: {np.sqrt(var_c[MS]):.3f} µg/L")
    print(f"v    = {par[0]:.3g} ± {std_par[MS,0]:.5g} m/s")
    print(f"D    = {par[1]:.3g} ± {std_par[MS,1]:.5g} m²/s")
    print(f"rec= {par[2]:.3g} ± {std_par[MS,2]:.5g}")
    print(f'Q: {Q:.3f} m³/s')
    

    # Berechnung Modellkurve 
    v, D, rec = par                                 # Parameter auspacken
    g_mod = g(t, x, v, D, rec)                      # ADE-Transferfunktion mit bester Parameterschätzung
    mod = np.convolve(g_mod, cin, mode='full') * dt # Faltung
    mod = mod[:len(cout)]                           # Anpassung an Länge von cout
    
    # Fit-Güte ADE
    SSE_ADE = np.sum((cout - mod)**2)               # Summe der kleinsten Fehlerquadrate (Summe der quadrierten Abweichungen, je kleiner desto besser passt Modell)
    MSE_ADE = SSE_ADE / len(cout)                   # mittleres quadratisches Fehlermaß (SSE geteit durch Anzahl Datenpunkte, durchschnittlicher quadratischer Fehler)
    RMSE_ADE = np.sqrt(MSE_ADE)                     # Root Mean Squared Error (Abweichung zwischen Modell und Messdaten in gleicher Einheit wie die Messdaten)
    
    # Speichern der ADE-Parameter und der Güte-Parameter in einem dictionary
    ade_results.append({
        "MS": MS+1,
        "σ_meas": np.sqrt(var_c[MS]),
        "v": par[0],
        "v_std": std_par[MS,0],
        "D": par[1],
        "D_std": std_par[MS,1],
        "rec": par[2],
        "rec_std": std_par[MS,2],
        "Q": Q,
        "SSE": SSE_ADE,
        "RMSE": RMSE_ADE
    })
    
    # Plot
    ax = axes[MS]  # Subplot für diese Messstelle
    ax.plot((t/60)[::12], cout[::12], '.', label=f"Durchbruchskurve", color='black') # Plot Messdaten 
    ax.plot(t/60, mod, '-', label=f"ADE", color='blue') #Plot ADE-Fit
    
#%% TSM Fit (Transiente Speicherzonen Modell)

# Vorbereitung Ergebnis array
var_c   = np.full(4,np.nan)     # Varianz der Parameter
bestpar = np.full((4,5),np.nan) # beste Schätzung der 5 Parameter (v=Fließgeschwindigkeit der mobilen Phase, D=Dispersionskoeffizient, Arel=Aimob/Amob, k=Austauschrate, recov=Wiederfindung)
std_par = np.full((4,5),np.nan) # Standardabweichung der Parameter 

# Laplace-transformierte Transferfunktion (im Laplace-Raum ist Lösung einfacher)
def g_laplace(s, x, v, D, beta, k, recov):
    b = s + beta * s * k / (k + s)
    alpha = (-v + np.sqrt(v ** 2 + 4 * D * b)) / D * 0.5
    g = recov * np.exp(-alpha * x)
    return g

# Residuenfunktion
def residuals(par, cin, x, t, data):
    g_wo_0 = invlap(g_laplace, t[1:], 0, 1e-9, x, *par) # Rücktransformation der Transferfunktion aus dem Laplace-Raum in die Zeitdomäne
    g_wo_0[np.isnan(g_wo_0)] = 0                        # Nans werden durch 0 ersetzt
    g=np.zeros(len(t))                                  # array, um Transferfunktion zu speichern
    g[1:]=g_wo_0                                        # g ab t>0 (gleich lang wie Transferfunktion ab t>0)
    mod = np.convolve(g, cin, mode='full')*dt           # Faltung Transferfunktion mit Inputsignal cin
    mod=mod[0:len(data)]                                # Länge an Messdaten anpassen
    return mod - data                                   # Differenz zwischen modellierter Durchbruchskurve und Messdaten (Residuen)

# Berechnung Durchfluss M1 mit nulltem Moment
t = np.array(data.iloc[:,1])*3600   # Zeit in Sekunden
cmeas = np.array(data.iloc[:,2])    # gemessene Leitfähigkeitszeitreihe M1
dt = t[1]-t[0]                      # zeitlicher Abstand zwischen den Messpunkten
m0 = np.sum(cmeas)*dt               # nulltes Moment
Q = m/m0                            # Durchfluss an M1

print(f'Q from m0 at BTC 1: {Q:.3f} m3/s')

# Definition generischer multistart least-square fit
def multistart(func,n,x0,bounds,takelogpar):            # func=Residuenfunktion, n=Anzahl Startpunkte für multistart, x0=Startparameter                     
                                                        # bounds= Bereich, aus dem Parameter gewählt werden, takelogpar=Optimierung in log Skala
    # Latin Hypercube Sampler
    sampler = qmc.LatinHypercube(d=len(x0))             # wählt n zufällige Startpunkte im d-dimensionalen Raum (d=Anzahl der Parameter)
    # Ziehung sample
    sample = sampler.random(n=n)
    # least-square fit mit Startparametern
    result=least_squares(func, x0, diff_step=0.001*x0)  # Least Square Fit mit den Startparametern
    # Parameter speichern, Wert der Zielfunktion, Jacobi-Matrix
    bestpar = result.x
    bestcost=result.cost
    jac=result.jac
    
    for i in range(n):                                  # Schleife für jeden zufällig gewählten Startpunkt
        if takelogpar:                                  # Optimierung der Parameter im Logarithmus
           # wenn Parameter log-Parameter sind Funktion neu definieren 
           funclog = lambda lnpar: func(np.exp(lnpar))
           # Startwerte
           lnpar = bounds[:,0]+sample[i,:]*(bounds[:,1]-bounds[:,0])
           # least-square fit
           result = least_squares(funclog, lnpar, diff_step=0.001*lnpar)
        else:                                           # Optimierung lineare Parameter
           # Startwerte
           par = bounds[:,0]+sample[i,:]*(bounds[:,1]-bounds[:,0])
           # least-square fit
           result = least_squares(func, par, diff_step=0.001*par)
        if result.cost<bestcost:                        # Vergleich aktueller Fit mit bisher bestem Fit
           # wenn aktueller fit besser, als bisheriger fit 
           # Parameter speichern, Wert der Zielfunktion, Jacobi-Matrix
           if takelogpar:
              bestpar = np.exp(result.x)
           else:
              bestpar = result.x 
           bestcost=result.cost
           jac=result.jac
        print(f'trial {i}: current SSE = {2*result.cost:.1f}, best SSE={2*bestcost:.1f}')
    return bestpar, bestcost, jac    

# Vorbereitung Ergebnis-Ausgabe TSM-Parameter 
all_results = []

# Schleife für alle Durchbruchskurven
for MS in range(4):
    print(f"Analyze BTC {MS+1}")
    if MS==0:
       tin = 0.
       cin = m/Q/dt
    else:
       tin = t
       cin = np.array(data.iloc[:,MS+1])
    
    tout = t
    cout = np.array(data.iloc[:,MS+2])
    
    dt = tout[1]-tout[0]
    cmeas = cout
    x = xall[MS] 
    # Momentanalyse
    m0in  = np.sum(cin)*dt
    m0out = np.sum(cout)*dt
    
    mu_tau_in  = np.sum(cin*tin)*dt/m0in
    mu_tau_out = np.sum(cout*tout)*dt/m0out
    
    var_tau_in  = np.sum(cin*(tin-mu_tau_in)**2)*dt/m0in
    var_tau_out = np.sum(cout*(tout-mu_tau_out)**2)*dt/m0out
    
    # Startparameter aus der Momentanalyse
    recov = m0out/m0in
    v = x/(mu_tau_out-mu_tau_in)
    D = 0.5*(var_tau_out-var_tau_in)/x*v**3
    # Bounds und Startparameter
    # Reihenfolge: v, D, Arel, k, recovery
    # zuerst mit log-Parametern und weiten Grenzen
    x0 = np.array([v*1.1, D*0.5, 0.05, 0.005, recov])
    bounds = np.log(x0[:,None] @ np.array([.1,10])[None,:])
    bounds[-1,:] = np.log(x0[-1]*np.array((.8,1.2)))

    # Anzahl der samples
    if MS == 0:    
       n = 100
    else:
       n = 50 
    
    func = lambda par: residuals(par,cin,x,t,cmeas)
    bestpar[MS,:], bestcost, jac = multistart(func,n,x0,bounds,True)    
    
    # Eingrenzung mit schmaleren Grenzen und ohne Logarithmus
    x0 = bestpar[MS,:]
    bounds = x0[:,None] @ np.array([.5,2.])[None,:]
    bounds[-1,:] = x0[-1]*np.array((.8,1.2))    
    bestpar[MS,:], bestcost, jac = multistart(func,n,x0,bounds,False)    
    
    # noch schmalere Grenzen
    par = bestpar[MS,:]
    x0 = par
    bounds = x0[:,None] @ np.array([.9,1.1])[None,:]
    bestpar[MS,:], bestcost, jac = multistart(func,n,x0,bounds,False)    
    
    # Summe der kleinsten Fehlerquadrate
    SSE = 2*bestcost
    # Varianz der Messung
    var_c[MS] = SSE/(len(cout)-len(par))
    # Kovarianzmatrix der Parameter
    Cpp = var_c[MS]*inv(jac.T@jac)
    # Standardabweichung der Parameter
    std_par[MS,:] = np.sqrt(np.diag(Cpp))
    
    print(f"Standard deviation of measurements: {np.sqrt(var_c[MS]):.3f} ug/l")
    print("Optimized parameters:")
    print(f"v    = {bestpar[MS,0]:.3g} +- {std_par[MS,0]:.5g} m/s")
    print(f"D    = {bestpar[MS,1]:.3g} +- {std_par[MS,1]:.5g} m2/s")
    print(f"Arel = {bestpar[MS,2]:.3g} +- {std_par[MS,2]:.5g}")
    print(f"k    = {bestpar[MS,3]:.3g} +- {std_par[MS,3]:.5g} /s")
    print(f"recov= {bestpar[MS,4]:.3g} +- {std_par[MS,4]:.5g}")
    print(f"Q    = {Q/np.prod(bestpar[:MS+1,4]):.3g}  m3/s")
    
    # Simuliertes Modell
    g_wo_0 = invlap(g_laplace, t[1:], 0, 1e-9, x, *bestpar[MS,:])
    g_wo_0[np.isnan(g_wo_0)] = 0
    g = np.zeros(len(t))
    g[1:]=g_wo_0
    modTSM = np.convolve(g, cin, mode='full')*dt
    modTSM=modTSM[0:len(cmeas)]
    
    # Fit-Güte TSM
    SSE_TSM = np.sum((cmeas - modTSM)**2)
    MSE_TSM = SSE_TSM / len(cmeas)
    RMSE_TSM = np.sqrt(MSE_TSM)

    # Zugriff auf Güte-Parameter des ADE-Fits
    SSE_ADE = ade_results[MS]["SSE"]
    RMSE_ADE = ade_results[MS]["RMSE"]
    
    # Ausgabe: Güte der Fits von ADE und TSM
    results_df1 = pd.DataFrame({
        "Modell": ["ADE", "TSM"],
        "SSE": [SSE_ADE, SSE_TSM],
        "RMSE [µg/L]": [RMSE_ADE, RMSE_TSM],
        })

    print("\nFit-Güte Messstelle", MS+1)
    print(results_df1.to_string(index=False))
    print('')
    
    # Speichern der Ergebnisse für die Güte von ADE und TSM 
    results_df2 = pd.DataFrame({
    "Messstelle": [MS+1, MS+1],
    "Modell": ["ADE", "TSM"],
    "SSE": [SSE_ADE, SSE_TSM],
    "RMSE [µg/L]": [RMSE_ADE, RMSE_TSM],
    })
    all_results.append(results_df2)
    
    
    # Plot des Fit
    ax = axes[MS]  # gleicher Subplot wie ADE
    ax.plot(t/60, modTSM, '-', label=f"TSM",color='orange')
    ax.set_title(f"Messstelle {MS+1}", fontsize=17)
    ax.legend(fontsize=13)
    ax.tick_params(axis='x', labelsize=15)  # Schriftgröße x-Achse
    ax.tick_params(axis='y', labelsize=15)  # Schriftgröße y-Achse
    ax.set_xlabel('Zeit [min]', fontsize=16)
    ax.set_ylabel('Konzentration [µg/L]', fontsize=16)
    ax.grid(True)
plt.tight_layout()
plt.show()

# Ergebnisausgabe Parameter ADE
print("Summary of results ADE (abschnittsweise außer Q)")
print('')
for res in ade_results:
    print(f"ADE: Measurement station {res['MS']}:")
    print(f"Standard deviation of measurements: {res['σ_meas']:.3f} ug/l")
    print("Optimized parameters:")
    print(f"v    = {res['v']:.3g} +- {res['v_std']:.5g} m/s")
    print(f"D    = {res['D']:.3g} +- {res['D_std']:.5g} m2/s")
    print(f"rec  = {res['rec']:.3g} +- {res['rec_std']:.5g}")
    print(f"Q    = {res['Q']:.3g}  m3/s")
    print('')


# Ergebnisausgabe Parameter TSM
print("Summary of results TSM (abschnittsweise außer Q)")
print('')
for MS in range(4):
    print(f'TSM: Measurement station {MS+1}:')
    print(f"Standard deviation of measurements: {np.sqrt(var_c[MS]):.3f} ug/l")
    print("Optimized parameters:")
    print(f"v    = {bestpar[MS,0]:.3g} +- {std_par[MS,0]:.5g} m/s")
    print(f"D    = {bestpar[MS,1]:.3g} +- {std_par[MS,1]:.5g} m2/s")
    print(f"Arel = {bestpar[MS,2]:.3g} +- {std_par[MS,2]:.5g}")
    print(f"k    = {bestpar[MS,3]:.3g} +- {std_par[MS,3]:.5g} /s")
    print(f"recov= {bestpar[MS,4]:.3g} +- {std_par[MS,4]:.5g}")
    print(f"Q    = {Q/np.prod(bestpar[:MS+1,4]):.3g}  m3/s")
    #print(f'uncertainty of recovery: {std_par[MS,4]:.5g}')
    print('')

# Ergebnisausgabe Güte des Fits
final_results = pd.concat(all_results, ignore_index=True)

print("\n Güte der Fits aller Messstellen")
print(final_results.to_string(index=False))