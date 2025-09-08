# -*- coding: utf-8 -*-
"""
Created on Thu Jul  3 17:20:51 2025

### MGB: hQ-Beziehung und Durchflusszeitreihe ###

@author: Ellen Diez
"""

# =============================================================================
# 1. Einlesen der Daten
# =============================================================================

# Pakete importieren
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import matplotlib.dates as mdates
from sklearn.metrics import mean_squared_error
from scipy.optimize import curve_fit

# Kalibrierungsdaten einlesen, nach aufsteigendem Durchfluss sortieren und datetime-Spalte erstellen
df = pd.read_csv('MGB_hQ.csv', sep = '\t', decimal = ',', comment = '#')
df = df.sort_values(by = ['Q [m^3/s]'])
df['datetime'] = pd.to_datetime(df['Zeit'], format = '%d.%m.%Y %H:%M:%S')

# Gemessene Druck- und Luftdruckdaten einlesen und datetime-Zeitspalte erstellen
pw = pd.read_csv('MGB_Druck.csv', sep = ',', decimal = '.', comment = '#', parse_dates = ['Date/time'])
pw['datetime'] = pd.to_datetime(pw['Date/time'], format = '%d.%m.%Y %H:%M:%S')
pl = pd.read_csv('Luftdruck_Leven.csv', sep = ',', decimal = '.', comment = '#')
pl = pl.drop(columns = 'Temperatur[GradC]')
pl['datetime'] = pd.to_datetime(pl['Date/time'], format = '%Y/%m/%d %H:%M:%S')

# Druckdaten und Luftdruckdaten zuschneiden
start = '2025-08-04 00:00:00'
ende = '2025-08-12 23:59:00'
pw_cut = pw[pw['datetime'] >= start]
pl_cut = pl[pl['datetime'] >= start]
pw_cut = pw_cut[pw_cut['datetime'] <= ende]
pl_cut = pl_cut[pl_cut['datetime'] <= ende]

# Datetimespalte als Index setzen
pw_cut.set_index('datetime', inplace = True)
pl_cut.set_index('datetime', inplace = True)

# Fünfzehnminütige Druck- und Luftdruckdaten extrahieren
pw10 = pw_cut[pw_cut.index.minute % 15 == 0]
pl10 = pl_cut[pl_cut.index.minute % 15 == 0]

# Nettowasserstand bestimmen
hs = pd.DataFrame(pw10['Druck[cmH2O]'] - pl10['Druck[cmH2O]'])
hs['Wasserstand [mWs]'] = hs['Druck[cmH2O]']/100

#%% ===========================================================================
# 2. Lineare Regression
# =============================================================================

# 2.1 Annahme: exponentielles Verhalten (Potenzmodell) - Linearisierung und Regression

# numpy-Arrays der Wasserstände und Durchflüsse erstellen
h_numpy = df['h [m]'].values.reshape(-1, 1)
Q_numpy = df['Q [m^3/s]'].values.reshape(-1, 1)

# richtige Formatierung für Anwendung der linearen Regression
lnQ = np.log(df['Q [m^3/s]'])   # Logarithmierung
lnh = np.log(df['h [m]'])
lnQ = np.array(lnQ)             # series in Array umwandeln
lnh = np.array(lnh)
lnQ = lnQ.reshape(-1, 1)        # 1D-Array in 2D-Array umwandeln (für Funktion LinearRegression().fit)
lnh = lnh.reshape(-1, 1)

# Lineare Regression fitten
reg = LinearRegression().fit(lnh, lnQ)

# Paramter ausgeben lassen
lnc1 = reg.intercept_
c2 = reg.coef_
print(f'c2: {c2}')

# Parameter c1 bestimmen
c1 = np.exp(lnc1)
print(f'c1: {c1}')

# Kalibrationskurve mit Werten berechnen
def Q_kali_log(c1, c2, h):
    return c1*(h**c2)
h_reg = np.linspace(0.25, 0.36, 50).reshape(-1, 1)  # Modelleriungsbereich erstellen
Q_reg = Q_kali_log(c1, c2, h_reg)
lnh_reg = np.log(h_reg)
lnQ_reg = np.log(Q_reg)

