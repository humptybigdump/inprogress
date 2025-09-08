# -*- coding: utf-8 -*-
"""
Created on Thu Jul  3 17:20:51 2025

### M1: hv-Beziehung und Geschwindikeitszeitreihe ###

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

# Kalibrierungsdaten einlesen, nach aufsteigender Geschwindigkeit sortieren und datetime-Spalte erstellen
df = pd.read_csv('S1_hv.csv', sep = '\t', decimal = ',', comment = '#')
df = df.sort_values(by = ['v [m/s]'])
df['datetime'] = pd.to_datetime(df['Zeit'], format = '%d.%m.%Y %H:%M:%S')

# Gemessene Druck- und Luftdruckdaten einlesen und datetime-Zeitspalte erstellen
pw = pd.read_csv('S1_Druck.csv', sep = '\t', decimal = ',', comment = '#')
pw['datetime'] = pd.to_datetime(pw['Date/time'], format = '%d.%m.%Y %H:%M')
pl = pd.read_csv('Luftdruck.csv', sep = ',', decimal = '.')
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

# Zehnminütige Druck- und Luftdruckdaten extrahieren
pw10 = pw_cut[pw_cut.index.minute % 10 == 0]
pl10 = pl_cut[pl_cut.index.minute % 10 == 0]

# Nettowasserstand bestimmen
hs = pd.DataFrame(pw10['Druck[cmH2O]'] - pl10['Druck[cmH2O]'])
hs['Wasserstand [mWs]'] = hs['Druck[cmH2O]']/100

# Ausreißer entfernen - Auslesung der Logger
hs['Wasserstand [mWs]'].loc[hs.index == '2025-08-08 17:20:00'] = np.nan
hs['Wasserstand [mWs]'].loc[hs.index == '2025-08-08 17:30:00'] = np.nan

#%% Wasserstandsinformationen für gewünschten Zeitpunkt abrufen
info = hs.loc[hs.index == '2025-08-11 10:10:00']
print(info)
print('\n')

#%% ===========================================================================
# 2. Lineare Regression
# =============================================================================

# 2.1 Annahme: exponentielles Verhalten (Potenzmodell) - Linearisierung und Regression

# numpy-Arrays der Wasserstände und Geschwindigkeiten erstellen
h_numpy = df['h [m]'].values.reshape(-1, 1)
v_numpy = df['v [m/s]'].values.reshape(-1, 1)

# richtige Formatierung für Anwendung der linearen Regression
lnv = np.log(df['v [m/s]'])   # Logarithmierung
lnh = np.log(df['h [m]'])  
lnv = np.array(lnv)             # series in Array umwandeln  
lnh = np.array(lnh)
lnv = lnv.reshape(-1, 1)        # 1D-Array in 2D-Array umwandeln (für Funktion LinearRegression().fit)
lnh = lnh.reshape(-1, 1)

# Lineare Regression fitten
reg = LinearRegression().fit(lnh, lnv)

# Paramter ausgeben lassen
lnc1 = reg.intercept_
c2 = reg.coef_
print(f'c2: {c2}')

# Parameter c1 bestimmen
c1 = np.exp(lnc1)
print(f'c1: {c1}')

# Kalibrationskurve mit Werten berechnen
def v_kali_log(c1, c2, h):
    return c1*(h**c2)
h_reg = np.linspace(0.17, 0.2, 50).reshape(-1, 1)  # Modelleriungsbereich erstellen
v_reg = v_kali_log(c1, c2, h_reg)
lnh_reg = np.log(h_reg)
lnv_reg = np.log(v_reg)

# RMSE Fit mit Logarithmierung berechnen
v_fit_log = v_kali_log(c1, c2, h_numpy)             # gefittete Daten für diskrete Wasserstände berechnen
mse_log = mean_squared_error(v_numpy, v_fit_log)    # meansquareerror berechnen
rmse_log = np.sqrt(mse_log)                         # Wurzel ziehen
print(f'MSE_log: {mse_log}, RMSE_log: {rmse_log}\n')

# 2.2 Linearer Fit: Annahme lineares Verhalten, Regression ohne Liniearisierung

# Lineare Regression fitten
reg2 = LinearRegression().fit(h_numpy, v_numpy)

# Parameter ausgeben lassen
a = reg2.intercept_
m = reg2.coef_
print(f'y-Achsenabschnitt: {a}')
print(f'Steigung: {m}')

# Linearen Fit berechnen
def v_kali_linear(a, m, h):
    return m*h+a
v_reg_linear = v_kali_linear(a, m, h_reg)

# RMSE Fit linear berechnen
v_fit_linear = v_kali_linear(a, m, h_numpy)
mse_linear = mean_squared_error(v_numpy, v_fit_linear)
rmse_linear = np.sqrt(mse_linear)
print(f'MSE_lin: {mse_linear}, RMSE_lin: {rmse_linear}\n')

# 2.3 Fit mit Scypi_optimize curve_fit, Annahme Potenzgesetz

# Fitfunktion definieren
def v_kali_curve(h, d1, d2):
    return d1*(h**d2)
startwerte = [1.0, 1.0]

# Fit durchführen
v_numpy_flat= v_numpy.flatten()
h_numpy_flat= h_numpy.flatten()
para, covar = curve_fit(v_kali_curve, h_numpy_flat, v_numpy_flat, p0 = startwerte)

# Gefittete Parameter ausgeben lassen, Fitwerte berechnen
d1, d2 = para
print(f'd1: {d1}, d2: {d2}')
v_reg_curve = v_kali_curve(h_reg, d1, d2)

# RMSE Fit mit curvefit berechnen
v_fit_curve = v_kali_curve(h_numpy, d1, d2)
mse_curve = mean_squared_error(v_numpy, v_fit_curve)
rmse_curve = np.sqrt(mse_curve)
print(f'MSE_curve: {mse_curve}, RMSE_curve: {rmse_curve}')

#%% ===========================================================================
# 3. h-v-Beziehung plotten
# =============================================================================

# Abbildung mit Messwerten und Kalibrierkurve erstellen
df_Luk = df[df['Lukas'] == 1]   # ein Teil der Abflussmessungen wurde von Lukas Althoff durchgeführt
df_wir = df[df['Lukas'] == 0]
fig,ax = plt.subplots(2,1, figsize = (6.5,10))
#ax[0].plot(df_Luk['v [m/s]'], df_Luk['h [m]'], linestyle = 'none', marker = ('*'), color = 'red', markersize = '12', label = 'Messung L.Althoff')
ax[0].plot(df_wir['v [m/s]'], df_wir['h [m]'], linestyle = 'none', marker = ('x'), markeredgecolor = 'red', markersize = '12', label = 'Messung')
ax[0].plot(v_reg, h_reg, color = 'blue', label = 'Fit Potenzgesetz durch Linearisierung')
ax[0].plot(v_reg_linear, h_reg, color = 'green', label = 'Fit linear')
ax[0].plot(v_reg_curve, h_reg, color = 'orange', label = 'Fit Potenzgesetz durch curve_fit')
ax[0].set_title('h-v-Beziehung M1', fontsize = 25, pad = 12)
ax[0].set_xlabel('Geschwindigkeit v [$\mathrm{m\ s^{-1}}$]', fontsize = 18)
ax[0].set_ylabel('Wasserstand h [m]', fontsize = 18)
ax[0].legend(loc = 'best', fontsize = 12)
ax[0].grid()

# Linearisierte Abbildung mit Messwerten und Kalibriergerade (ln(v)=ln(c1)+c2*ln(h))
lnv_Luk = np.log(df_Luk['v [m/s]'])
lnh_Luk = np.log(df_Luk['h [m]'])
lnv_wir = np.log(df_wir['v [m/s]'])
lnh_wir = np.log(df_wir['h [m]'])
#ax[1].plot(lnv_Luk, lnh_Luk, linestyle = 'none', marker = ('*'), color = 'red', markersize = '12', label = 'Messung L.Althoff')
ax[1].plot(lnv_wir, lnh_wir, linestyle = 'none', marker = ('x'), markeredgecolor = 'red', markersize = '12', label = 'Messung')
ax[1].plot(lnv_reg, lnh_reg, color = 'blue', label = 'Regression')
ax[1].set_title('Linearisierte h-v-Beziehung M1', fontsize = 25, pad = 12)
ax[1].set_xlabel('ln v', fontsize = 18)
ax[1].set_ylabel('ln h', fontsize = 18)
ax[1].legend(loc = 'best', fontsize = 12)
ax[1].grid()

# Abstände der Plots festlegen
plt.subplots_adjust(wspace = 0.5, hspace = 0.5)

#%% ===========================================================================
# 4. Kontinuierliche Geschwindigkeitszeitreihe berechnen
# =============================================================================

# series-Objekt in numpyarray umwandeln
h_reihe = hs['Wasserstand [mWs]'].to_numpy()

# Geschwindigkeiten berechnen mit linearem Fit (vgl. 2.2)
v_reihe_linear = v_kali_linear(a, m, h_reihe).reshape(-1, 1)
hs['v_linear [m/s]'] = v_reihe_linear

# Geschwindigkeiten berechnen mit Potenzmodell durch Logarithmierung (vgl. 2.1)
v_reihe_log = v_kali_log(c1, c2, h_reihe).reshape(-1, 1)
hs['v_log [m/s]'] = v_reihe_log

# Geschwindigkeiten berechnen mit Potenzmodell durch curve_fit (vgl. 2.3)
v_reihe_curve = v_kali_curve(h_reihe, d1, d2).reshape(-1, 1)
hs['v_curve [m/s]'] = v_reihe_curve

#%% ===========================================================================
# 5. Kontinuierliche Geschwindigkeitszeitreihe plotten
# =============================================================================

fig,ax = plt.subplots()
ax.plot(hs.index, hs['v_linear [m/s]'], label = 'Lineares Modell')
ax.plot(hs.index, hs['v_log [m/s]'], label = 'Potenzmodell durch Linearisierung')
ax.plot(hs.index, hs['v_curve [m/s]'], label = 'Potenzmodell durch curve_fit')
#ax.set_title('Geschwindigkeitszeitreihe M1', fontsize = 25, pad = 12)
ax.set_xlabel('Zeit', fontsize = 18)
ax.set_ylabel('Geschwindigkeit v [$\mathrm{m\ s^{-1}}$]', fontsize = 16)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
fig.autofmt_xdate()
ax.grid()

# Vertikale Linien für Messzeitpunkte erstellen
messzeitpunkte = pd.to_datetime(df_wir['Zeit'], format = '%d.%m.%Y %H:%M:%S')
ax.axvline(messzeitpunkte[0], color = 'red', linestyle = '--', label = 'Messzeitpunkte')
for i in range(len(messzeitpunkte)):
    ax.axvline(messzeitpunkte[i], color = 'red', linestyle = '--')
    
# Horizontale Linie für Unsicherheitsbereich erstellen
v_max = df['v [m/s]'].max()
v_min = df['v [m/s]'].min()
ax.axhline(v_max, color = 'purple', linestyle = '-.', label = 'Wertebereich für Fit')
ax.axhline(v_min, color = 'purple', linestyle = '-.')
ax.legend(loc = 'best')

#%% ===========================================================================
# 6. Geschwindigkeitszeitreihe exportieren
# =============================================================================

hs = hs.drop(columns = ['Druck[cmH2O]'])
hs.to_csv('M1_Geschwindigkeitszeitreihe.csv', index = True) # Index wird mit exportiert

#%% ===========================================================================
# 7. Unsicherheitsbetrachtung
# =============================================================================

# Unsicherheit von v durch Parameterunsicherheit berechnen
def unsicher_param(h, d1, d2, covar):
    dvdp = np.array([[h**d2], [d1*np.log(h)*h**d2]])
    dvdp_T = np.array([h**d2, d1*np.log(h)*h**d2])
    return (dvdp_T@covar@dvdp)

# Leere Dataframe-Spalten erstellen und Index neu einrichten
hs['Unsicherheit v_curve_param^2'] = None
hs['Unsicherheit v_curve_h^2'] = None
hs['datetime'] = pd.to_datetime(hs.index, format = '%Y/%m/%d %H:%M:%S')
hs = hs.reset_index(drop = True)

for i in range(len(hs['Wasserstand [mWs]'])):
    h = hs['Wasserstand [mWs]'][i]
    hs.loc[i, 'Unsicherheit v_curve_param^2'] = unsicher_param(h, d1, d2, covar)

# Unsicherheit von v durch Unsicherheit der kontinuierlichen Wasserstände berechnen
ungenau_h = 0.003 # 3 mm Unsicherheit Wasserstand

def unsicher_h(d1, d2, ungenau_h, h):
    return ((d1**2)*(d2**2)*(h**(2*d2-2)) *(ungenau_h**2))   

for i in range(len(hs['Wasserstand [mWs]'])):
    h = hs['Wasserstand [mWs]'][i]
    hs.loc[i, 'Unsicherheit v_curve_h^2'] = unsicher_h(d1, d2, ungenau_h, h)
    
# Ungenauigkeiten addieren
hs['Unsicherheit v_curve'] = (hs['Unsicherheit v_curve_param^2'] + hs['Unsicherheit v_curve_h^2'])**(1/2)

#%% ===========================================================================
# 8. Durchfluss während Tracerversuchs mit Unsicherheit plotten
# =============================================================================

# Werte auf Tracerversuchszeiten zuschneiden
start_tracer = '2025-08-10 21:50'
ende_tracer = '2025-08-11 02:50'
hs_tracer = hs[hs['datetime'] >= start_tracer]
hs_tracer = hs_tracer[hs_tracer['datetime'] <= ende_tracer]

# Mittlere Geschwindigkeit Tracerversuch
v_mean = hs_tracer['v_curve [m/s]'].mean()
v_unsicher_mean = hs_tracer['Unsicherheit v_curve'].mean()
print(f'\nMittlere Geschwindigkeit: {v_mean}; Mittlere Unsicherheit: {v_unsicher_mean}')

# Plot erstellen
fig,ax = plt.subplots()
ax.plot(hs_tracer['datetime'], hs_tracer['v_curve [m/s]'], color = 'green', label = 'Potenzmodell durch curve_fit')
ax.axhline(v_mean, color = 'purple', linestyle = '-.', label = 'Mittelwert Geschwindigkeit')
#ax.set_title('Unsicherheit Geschwindigkeit M1 Tracerversuch', fontsize = 25, pad = 12)
ax.set_xlabel('Zeit', fontsize = 18)
ax.set_ylabel('Geschwindigkeit v [$\mathrm{m\ s^{-1}}$]', fontsize = 16)
ax.grid()
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
fig.autofmt_xdate()

# Unsicherheit plotten
ax.errorbar(hs_tracer['datetime'], hs_tracer['v_curve [m/s]'], yerr = hs_tracer['Unsicherheit v_curve'], fmt = '.', alpha = 0.5, capsize = 2, label = 'Unsicherheit')

# Legende
ax.legend(loc = 'best')


