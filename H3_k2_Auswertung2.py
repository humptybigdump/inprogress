#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from scipy.optimize import curve_fit
from scipy.stats import pearsonr
import matplotlib.dates as mdates
from datetime import datetime
import seaborn as sns

#Daten einlesen
df1 = pd.read_csv('./Hauptversuch/PropTracer_EchteDaten2.csv',comment='#')

Prop_Gas_Area= np.array(df1['Propan Gasphase in Area']) #Propan in der Gasphase bei Messung im Labor
df1['datetime'] = pd.to_datetime(df1['Datum'] + ' ' + df1['Uhrzeit'], format='%Y-%m-%d %I:%M:%S %p') #Datum und Uhrzeit in datetime-Format umwandeln
pd.set_option("display.float_format", "{:.2f}".format)
np.set_printoptions(precision=4)

#Massendifferenz voll-leer in g zu Volumen umrechnen und zu df1 hinzufügen
m_ges_g = np.array(df1['m_ges in g'])
m_leer_g = np.array(df1['m_leer_vial in g'])
m_W_g = m_ges_g - m_leer_g
#print("Massendifferenz leer-voll in g")
#print(m_W_g)

#Gramm zu Kilogramm
#Dichte von Wasser: 1000 kg/m³(Wiegen hat im Labor stattgefunden)
V_w_m3 = (m_W_g /1000)  / 1000
V_w_ml = (V_w_m3*1000000)
#zum Dataframe hinzufügen:
df1['m_Wasser in g'] = m_W_g.tolist()
df1['V_Wasser in ml'] = V_w_ml.tolist()
#print("df1:")
#print(df1)



# In[2]:


# Konzentration Propan in Wasser zum Entnahmezeitpunkt

#c_w_Area = (((V_w_m3/H_Prop)+V_g_m3)*Prop_Gas_Area)/V_w_m3
V_g_m3 = 0.00002-V_w_m3 #Volumen der Probengläsle: 20ml = 2E-5m³
V_g_ml = 20-V_w_ml #Volumen der Probengläsle: 20ml
#print("Gasvolumen" , '\n' , V_g_m3)
H_Prop = 26.893 #Einheitslose Henrykonstante Propan bei Raumtemperatur (298.15 K) (cg/cw)

c_w_Area1 = (((V_w_ml/H_Prop)+V_g_ml)*Prop_Gas_Area)/V_w_ml
#print("Propankonzentration im Wasser zum Entnahmezeitpunkt in Area (unverdünnt)" ,'\n', c_w_Area1)

## Verdünnung
Q_MS1_4 = np.array([0.28 , 0.291 , 0.311 , 0.354]) #Durchflussdaten von H2 [MS1 , MS2 , MS3 , MS4] in m³/s
Q_Verhältnisse = Q_MS1_4/Q_MS1_4[0]
Q_Verhältnisse_part1 = [Q_Verhältnisse[0]]*8
Q_Verhältnisse_part2 = [q for q in Q_Verhältnisse for _ in range(5)]
Q_Verhältnisse_expanded = Q_Verhältnisse_part1 + Q_Verhältnisse_part2 #Korrekturfaktor für jede Probe
#print(Q_Verhältnisse_expanded)

c_w_Area = c_w_Area1*Q_Verhältnisse_expanded
#print(c_w_Area)

#zum Dataframe hinzufügen
df1['V_Gas in ml'] = V_g_ml.tolist()
df1['c_w in Area (unverdünnt)'] = c_w_Area1.tolist()
df1['c_w in Area'] = c_w_Area.tolist()
print("df1:" , df1)


# In[8]:


#Daten in Abschnitte zusammenfassen
#Messtelle 1 (MS1)
df_MS1 =df1[['Glasnummer', 'datetime', 'V_Wasser in ml', 'Propan Gasphase in Area', 'c_w in Area' ]][8:13]
#print("df Messstelle 1", df_MS1)

#Messtelle 2 (MS2)
df_MS2 =df1[['Glasnummer', 'datetime', 'V_Wasser in ml' , 'Propan Gasphase in Area', 'c_w in Area']][13:18]
#print("df Messstelle 2" , df_MS2)

#Messtelle 3 (MS3)
df_MS3 =df1[['Glasnummer', 'datetime', 'V_Wasser in ml' , 'Propan Gasphase in Area', 'c_w in Area']][18:23]
#print("df Messstelle 3" , df_MS3)

#Messtelle 4 (MS4)
df_MS4 =df1[['Glasnummer', 'datetime', 'V_Wasser in ml' , 'Propan Gasphase in Area', 'c_w in Area']][23:28]
#print("df Messstelle 4" , df_MS4)


# In[4]:


#Mittelwerte der Propankonzetrationen der Messreihen
MS1_c_w_Area_mean = np.mean(c_w_Area[8:13])
MS2_c_w_Area_mean = np.mean(c_w_Area[13:18])
MS3_c_w_Area_mean = np.mean(c_w_Area[18:23])
MS4_c_w_Area_mean = np.mean(c_w_Area[23:28])