# RMSE Fit mit Logarithmierung berechnen
Q_fit_log = Q_kali_log(c1, c2, h_numpy)             # gefittete Daten für diskrete Wasserstände berechnen
mse_log = mean_squared_error(Q_numpy, Q_fit_log)    # meansquareerror berechnen
rmse_log = np.sqrt(mse_log)                         # Wurzel ziehen
print(f'MSE_log: {mse_log}, RMSE_log: {rmse_log}\n')

# 2.2 Linearer Fit: Annahme lineares Verhalten, Regression ohne Liniearisierung

# Lineare Regression fitten
reg2 = LinearRegression().fit(h_numpy, Q_numpy)

# Parameter ausgeben lassen
a = reg2.intercept_
m = reg2.coef_
print(f'y-Achsenabschnitt: {a}')
print(f'Steigung: {m}')

# Linearen Fit berechnen
def Q_kali_linear(a, m, h):
    return m*h+a
Q_reg_linear = Q_kali_linear(a, m, h_reg)

# RMSE Fit linear berechnen
Q_fit_linear = Q_kali_linear(a, m, h_numpy)
mse_linear = mean_squared_error(Q_numpy, Q_fit_linear)
rmse_linear = np.sqrt(mse_linear)
print(f'MSE_lin: {mse_linear}, RMSE_lin: {rmse_linear}\n')

# 2.3 Fit mit Scypi_optimize curve_fit, Annahme Potenzgesetz

# Fitfunktion definieren
def Q_kali_curve(h, d1, d2):
    return d1*(h**d2)
startwerte = [1.0, 1.0]

# Fit durchführen
Q_numpy_flat= Q_numpy.flatten()
h_numpy_flat= h_numpy.flatten()
para, covar = curve_fit(Q_kali_curve, h_numpy_flat, Q_numpy_flat, p0 = startwerte)

# Gefittete Parameter ausgeben lassen, Fitwerte berechnen
d1, d2 = para
print(f'd1: {d1}, d2: {d2}')
Q_reg_curve = Q_kali_curve(h_reg, d1, d2)

# RMSE Fit mit curvefit berechnen
Q_fit_curve = Q_kali_curve(h_numpy, d1, d2)
mse_curve = mean_squared_error(Q_numpy, Q_fit_curve)
rmse_curve = np.sqrt(mse_curve)
print(f"MSE_curve: {mse_curve}, RMSE_curve: {rmse_curve}")

#%% ===========================================================================
# 3. h-Q-Beziehung plotten
# =============================================================================

# Abbildung mit Messwerten und Kalibrierkurve erstellen
df_Luk = df[df['Lukas'] == 1]   # ein Teil der Abflussmessungen wurde von Lukas Althoff durchgeführt
df_wir = df[df['Lukas'] == 0]
fig,ax = plt.subplots(2,1, figsize = (10,10))
ax[0].plot(df_Luk['Q [m^3/s]'], df_Luk['h [m]'], linestyle = 'none', marker = ('*'), color = 'red', markersize = '12', label = 'Messung L.Althoff')
ax[0].plot(df_wir['Q [m^3/s]'], df_wir['h [m]'], linestyle = 'none', marker = ('x'), markeredgecolor = 'red', markersize = '12', label = 'Messung')
ax[0].plot(Q_reg, h_reg, color = 'blue', label = 'Fit Potenzgesetz durch Linearisierung')
ax[0].plot(Q_reg_linear, h_reg, color = 'green', label = 'Fit linear')
ax[0].plot(Q_reg_curve, h_reg, color = 'orange', label = 'Fit Potenzgesetz durch curve_fit')
ax[0].set_title('h-Q-Beziehung MGB', fontsize = 25, pad = 12)
ax[0].set_xlabel('Durchfluss Q [$\mathrm{m^3\ s^{-1}}$]', fontsize = 18)
ax[0].set_ylabel('Wasserstand h [m]', fontsize = 18)
ax[0].legend(loc = 'best', fontsize = 12)
ax[0].grid()