#Standardabweichungen berechnen
MS1_c_w_Area_std = np.std(c_w_Area[8:13])
MS2_c_w_Area_std = np.std(c_w_Area[13:18])
MS3_c_w_Area_std = np.std(c_w_Area[18:23])
MS4_c_w_Area_std = np.std(c_w_Area[23:28])
#relativer Fehler
MS1_c_w_Area_Fehler_Prozent = (MS1_c_w_Area_std / MS1_c_w_Area_mean)*100
MS2_c_w_Area_Fehler_Prozent = (MS2_c_w_Area_std / MS2_c_w_Area_mean)*100
MS3_c_w_Area_Fehler_Prozent = (MS3_c_w_Area_std / MS3_c_w_Area_mean)*100
MS4_c_w_Area_Fehler_Prozent = (MS4_c_w_Area_std / MS4_c_w_Area_mean)*100

#Anteilige Unetrschiede zur Maximalkonzentration
MS1_1_Verhaeltnis =  MS1_c_w_Area_mean / MS1_c_w_Area_mean
MS2_1_Verhaeltnis =  MS2_c_w_Area_mean / MS1_c_w_Area_mean
MS3_1_Verhaeltnis =  MS3_c_w_Area_mean / MS1_c_w_Area_mean
MS4_1_Verhaeltnis =  MS4_c_w_Area_mean / MS1_c_w_Area_mean

print("Mittelwerte der Propankonzentrationen an den Messstellen:")
print(f"MS1: {MS1_c_w_Area_mean:.3f} (± {MS1_c_w_Area_Fehler_Prozent:.2f}%), Verhältnis zu MS1: {MS1_1_Verhaeltnis:.2f}")
print(f"MS2: {MS2_c_w_Area_mean:.3f} (± {MS2_c_w_Area_Fehler_Prozent:.2f}%), Verhältnis zu MS1: {MS2_1_Verhaeltnis:.2f}")
print(f"MS3: {MS3_c_w_Area_mean:.3f} (± {MS3_c_w_Area_Fehler_Prozent:.2f}%), Verhältnis zu MS1: {MS3_1_Verhaeltnis:.2f}")
print(f"MS4: {MS4_c_w_Area_mean:.3f} (± {MS4_c_w_Area_Fehler_Prozent:.2f}%), Verhältnis zu MS1: {MS4_1_Verhaeltnis:.2f}")


# In[9]:


#Gasaustauschkoeffizient in 1/Zeit für die drei Messabschnitte berechnen (Referenz von Knapps Paper: 50-70/Tag)

#Fließzeit tau von H2 (in Minuten) [0 , MS1-2 , MS2-3 , MS3-4]
tau = np.array([0 , 58.54 , 73.65 , 55.46]) # in Minuten zwischen den Messstellen
tau_min_std = np.array([0 , 5.57 , 5.91 , 10.07]) #Standardabweichung von tau, Daten von H2

Einheit_tau = "Minute"
tau_s = np.array(tau*60)

tau_kumuliert = np.cumsum(tau)
#print("tau_kumuliert in", Einheit_tau, tau_kumuliert)

#Gasaustauschkoeffizient Propan in 1/ZEit
k2_MS1_2_Prop = np.log(MS1_c_w_Area_mean /MS2_c_w_Area_mean) / tau[1]
k2_MS2_3_Prop = np.log(MS2_c_w_Area_mean /MS3_c_w_Area_mean) / tau[2]
k2_MS3_4_Prop = np.log(MS3_c_w_Area_mean /MS4_c_w_Area_mean) / tau[3]


#Fehlerfortpflanzung k2 (Unsicherheiten von Konzentrationen und Fließzeit(h2))

#partielle Ableitungen: 
#dk2_dcup = 1/(cup*tau)
#dk2_dcdown = -1/(cdown*tau)
#dk2_dtau = -(ln(cup/cdown))/tau^2

#hier erstmal für Propan und ohne Temperatureinfluss
#MS1 bis MS2
delta_k2_MS1_2 = np.sqrt( (((1/(MS1_c_w_Area_mean*tau[1]))*MS1_c_w_Area_std)**2) + 
                         (((-1/(MS2_c_w_Area_mean*tau[1]))*MS2_c_w_Area_std)**2) + 
                         ((((-np.log(MS1_c_w_Area_mean/MS2_c_w_Area_mean))/(tau[1]**2))*tau_min_std[1])**2) )
#MS2 bis MS3
delta_k2_MS2_3 = np.sqrt( (((1/(MS2_c_w_Area_mean*tau[2]))*MS2_c_w_Area_std)**2) + 
                         (((-1/(MS3_c_w_Area_mean*tau[2]))*MS3_c_w_Area_std)**2) + 
                         ((((-np.log(MS2_c_w_Area_mean/MS3_c_w_Area_mean))/(tau[2]**2))*tau_min_std[2])**2) )
#MS3 bis MS4
delta_k2_MS3_4 = np.sqrt( (((1/(MS3_c_w_Area_mean*tau[3]))*MS3_c_w_Area_std)**2) + 
                         (((-1/(MS4_c_w_Area_mean*tau[3]))*MS4_c_w_Area_std)**2) + 
                         ((((-np.log(MS3_c_w_Area_mean/MS4_c_w_Area_mean))/(tau[3]**2))*tau_min_std[3])**2) )

print()
print(f"Gasaustauschkoeffizienten Propan in EINHEIT 1/ {Einheit_tau} ")
print(f"MS1-MS2 {k2_MS1_2_Prop:.4f} (+- {delta_k2_MS1_2:.4f} )")
print(f"MS2-MS3 {k2_MS2_3_Prop:.4f} (+- {delta_k2_MS2_3:.4f} )")
print(f"MS3-MS4 {k2_MS3_4_Prop:.4f} (+- {delta_k2_MS3_4:.4f} )")


#Gasaustauschkoeffizient Sauerstoff in 1/Zeit
k2_MS1_2_O2 = k2_MS1_2_Prop * 1.39 #aus Julia Knapps Paper
k2_MS2_3_O2 = k2_MS2_3_Prop * 1.39
k2_MS3_4_O2 = k2_MS3_4_Prop * 1.39

#abs Fehler skaliert mit
delta_k2_MS1_2_O2 = delta_k2_MS1_2 * 1.39 #aus Julia Knapps Paper
delta_k2_MS2_3_O2 = delta_k2_MS2_3 * 1.39
delta_k2_MS3_4_O2 = delta_k2_MS3_4 * 1.39

print()
print(f"Gasaustauschkoeffizienten Sauerstoff in EINHEIT 1/ {Einheit_tau}")
print(f"MS1-MS2 {k2_MS1_2_O2:.4f} (+-{delta_k2_MS1_2_O2:.4f})")
print(f"MS2-MS3 {k2_MS2_3_O2:.4f} (+-{delta_k2_MS2_3_O2:.4f})")
print(f"MS3-MS4 {k2_MS3_4_O2:.4f} (+-{delta_k2_MS3_4_O2:.4f})")


#Temperaturkorrektur auf 20°C unter Annahme, dass T= konst an jeder Messstelle während des Experiments
#aus dem anderen Code: mittlere Temperaturen über den Zeitraum des Tracerversuchs in jedem Messabschnitt
TemperaturMS1_2_mean = 17.544 # in °C
TemperaturMS2_3_mean = 17.742 
TemperaturMS3_4_mean = 18.013

TemperaturMS1_2_std  = 0.320
TemperaturMS2_3_std  = 0.348
TemperaturMS3_4_std  = 0.455
#laut Knapp: k2_T = k2_20Grad * 1.0241^(T-20°C) deshalb ist k2_20Grad = k2_T /1.0241^(T-20°C)

k2_MS1_2_O2_20Grad = k2_MS1_2_O2 / (1.0241**(TemperaturMS1_2_mean-20))
k2_MS2_3_O2_20Grad = k2_MS2_3_O2 / (1.0241**(TemperaturMS2_3_mean-20))
k2_MS3_4_O2_20Grad = k2_MS3_4_O2 / (1.0241**(TemperaturMS3_4_mean-20))


#Fehlerfortpflanzung mit fehlerfortgepflanzter Unsicherheit von k2 und der Temperatur
#partielle Ableitungen: 
#dk2(20)/dk2(T) = 1,0241^(20°C-T)
#dk2(20)/dT = 0.0383*k2(T) * exp(-0.0238 T)

delta_k2_MS1_2_20Grad = np.sqrt( ((((1.0241**(20-TemperaturMS1_2_mean))*delta_k2_MS1_2_O2)**2) + 
                         (((0.0383*k2_MS1_2_O2*np.exp(-0.0238*TemperaturMS1_2_mean))*TemperaturMS1_2_std)**2)))
delta_k2_MS2_3_20Grad = np.sqrt( ((((1.0241**(20-TemperaturMS2_3_mean))*delta_k2_MS2_3_O2)**2) + 
                         (((0.0383*k2_MS2_3_O2*np.exp(-0.0238*TemperaturMS2_3_mean))*TemperaturMS2_3_std)**2)))
delta_k2_MS3_4_20Grad = np.sqrt( ((((1.0241**(20-TemperaturMS3_4_mean))*delta_k2_MS3_4_O2)**2) + 
                         (((0.0383*k2_MS3_4_O2*np.exp(-0.0238*TemperaturMS3_4_mean))*TemperaturMS3_4_std)**2)))