# Linearisierte Abbildung mit Messwerten und Kalibriergerade (ln(Q)=ln(c1)+c2*ln(h))
lnQ_Luk = np.log(df_Luk['Q [m^3/s]'])
lnh_Luk = np.log(df_Luk['h [m]'])
lnQ_wir = np.log(df_wir['Q [m^3/s]'])
lnh_wir = np.log(df_wir['h [m]'])
ax[1].plot(lnQ_Luk, lnh_Luk, linestyle = 'none', marker = ('*'), color = 'red', markersize = '12', label = 'Messung L.Althoff')
ax[1].plot(lnQ_wir, lnh_wir, linestyle = 'none', marker = ('x'), markeredgecolor = 'red', markersize = '12', label = 'Messung')
ax[1].plot(lnQ_reg, lnh_reg, color = 'blue', label = 'Regression')
ax[1].set_title('Linearisierte h-Q-Beziehung MGB', fontsize = 25, pad = 12)
ax[1].set_xlabel('ln Q', fontsize = 18)
ax[1].set_ylabel('ln h', fontsize = 18)
ax[1].legend(loc = 'best', fontsize = 12)
ax[1].grid()

# Abstände der Plots festlegen
plt.subplots_adjust(wspace = 0.5, hspace = 0.5)

#%% ===========================================================================
# 4. Kontinuierliche Durchflusszeitreihe berechnen
# =============================================================================

# series-Objekt in numpyarray umwandeln
h_reihe = hs['Wasserstand [mWs]'].to_numpy()

# Durchflüsse berechnen mit linearem Fit (vgl. 2.2)
Q_reihe_linear = Q_kali_linear(a, m, h_reihe).reshape(-1, 1)
hs['Q_linear [m^3/s]'] = Q_reihe_linear

# Durchflüsse berechnen mit Potenzmodell durch Logarithmierung (vgl. 2.1)
Q_reihe_log = Q_kali_log(c1, c2, h_reihe).reshape(-1, 1)
hs['Q_log [m^3/s]'] = Q_reihe_log

# Durchflüsse berechnen mit Potenzmodell durch curve_fit (vgl. 2.3)
Q_reihe_curve = Q_kali_curve(h_reihe, d1, d2).reshape(-1, 1)
hs['Q_curve [m^3/s]'] = Q_reihe_curve

#%% ===========================================================================
# 5. Kontinuierliche Durchflusszeitreihe plotten
# =============================================================================

fig,ax = plt.subplots()
ax.plot(hs.index, hs['Q_linear [m^3/s]'], label = 'Lineares Modell')
ax.plot(hs.index, hs['Q_log [m^3/s]'], label = 'Potenzmodell durch Linearisierung')
ax.plot(hs.index, hs['Q_curve [m^3/s]'], label = 'Potenzmodell durch curve_fit')
#ax.set_title('Durchflusszeitreihe MGB', fontsize = 25, pad = 12)
ax.set_xlabel('Zeit', fontsize = 18)
ax.set_ylabel('Durchfluss Q [$\mathrm{m^3\ s^{-1}}$]', fontsize = 18)
ax.legend(loc = 'best', fontsize = 12)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
fig.autofmt_xdate()
ax.grid()

# Vertikale Linien für Messzeitpunkte erstellen
messzeitpunkte = pd.to_datetime(df_wir['Zeit'], format = '%d.%m.%Y %H:%M:%S')
ax.axvline(messzeitpunkte[0], color = 'red', linestyle = '--', label = 'Messzeitpunkte')
for i in range(len(messzeitpunkte)):
    ax.axvline(messzeitpunkte[i], color = 'red', linestyle = '--')

# Horizontale Linie für Unsicherheitsbereich erstellen
Q_max = df['Q [m^3/s]'].max()
Q_min = df['Q [m^3/s]'].min()
ax.axhline(Q_max, color = 'purple', linestyle = '-.', label = 'Wertebereich für Fit')
ax.axhline(Q_min, color = 'purple', linestyle = '-.')
ax.legend(loc = 'best')
#fig.savefig('H1_MGB_Qt', dpi = 300, bbox_inches = 'tight')