print()
print("Korrigiert auf 20 Grad in 1/", Einheit_tau)
print(f"MS1-MS2 {k2_MS1_2_O2_20Grad:.4f} (+-{delta_k2_MS1_2_20Grad:.4f})")
print(f"MS2-MS3 {k2_MS2_3_O2_20Grad:.4f} (+-{delta_k2_MS2_3_20Grad:.4f})")
print(f"MS3-MS4 {k2_MS3_4_O2_20Grad:.4f} (+-{delta_k2_MS3_4_20Grad:.4f})")



# In[ ]:





# In[10]:


#k2 mit O'Connor/Dobbins: k2 = (sqrt(D_m * v)/h^1.5)
D_m2_pro_s = 2.1E-9 #molekularer Diffusionskoeffizient von Sauerstoff in Wasser bei 20°C
x_m = np.array([0, 1325.1 , 1713.9 , 994.9]) #Abstände zwischen den Messstellen von H2
v_mean_m_pro_s = x_m[1:4] / tau_s[1:4]
#print(v_mean_m_pro_s)
h_mean_Abschnitte_m = np.array([0.48,0.46,0.41]) #Daten der Modellierungsgruppe

k2_OCD_pro_sek = (np.sqrt(D_m2_pro_s * v_mean_m_pro_s))/(h_mean_Abschnitte_m**1.5)
k2_OCD_pro_min = k2_OCD_pro_sek*60
print("Gasaustauschkoeffizient Sauerstoff von O'Connor und Dobbins(isotrope Turbulenz) in 1/Minute")
print(f"MS1-MS2 {k2_OCD_pro_min[0]:.4f}")
print(f"MS2-MS3 {k2_OCD_pro_min[1]:.4f}")
print(f"MS3-MS4 {k2_OCD_pro_min[2]:.4f}")


# In[16]:


#nette Graphiken: Konzentrationen an den Messstellen und Uhrzeit
#plot 1
fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.semilogy(df1['datetime'][1:8], df1['c_w in Area'][1:8], color='#ADA3A3', linestyle = 'None',marker='o', label='Zeitreihe an MS1')
ax1.semilogy(df_MS1['datetime'], df_MS1['c_w in Area'], color='blue', linestyle = 'None',marker='x', label='M1')
ax1.semilogy(df_MS2['datetime'], df_MS2['c_w in Area'], color='#F58514', linestyle = 'None',marker='x', label='M2')
ax1.semilogy(df_MS3['datetime'], df_MS3['c_w in Area'], color='#00A37A', linestyle = 'None',marker='x', label='M3')
ax1.semilogy(df_MS4['datetime'], df_MS4['c_w in Area'], color='#FF5CE2', linestyle = 'None',marker='x', label='M4')

ax1.set_ylabel("Propankonzentration im Wasser in Area",fontsize=14)
ax1.set_xlabel("Uhrzeit", fontsize=14)
plt.xticks(rotation=45)
ax1.xaxis.set_major_locator(mdates.MinuteLocator(interval=15))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

ax1.grid(True, color='#d6d6d6', which='both', linestyle='-', linewidth=0.7, alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()


#%%plot2 mit tau kumuliert und neuem Dataframe
#verdünnt, aber für Propan
import statsmodels.api as sm

#Dataframe erstellen, der der Konzentration jeder Messstelle die richtige Fließzeit zuordnet
tau_kumuliert_expanded = [t for t in tau_kumuliert for _ in range(5)]
tau_kumuliert_array = np.array(tau_kumuliert_expanded) 
c_w_Area_Messstellen_log1 = np.log(c_w_Area[8:28])
df3 = pd.DataFrame({'tau': tau_kumuliert_expanded, 'log(c_w in Area)': c_w_Area_Messstellen_log1})
print(df3)

#%%Abschnitt MS1_2
#regressionsgerade 1_2
tau_kumuliert_array1 = sm.add_constant(tau_kumuliert_array[0:10])
linear_model1 = sm.OLS(c_w_Area_Messstellen_log1[0:10], tau_kumuliert_array1)
results1 = linear_model1.fit()
results1.params

tau_min1, tau_max1 = tau_kumuliert_array1.min(), tau_kumuliert_array1.max()
tau_plot1 = np.linspace(tau_min1, tau_max1,100)
c_w_reg1=results1.params[0] + results1.params[1]*tau_plot1  #Geradengleichung

#Unsicherheit der Gerade 1_2
p1, cov1 = np.polyfit(tau_kumuliert_array[0:10],c_w_Area_Messstellen_log1[0:10], 1, cov=True)   # p = [m, b]
m, b = p1
m_err1, b_err1 = np.sqrt(np.diag(cov1))     # Standardfehler von m und b
m_err1_rel = (-m_err1/m)*100                     #relativer Fehler in Prozent
print()
print(f"MS1_2: y = ({m:.4f} ± {m_err1:.5f})x + ({b:.5f} ± {b_err1:.5f})")
print(f"      relativer Fehler der Steigung (k2): {m_err1_rel:.3f}%")

#Konfidenzband 1-2
tau_plot1_exog = sm.add_constant(tau_plot1)
pred = results1.get_prediction(tau_plot1_exog)
conf_int = pred.conf_int(alpha=0.05)
pred_int = pred.conf_int(obs=True, alpha=0.05)


#%%Abschnitt MS2_3
#regressionsgerade 2_3
tau_kumuliert_array2 = sm.add_constant(tau_kumuliert_array[5:15])
linear_model2 = sm.OLS(c_w_Area_Messstellen_log1[5:15], tau_kumuliert_array2)
results2 =linear_model2.fit()
results2.params

tau_min2, tau_max2 = tau_kumuliert_array2.min(), tau_kumuliert_array2.max()
tau_plot2 = np.linspace(tau_min2, tau_max2,100)
x_fit2 = np.linspace(50, 140, 100)
c_w_reg2=results2.params[0] + results2.params[1]*x_fit2  #Geradengleichung

#Unsicherheit der Gerade 2_3
p2, cov2 = np.polyfit(tau_kumuliert_array[5:15],c_w_Area_Messstellen_log1[5:15], 1, cov=True)   # p = [m, b]
m2, b2 = p2
m2_err, b2_err = np.sqrt(np.diag(cov2))     # Standardfehler von m und b
m_err2_rel = (-m2_err/m2)*100                     #relativer Fehler in Prozent
print(f"MS2_3: y = ({m2:.4f} ± {m2_err:.5f})x + ({b2:.5f} ± {b2_err:.5f})")
print(f"      relativer Fehler der Steigung (k2): {m_err2_rel:.3f}%")

#Konfidenzintervall 
x_fit2_exog = sm.add_constant(x_fit2)
pred2 = results2.get_prediction(x_fit2_exog)
conf_int2=pred2.conf_int(alpha=0.05)
pred_int2=pred2.conf_int(obs=True, alpha=0.05)


#%%Abschnitt 3_4
tau_kumuliert_array3 = sm.add_constant(tau_kumuliert_array[10:20])
linear_model3 = sm.OLS(c_w_Area_Messstellen_log1[10:20], tau_kumuliert_array3)
results3 =linear_model3.fit()
results3.params

tau_min3, tau_max3 = tau_kumuliert_array3.min(), tau_kumuliert_array3.max()
#print(tau_min3, tau_max3)
tau_plot3 = np.linspace(tau_min3, tau_max3,100)
x_fit3 = np.linspace(120, 200, 100)
c_w_reg3=results3.params[0] + results3.params[1]*x_fit3 #Geradengleichung

#Unsicherheit der Gerade 3_4
p3, cov3 = np.polyfit(tau_kumuliert_array[10:20],c_w_Area_Messstellen_log1[10:20], 1, cov=True)   # p = [m, b]
m3, b3 = p3
m3_err, b3_err = np.sqrt(np.diag(cov3))     # Standardfehler von m und b
print(f"MS3_4: y = ({m3:.4f} ± {m3_err:.5f})x + ({b3:.5f} ± {b3_err:.5f})")
m_err3_rel = (-m3_err/m3)*100                     #relativer Fehler in Prozent
print(f"      relativer Fehler der Steigung (k2): {m_err3_rel:.3f}%")

#Konfidenzband
x_fit3_exog = sm.add_constant(x_fit3)
pred3 = results3.get_prediction(x_fit3_exog)
conf_int3=pred3.conf_int(alpha=0.05)
pred_int3=pred3.conf_int(obs=True, alpha=0.05)


#%% Formatieren
#Plot allgemein erstellen
fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(tau_plot1, c_w_reg1, color='black', ls='-',lw=1, label='Gasaustauschkoeffizient')
ax1.plot(tau_plot1, conf_int[:,0], color='#668B8B', ls='--', lw=1, label='Konfidenzintervall')
ax1.plot(tau_plot1, conf_int[:,1], color='#668B8B', ls='--', lw=1)

ax1.plot(x_fit2, c_w_reg2, color='black', ls='-',lw=1)
ax1.plot(x_fit2, conf_int2[:,0], color='#668B8B', ls='--', lw=1)
ax1.plot(x_fit2, conf_int2[:,1], color='#668B8B', ls='--', lw=1)

ax1.plot(x_fit3, c_w_reg3, color='black', ls='-',lw=1)
ax1.plot(x_fit3, conf_int3[:,0], color='#668B8B', ls='--', lw=1)
ax1.plot(x_fit3, conf_int3[:,1], color='#668B8B', ls='--', lw=1)

ax1.plot(df3['tau'][0:5], df3['log(c_w in Area)'][0:5], color='blue', linestyle = 'None',marker='x', label='M1')
ax1.plot(df3['tau'][5:10], df3['log(c_w in Area)'][5:10], color='#F58514', linestyle = 'None',marker='x', label='M2')
ax1.plot(df3['tau'][10:15], df3['log(c_w in Area)'][10:15], color='#00A37A', linestyle = 'None',marker='x', label='M3')
ax1.plot(df3['tau'][15:20], df3['log(c_w in Area)'][15:20], color='#FF5CE2', linestyle = 'None',marker='x', label='M4')
ax1.set_ylabel("log(Propankonzentration im Wasser in Area)",fontsize=12)
ax1.set_xlabel("Fließzeit ab MS1", fontsize=12)
ax1.grid(True, color='#d6d6d6', which='both', linestyle='-', linewidth=0.7, alpha=0.7)

#Geradeengleichungen unten links einfügen
Gleichungen_text = (
    fr"Geradengleichungen:" + "\n"
    fr"M1-M2: $y = ({m:.3f} \pm {m_err1:.4f})x + ({b:.2f} \pm {b_err1:.2f})$" + "\n"
    fr"M2-M3: $y = ({m2:.3f} \pm {m2_err:.4f})x + ({b2:.2f} \pm {b2_err:.2f})$" + "\n"
    fr"M3-M4: $y = ({m3:.3f} \pm {m3_err:.4f})x + ({b3:.2f} \pm {b3_err:.2f})$" 
    )

ax1.text(
    0.02, 0.02, Gleichungen_text, 
    transform=ax1.transAxes, #nach links unten
    fontsize=10,
    verticalalignment='bottom',
    horizontalalignment='left',
    bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="black", alpha=0.8)
    )