#%% ===========================================================================
# 6. Durchflusszeitreihe exportieren
# =============================================================================

hs = hs.drop(columns = 'Druck[cmH2O]')
hs.to_csv('MGB_Durchflusszeitreihe.csv', index = True)  # Index wird mit exportiert

#%% ===========================================================================
# 7. Unsicherheitsbetrachtung
# =============================================================================

# Unsicherheit von Q durch Parameterunsicherheit berechnen
def unsicher_param(h, d1, d2, covar):
    dQdp = np.array([[h**d2], [d1*np.log(h)*h**d2]])
    dQdp_T = np.array([h**d2, d1*np.log(h)*h**d2])
    return (dQdp_T@covar@dQdp)

# Leere Dataframe-Spalten erstellen und Index neu einrichten
hs['Unsicherheit Q_curve_param^2'] = None
hs['Unsicherheit Q_curve_h^2'] = None
hs['datetime'] = pd.to_datetime(hs.index, format = '%Y/%m/%d %H:%M:%S')
hs = hs.reset_index(drop = True)

for i in range(len(hs['Wasserstand [mWs]'])):
    h = hs['Wasserstand [mWs]'][i]
    hs.loc[i, 'Unsicherheit Q_curve_param^2'] = unsicher_param(h, d1, d2, covar)

# Unsicherheit von Q durch Unsicherheit der kontinuierlichen Wasserstände berechnen
ungenau_h = 0.003 # 3 mm Unsicherheit Wasserstand

def unsicher_h(d1, d2, ungenau_h, h):
    return ((d1**2)*(d2**2)*(h**(2*d2-2)) *(ungenau_h**2))   

for i in range(len(hs['Wasserstand [mWs]'])):
    h = hs['Wasserstand [mWs]'][i]
    hs.loc[i, 'Unsicherheit Q_curve_h^2'] = unsicher_h(d1, d2, ungenau_h, h)
    
# Ungenauigkeiten addieren
hs['Unsicherheit Q_curve'] = (hs['Unsicherheit Q_curve_param^2'] + hs['Unsicherheit Q_curve_h^2'])**(1/2)

#%% ===========================================================================
# 8. Durchfluss während Tracerversuchs mit Unsicherheit plotten
# =============================================================================

# Werte auf Tracerversuchszeiten zuschneiden
start_tracer = '2025-08-10 21:50'
ende_tracer = '2025-08-11 02:50'
hs_tracer = hs[hs['datetime'] >= start_tracer]
hs_tracer = hs_tracer[hs_tracer['datetime'] <= ende_tracer]

# Mittlerer Durchfluss Tracerversuch
Q_mean = hs_tracer['Q_curve [m^3/s]'].mean()
Q_unsicher_mean = hs_tracer['Unsicherheit Q_curve'].mean()
print(f'\nMittlerer Durchfluss: {Q_mean}; Mittlere Unsicherheit: {Q_unsicher_mean}')

# Plot erstellen
fig,ax = plt.subplots()
ax.plot(hs_tracer['datetime'], hs_tracer['Q_curve [m^3/s]'], color = 'green', label = 'Potenzmodell durch curve_fit')
ax.axhline(Q_mean, color = 'purple', linestyle = '-.', label = 'Mittelwert Durchfluss')
#ax.set_title('Unsicherheit Durchfluss M2 Tracerversuch', fontsize = 25, pad = 12)
ax.set_xlabel('Zeit', fontsize = 18)
ax.set_ylabel('Durchfluss Q [$\mathrm{m^3\ s^{-1}}$]', fontsize = 18)
ax.grid()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
fig.autofmt_xdate()

# Unsicherheit plotten
ax.errorbar(hs_tracer['datetime'], hs_tracer['Q_curve [m^3/s]'], yerr = hs_tracer['Unsicherheit Q_curve'], fmt = '.', alpha = 0.5, capsize = 2, label = 'Unsicherheit')

# Legende
ax.legend(loc = 'best')