ax1.legend()
plt.show()


#%%
#auf Sauerstoff umrechnen
m_O2 = np.array(-m *1.39)
m2_O2 = np.array(-m2 *1.39)
m3_O2 = np.array(-m3 *1.39)

m_err1_O2 = m_err1*1.39 
m2_err_O2 = m2_err*1.39
m3_err_O2 = m3_err*1.39

print(f"MS1-MS2, k2 für Sauerstoff: {m_O2:.3f} (+-{m_err1_O2:.4f}) pro Minute")
print(f"MS2-MS3, k2 für Sauerstoff: {m2_O2:.3f} (+-{m2_err_O2:.4f}) pro Minute")
print(f"MS3-MS4, k2 für Sauerstoff: {m3_O2:.3f} (+-{m3_err_O2:.4f}) pro Minute")


#Temperaturkorrektur
m_O2_20Grad = m2_O2 / (1.0241**(TemperaturMS1_2_mean-20))
m2_O2_20Grad = m2_O2 / (1.0241**(TemperaturMS2_3_mean-20))
m3_O2_20Grad = m3_O2 / (1.0241**(TemperaturMS3_4_mean-20))

#Fehlerfortpflanzung analog zur Berechnung mit den Mittelwerten
#mit fehlerfortgepflanzter Unsicherheit von k2 und der Temperatur
#partielle Ableitungen: 
#dk2(20)/dk2(T) = 1,0241^(20°C-T)
#dk2(20)/dT = 0.0383*k2(T) * exp(-0.0238 T)

#MS1-MS2
delta_m_20Grad = np.sqrt( ((((1.0241**(20-TemperaturMS1_2_mean))*m_err1_O2)**2) + 
                         (((0.0383*m_O2*np.exp(-0.0238*TemperaturMS1_2_mean))*TemperaturMS1_2_std)**2)))
#MS2-MS3
delta_m2_20Grad = np.sqrt( ((((1.0241**(20-TemperaturMS2_3_mean))*m2_err_O2)**2) + 
                         (((0.0383*m2_O2*np.exp(-0.0238*TemperaturMS2_3_mean))*TemperaturMS2_3_std)**2)))
delta_m3_20Grad = np.sqrt( ((((1.0241**(20-TemperaturMS3_4_mean))*m3_err_O2)**2) + 
                         (((0.0383*m3_O2*np.exp(-0.0238*TemperaturMS3_4_mean))*TemperaturMS3_4_std)**2)))

print(f"MS1-MS2, k2 temperaturkorrigiert: {m_O2_20Grad:.3f}(+-{delta_m_20Grad:.4f}) pro Minute")
print(f"MS2-MS3, k2 temperaturkorrigiert: {m2_O2_20Grad:.3f}(+-{delta_m2_20Grad:.4f}) pro Minute")
print(f"MS3-MS4, k2 temperaturkorrigiert: {m3_O2_20Grad:.3f}(+-{delta_m3_20Grad:.4f}) pro Minute")


# In[ ]:





# In[21]:


#Zeitreihe: nette Graphik über Zeit

#eigenen Dataframe mit Zeitreihe
df_Z = df1[['Glasnummer' , 'datetime', 'V_Wasser in ml', 'Propan Gasphase in Area', 'c_w in Area']][1:8]
#Mittelwert der Messreihe nach Uranin-Peak an MS1 als zusätzlicher Punkt der Zeitreihe
UhrzeitextraZeile = pd.to_datetime("2025-08-10 10:59:00 PM")
M1_extraZeile = pd.DataFrame([{'Glasnummer':'1x' , 'datetime':UhrzeitextraZeile, 'V_Wasser in ml':'xx', 'Propan Gasphase in Area':'xx', 'c_w in Area':MS1_c_w_Area_mean}])
df_Z = pd.concat([M1_extraZeile, df_Z])
print("df Zeitreihe")
print(df_Z)


#Mittelwert und Standardabweichung ohne Außreißer (die letzten drei Punkte)
c_w_Area_Zeitreihe = np.concatenate([c_w_Area[1:5], [MS1_c_w_Area_mean]]) #Mittelwert von MS1 auch als Punkt der Zeitreihe
c_w_Area_Zeitreihe_mean = np.mean(c_w_Area_Zeitreihe)
c_w_Area_Zeitreihe_std = np.std(c_w_Area_Zeitreihe)
c_w_Area_Zeitreihe_Fehler_Prozent = (c_w_Area_Zeitreihe_std/c_w_Area_Zeitreihe_mean)*100
print()
print(f"Zeitreihe Mittelwert und relative Abweichung: {c_w_Area_Zeitreihe_mean:.3f} (± {c_w_Area_Zeitreihe_Fehler_Prozent:.3f}%)")



#Diagramm c_w über Zeit mit allen Werten
fig, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(df_Z['datetime'], df_Z['c_w in Area'], color='blue', linestyle = 'None',marker='o', label='Propan')
ax1.set_ylabel("Propankonzentration im Wasser in Area",fontsize=17)
plt.xticks(rotation=45)
ax1.xaxis.set_major_locator(mdates.MinuteLocator(interval=15))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
ax1.grid(True)
ax1.set_xlabel("Uhrzeit", fontsize=17)


#Regression ohne Ausreißer (die letzten drei Punkte)
zeit = df_Z['datetime'][0:5]
Zeitreihe = df_Z['c_w in Area'][0:5]
zeit_dt = pd.to_datetime(zeit, format='%I:%M:%S %p')
zeit_num = mdates.date2num(zeit_dt)
linear_regression = np.polyfit(zeit_num, Zeitreihe,deg=1)
line = np.poly1d(linear_regression)
ax1.plot(zeit_dt, line(zeit_num), color='black', label='Regression')

plt.show()



# In[ ]:





# In[44]:


#Hypothese: Füllvolumen verändert Konzentrationsmessung mehr als durch die Umrechnung mit dem Henrygesetz bereinigt wird
#daher: Korrelation von Füllvolumen zu KOnzentration im Wasser

#erstmal an MS1, da dort besonders viele Daten erhoben wurden und bei der Probennahme weniger stark auf die genau Volumengleichheit geachtet wurde
df_MS1_ges = pd.concat([df_Z[1:6], df_MS1], ignore_index=True) #nur Werte, als noch Propan vorhanden war
print("df_MS1_ges" , df_MS1_ges)


#erstmal scatterplot
fig, ax1 = plt.subplots(2,2,figsize=(7, 4))
ax1[0,0].plot(df_Z['V_Wasser in ml'][1:6], df_Z['c_w in Area'][1:6], color='orange', linestyle = 'None',marker='o', label='Volumen gegen c_w')
ax1[0,0].plot(df_MS1['V_Wasser in ml'], df_MS1['c_w in Area'], color='red', linestyle = 'None',marker='o', label='Volumen gegen c_w')
fig.supylabel("Propankonzentration im Wasser in Area",fontsize=10)
fig.supxlabel("Wasservolumen im Headspace-Vial in ml", fontsize=10)
plt.xticks(rotation=45)
ax1[0,0].grid(True)
ax1[0,0].set_title("MS1")
fig.suptitle("Zusammenhang Probenvolumen und Propankonzentration")
#Korrelation (Pearson)
r, p_value = pearsonr(df_MS1_ges['V_Wasser in ml'], df_MS1_ges['c_w in Area'])
print(f"Pearson-Korrelationskoeffizient MS1: {r:.4f}")
print(f"P-Wert: {p_value:.4f}")

#Messstelle2
#scatterplot
ax1[0,1].plot(df_MS2['V_Wasser in ml'], df_MS2['c_w in Area'], color='red', linestyle = 'None',marker='o', label='Volumen gegen c_w')
ax1[0,1].grid(True)
ax1[0,1].set_title("MS2")
#Korrelation (Pearson)
r2, p_value2 = pearsonr(df_MS2['V_Wasser in ml'], df_MS2['c_w in Area'])
print()
print(f"Pearson-Korrelationskoeffizient MS2: {r2:.3f}")
print(f"P-Wert: {p_value2:.3f}")


#Messstelle 3
ax1[1,0].plot(df_MS3['V_Wasser in ml'], df_MS3['c_w in Area'], color='red', linestyle = 'None',marker='o', label='Volumen gegen c_w')
ax1[1,0].grid(True)
ax1[1,0].set_title("MS3")
#Korrelation (Pearson)
r3, p_value3 = pearsonr(df_MS3['V_Wasser in ml'], df_MS3['c_w in Area'])
print()
print(f"Pearson-Korrelationskoeffizient MS3: {r3:.3f}")
print(f"P-Wert: {p_value3:.3f}")


#Messstelle 4
ax1[1,1].plot(df_MS4['V_Wasser in ml'], df_MS4['c_w in Area'], color='red', linestyle = 'None',marker='o', label='Volumen gegen c_w')
ax1[1,1].grid(True)
ax1[1,1].set_title("MS4")
#Korrelation (Pearson)
r4, p_value4 = pearsonr(df_MS4['V_Wasser in ml'], df_MS4['c_w in Area'])
print()
print(f"Pearson-Korrelationskoeffizient MS4: {r4:.3f}")
print(f"P-Wert: {p_value4:.3f}")


plt.tight_layout()
plt.show()


# In[ ]:





# In[ ]:





# In[7]:


# Korrekturfaktor laut Hypothese

V_sample = 0.5
korr = (df1['V_Gas in ml']-V_sample)/df1['V_Gas in ml'] #Korrekturfaktor

df1['korr'] = korr.tolist()
#print("Korrekturaktor für c_w" , df1['korr'])
c_w_Area_korr = (df1['c_w in Area']/korr)
df1['c_w_Area_korr'] = c_w_Area_korr.tolist()

#Mittelwert und Standardabweichung Zeitreihe inklusive Max-Ausreißer
c_w_Area_Zeitreihe_mean2 = np.mean(c_w_Area[1:6])
c_w_Area_Zeitreihe_std2 = np.std(c_w_Area[1:6])
c_w_Area_Zeitreihe_Fehler_Prozent2 = (c_w_Area_Zeitreihe_std2/c_w_Area_Zeitreihe_mean2)*100
print()
print(f"(nicht korrigiert):Zeitreihe-Mittelwert und rel. Abw. mit Max-Ausreißer: {c_w_Area_Zeitreihe_mean2:.3f} (± {c_w_Area_Zeitreihe_Fehler_Prozent2:.3f}%)")


# Mittelwerte der Propankonzetrationen der Messreihen
Zeitreihe_c_w_Area_mean_korr = np.mean(c_w_Area_korr[1:5]) #ohne die beiden tief-Ausreißer
MS1_c_w_Area_mean_korr = np.mean(c_w_Area_korr[8:13])
MS2_c_w_Area_mean_korr = np.mean(c_w_Area_korr[13:18])
MS3_c_w_Area_mean_korr = np.mean(c_w_Area_korr[18:23])
MS4_c_w_Area_mean_korr = np.mean(c_w_Area_korr[23:28])

# Standardabweichungen berechnen
Zeitreihe_c_w_Area_korr_std = np.std(c_w_Area_korr[1:5])
MS1_c_w_Area_std_korr = np.std(c_w_Area_korr[8:13])
MS2_c_w_Area_std_korr = np.std(c_w_Area_korr[13:18])
MS3_c_w_Area_std_korr = np.std(c_w_Area_korr[18:23])
MS4_c_w_Area_std_korr = np.std(c_w_Area_korr[23:28])

#relativer Fehler
Zeitreihe_c_w_Area_korr_Fehler_Prozent = (Zeitreihe_c_w_Area_korr_std/Zeitreihe_c_w_Area_mean_korr)*100
MS1_c_w_Area_korr_Fehler_Prozent = (MS1_c_w_Area_std_korr / MS1_c_w_Area_mean_korr)*100
MS2_c_w_Area_korr_Fehler_Prozent = (MS2_c_w_Area_std_korr / MS2_c_w_Area_mean_korr)*100
MS3_c_w_Area_korr_Fehler_Prozent = (MS3_c_w_Area_std_korr / MS3_c_w_Area_mean_korr)*100
MS4_c_w_Area_korr_Fehler_Prozent = (MS4_c_w_Area_std_korr / MS4_c_w_Area_mean_korr)*100

print(f"(korrigiert): Zeitreihe-Mittelwert und rel. Abw: {Zeitreihe_c_w_Area_mean_korr:.3f} (± {Zeitreihe_c_w_Area_korr_Fehler_Prozent:.3f}%)")
print("korrigierte Mittelwerte der Propankonzentrationen nach Uranin-Peak an den Messstellen:")
print(f"MS1: {MS1_c_w_Area_mean_korr:.3f} (± {MS1_c_w_Area_korr_Fehler_Prozent:.3f}%)")
print(f"MS2: {MS2_c_w_Area_mean_korr:.3f} (± {MS2_c_w_Area_korr_Fehler_Prozent:.3f}%)")
print(f"MS3: {MS3_c_w_Area_mean_korr:.3f} (± {MS3_c_w_Area_korr_Fehler_Prozent:.3f}%)")
print(f"MS4: {MS4_c_w_Area_mean_korr:.3f} (± {MS4_c_w_Area_korr_Fehler_Prozent:.3f}%)")


# In[ ]:





# In[ ]:




