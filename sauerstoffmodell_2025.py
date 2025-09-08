# Umweltnaturwissenschaftliches Feldpraktikum 

# Gruppe A1: Stefanie Frey und Christina Trueck

# Sauerstoffmodell zu den Daten des Feldpraktikums 2025

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from scipy.integrate import solve_ivp
from astral.sun import sun
from astral import LocationInfo
from datetime import datetime
from scipy.optimize import curve_fit
from scipy.stats import linregress
from datetime import timedelta
from matplotlib.ticker import ScalarFormatter

# Datensaetze einlesen
df1 = pd.read_csv('Felddaten Logger 1_kalibriert.txt',header=0)
df2 = pd.read_csv('Felddaten Logger 2_kalibriert.txt',header=0)
df3 = pd.read_csv('Felddaten Logger 3_kalibriert.txt',header=0)
df4 = pd.read_csv('Felddaten Logger 4_kalibriert.txt',header=0)
df5 = pd.read_csv('Felddaten Logger 5_kalibriert.txt',header=0)
df6 = pd.read_csv('Felddaten Logger GB 83_kalibriert.txt',header=0)
df7 = pd.read_csv('Felddaten Logger GB 39_kalibriert.txt',header=0)
df_s = pd.read_csv('segmente_ueberwasser.csv',header=0)
df_s2 = pd.read_csv('segmente_ueberwasser_2.csv',header=0)

# Strahlungsdaten von Abschnitt M1-M3 in den Datensatz der Strahlungsdaten einfuegen
df_s['m13'] = df_s2['m2']

# Tuebingen festlegen
tuebingen = LocationInfo("Tuebingen","Germany","Europe/Berlin",48.52,9.05)

# Datensatz 2 kopieren, um Datenluecke nicht im Plot anzuzeigen
df2_2 = df2.copy()

# Zeit in datetime-Format umwandeln
df1['Zeit'] = pd.to_datetime(df1['Time (sec)'],unit='s')
df2['Zeit'] = pd.to_datetime(df2['Time (sec)'],unit='s')
df3['Zeit'] = pd.to_datetime(df3['Time (sec)'],unit='s')
df4['Zeit'] = pd.to_datetime(df4['Time (sec)'],unit='s')
df5['Zeit'] = pd.to_datetime(df5['Time (sec)'],unit='s')
df6['Zeit'] = pd.to_datetime(df6['Time (sec)'],unit='s')
df7['Zeit'] = pd.to_datetime(df7['Time (sec)'],unit='s')
df_s['Zeit'] = pd.to_datetime(df_s['time'],errors='coerce')
df2_2['Zeit'] = pd.to_datetime(df2['Time (sec)'],unit='s')

# Zeit im Strahlungsdatensatz nach hinten verschieben, um den Mittelpunkt der Zeit fuer einen Wert zu nehmen
df_s["Zeit"] = df_s["Zeit"] + pd.Timedelta(minutes=5)

# NaN-Werte interpolieren
df1.interpolate(method='linear',inplace=True)
df2.interpolate(method='linear',inplace=True)
df3.interpolate(method='linear',inplace=True)
df4.interpolate(method='linear',inplace=True)
df5.interpolate(method='linear',inplace=True)
df6.interpolate(method='linear',inplace=True)
df7.interpolate(method='linear',inplace=True)

# Zeitspalte als Index setzen
df1.set_index('Zeit',inplace=True)
df2.set_index('Zeit',inplace=True)
df3.set_index('Zeit',inplace=True)
df4.set_index('Zeit',inplace=True)
df5.set_index('Zeit',inplace=True)
df6.set_index('Zeit',inplace=True)
df7.set_index('Zeit',inplace=True)
df_s.set_index('Zeit',inplace=True)
df2_2.set_index('Zeit',inplace=True)

# Zeitindex in lokale Zeit konvertieren
df1.index = df1.index.tz_localize('UTC').tz_convert('Europe/Berlin')
df2.index = df2.index.tz_localize('UTC').tz_convert('Europe/Berlin')
df3.index = df3.index.tz_localize('UTC').tz_convert('Europe/Berlin')
df4.index = df4.index.tz_localize('UTC').tz_convert('Europe/Berlin')
df5.index = df5.index.tz_localize('UTC').tz_convert('Europe/Berlin')
df6.index = df6.index.tz_localize('UTC').tz_convert('Europe/Berlin')
df7.index = df7.index.tz_localize('UTC').tz_convert('Europe/Berlin')
#df2_2.index = df2.index.tz_localize('UTC').tz_convert('Europe/Berlin')

# Ueberpruefen, ob die Zeit in Sommerzeit angegeben ist
ist_sommerzeit1 = [ts.dst() != pd.Timedelta(0) for ts in df1.index]
ist_sommerzeit2 = [ts.dst() != pd.Timedelta(0) for ts in df2.index]
ist_sommerzeit3 = [ts.dst() != pd.Timedelta(0) for ts in df3.index]
ist_sommerzeit4 = [ts.dst() != pd.Timedelta(0) for ts in df4.index]
ist_sommerzeit5 = [ts.dst() != pd.Timedelta(0) for ts in df5.index]
ist_sommerzeit6 = [ts.dst() != pd.Timedelta(0) for ts in df6.index]
ist_sommerzeit7 = [ts.dst() != pd.Timedelta(0) for ts in df7.index]
ist_sommerzeit_s = df_s.index.map(lambda ts: ts.dst() != pd.Timedelta(0))

print(f"Anzahl Zeitstempel in Sommerzeit (df1): {sum(ist_sommerzeit1)}")
print(f"Anzahl Zeitstempel in Winterzeit (df1): {len(ist_sommerzeit1) - sum(ist_sommerzeit1)}")

print(f"Anzahl Zeitstempel in Sommerzeit (df2): {sum(ist_sommerzeit2)}")
print(f"Anzahl Zeitstempel in Winterzeit (df2): {len(ist_sommerzeit2) - sum(ist_sommerzeit2)}")

print(f"Anzahl Zeitstempel in Sommerzeit (df3): {sum(ist_sommerzeit3)}")
print(f"Anzahl Zeitstempel in Winterzeit (df3): {len(ist_sommerzeit3) - sum(ist_sommerzeit3)}")

print(f"Anzahl Zeitstempel in Sommerzeit (df4): {sum(ist_sommerzeit4)}")
print(f"Anzahl Zeitstempel in Winterzeit (df4): {len(ist_sommerzeit4) - sum(ist_sommerzeit4)}")

print(f"Anzahl Zeitstempel in Sommerzeit (df5): {sum(ist_sommerzeit5)}")
print(f"Anzahl Zeitstempel in Winterzeit (df5): {len(ist_sommerzeit5) - sum(ist_sommerzeit5)}")

print(f"Anzahl Zeitstempel in Sommerzeit (df6): {sum(ist_sommerzeit6)}")
print(f"Anzahl Zeitstempel in Winterzeit (df6): {len(ist_sommerzeit6) - sum(ist_sommerzeit6)}")

print(f"Anzahl Zeitstempel in Sommerzeit (df7): {sum(ist_sommerzeit7)}")
print(f"Anzahl Zeitstempel in Winterzeit (df7): {len(ist_sommerzeit7) - sum(ist_sommerzeit7)}")

print(f"Anzahl Zeitstempel in Sommerzeit (df_s): {sum(ist_sommerzeit_s)}")
print(f"Anzahl Zeitstempel in Winterzeit (df_s): {len(ist_sommerzeit_s) - sum(ist_sommerzeit_s)}")


#%%
## Sauerstoffkonzentrationen der einzelnen Logger darstellen

# Zeitbereich definieren
start = pd.to_datetime('2025-08-06 09:30:00')
ende = pd.to_datetime('2025-08-14 08:00:00')

# Ticks in 24h-Abstaenden an der x-Achse darstellen
ticks = pd.date_range(start=start,end=ende,freq='24h')

# Saettigungskonzentration aus den Temperaturdaten berechnen
def c_sat(T):                # Saettigungskonzentration [mg/L]
    return 468/(31.6+T)

# Sauerstoffkonzentrationen an M1 gemessen mit Logger 1
plt.figure(figsize=(8,8))
plt.plot(df1.index,df1['DO (mg/l)'],label=r'Konzentration $c ~ \mathrm{[mg ~ L^{-1}]}$',color='blue')
plt.plot(df1.index,c_sat(df1['T (deg C)']),label=r'Saettigungskonzentration $c_\mathrm{sat} ~ \mathrm{[mg ~ L^{-1}]}$',color='green')
plt.xlabel('\nZeit',fontsize=18)
plt.ylabel(r'Konzentration $c~[\mathrm{mg ~ L^{-1}}]$',fontsize=18)
plt.ylim(5,11)
plt.title('Messstation 1',fontsize=18)
plt.legend(loc='upper center',bbox_to_anchor=(0.5, -0.3),fontsize=14)
plt.grid(True)
plt.tick_params(axis='both',labelsize=16) 
ax = plt.gca()
ax.set_xlim(start,ende)
ax.set_xticks(ticks)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m\n%H:%M'))
plt.tight_layout()
plt.show()

# Sauerstoffkonzentrationen an M2 gemessen mit Logger 2

# Zeitbereich fuer die Datenluecke definieren
start_luecke = pd.Timestamp("2025-08-11 22:32:00")
ende_luecke = pd.Timestamp("2025-08-12 09:52:00")
df_before = df2_2[df2_2.index < start_luecke]
df_after  = df2_2[df2_2.index > ende_luecke]

plt.figure(figsize=(8,8))
plt.plot(df_before.index,df_before['DO (mg/l)'],label=r'Konzentration $c ~ \mathrm{[mg ~ L^{-1}]}$',color='blue')
plt.plot(df_after.index,df_after['DO (mg/l)'],color='blue')
plt.plot(df2.index,c_sat(df2['T (deg C)']), label=r'Saettigungskonzentration $c_\mathrm{sat} ~ \mathrm{[mg ~ L^{-1}]}$',color='green')
plt.xlabel('\nZeit',fontsize=18)
plt.ylabel(r'Konzentration $c~[\mathrm{mg ~ L^{-1}}]$',fontsize=18)
plt.ylim(5,11)
plt.title('Messstation 2',fontsize=18)
plt.legend(loc='upper center',bbox_to_anchor=(0.5, -0.3),fontsize=14)
plt.grid(True)
plt.tick_params(axis='both', labelsize=16) 
ax = plt.gca()
ax.set_xlim(start,ende)
ax.set_xticks(ticks)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m\n%H:%M'))
plt.tight_layout()
plt.show()

# Sauerstoffkonzentrationen an M3 gemessen mit Logger 3
plt.figure(figsize=(8,8))
plt.plot(df3.index,df3['DO (mg/l)'],label=r'Konzentration $c ~ \mathrm{[mg ~ L^{-1}]}$',color='blue')
plt.plot(df3.index,c_sat(df3['T (deg C)']),label=r'Saettigungskonzentration $c_\mathrm{sat} ~ \mathrm{[mg ~ L^{-1}]}$',color='green')
plt.xlabel('\nZeit',fontsize=18)
plt.ylabel(r'Konzentration $c~[\mathrm{mg ~ L^{-1}}]$',fontsize=18)
plt.ylim(5,11)
plt.title('Messstation 3',fontsize=18)
plt.legend(loc='upper center',bbox_to_anchor=(0.5, -0.3),fontsize=14)
plt.grid(True)
plt.tick_params(axis='both',labelsize=16) 
ax = plt.gca()
ax.set_xlim(start,ende)
ax.set_xticks(ticks)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m\n%H:%M'))
plt.tight_layout()
plt.show()

# Sauerstoffkonzentrationen an M4 gemessen mit Logger 4
plt.figure(figsize=(8,8))
plt.plot(df4.index,df4['DO (mg/l)'],label=r'Konzentration $c ~ \mathrm{[mg ~ L^{-1}]}$',color='blue')
plt.plot(df4.index,c_sat(df4['T (deg C)']),label=r'Saettigungskonzentration $c_\mathrm{sat} ~ \mathrm{[mg ~ L^{-1}]}$',color='green')
plt.xlabel('\nZeit',fontsize=18)
plt.ylabel(r'Konzentration $c~[\mathrm{mg ~ L^{-1}}]$',fontsize=18)
plt.ylim(5,11)
plt.title('Messstation 4',fontsize=18)
plt.legend(loc='upper center',bbox_to_anchor=(0.5, -0.3),fontsize=14)
plt.grid(True)
plt.tick_params(axis='both',labelsize=16) 
ax = plt.gca()
ax.set_xlim(start,ende)
ax.set_xticks(ticks)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m\n%H:%M'))
plt.tight_layout()
plt.show()

# Sauerstoffkonzentrationen an M5 (Goldersbach) gemessen mit Logger 5
plt.figure(figsize=(8,8))
plt.plot(df5.index,df5['DO (mg/l)'],label=r'Konzentration $c ~ \mathrm{[mg ~ L^{-1}]}$',color='blue')
plt.plot(df5.index,c_sat(df5['T (deg C)']),label=r'Saettigungskonzentration $c_\mathrm{sat} ~ \mathrm{[mg ~ L^{-1}]}$',color='green')
plt.xlabel('\nZeit',fontsize=18)
plt.ylabel(r'Konzentration $c~[\mathrm{mg ~ L^{-1}}]$',fontsize=18)
plt.ylim(0,11)
plt.title('Messstation 5 - Goldersbach',fontsize=18)
plt.legend(loc='upper center',bbox_to_anchor=(0.5, -0.3),fontsize=14)
plt.grid(True)
plt.tick_params(axis='both', labelsize=16) 
ax = plt.gca()
ax.set_xlim(start,ende)
ax.set_xticks(ticks)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m\n%H:%M'))
plt.tight_layout()
plt.show()

# Sauerstoffkonzentrationen an M5 (Goldersbach) gemessen mit Logger 5, 6 und 7
plt.figure(figsize=(10,8))
plt.plot(df5.index,df5['DO (mg/l)'],label='Logger 5',color='darkgreen',zorder=1)
plt.plot(df6.index,df6['DO (mg/l)'],label='Logger 6',color='gold',zorder=2) 
plt.plot(df7.index,df7['DO (mg/l)'],label='Logger 7',color='crimson',zorder=3)
plt.xlabel('\nZeit',fontsize=18)
plt.ylabel(r'Konzentration $c~[\mathrm{mg ~ L^{-1}}]$',fontsize=18)
plt.ylim(0,10)
plt.legend(loc='upper center',bbox_to_anchor=(0.35, 0.1),fontsize=15,ncol=3)
plt.grid(True)
plt.tick_params(axis='both', labelsize=16) 
ax = plt.gca()
ax.set_xlim(start,ende)
ax.set_xticks(ticks)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m\n%H:%M'))
plt.tight_layout()
plt.show()

# Sauerstoffkonzentrationen Vergleich zwischen Logger 3 und Logger 7
plt.figure(figsize=(10,8))
plt.plot(df3.index,df3['DO (mg/l)'],label=r'Logger 3',color='deepskyblue')
plt.plot(df7.index,df7['DO (mg/l)'],label='Goldersbach in Stroemung (39)',color='purple')
plt.xlabel('\nZeit',fontsize=18)
plt.ylabel(r'Konzentration $c~[\mathrm{mg ~ L^{-1}}]$',fontsize=18)
plt.ylim(6,9)
plt.title('Messstation 5 (Goldersbach) - Logger 3 und GB 39',fontsize=18)
plt.legend(loc='upper center',bbox_to_anchor=(0.5, -0.2),fontsize=14,ncol=5)
plt.grid(True)
plt.tick_params(axis='both',labelsize=16) 
ax = plt.gca()
ax.set_xlim(start,ende)
ax.set_xticks(ticks)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m\n%H:%M'))
plt.tight_layout()
plt.show()

# Sauerstoffkonzentrationen von allen Loggern 
plt.figure(figsize=(10,8))
plt.plot(df1.index,df1['DO (mg/l)'],label=r'Logger 1',color='darkorange')
plt.plot(df2.index,df2['DO (mg/l)'],label=r'Logger 2',color='yellowgreen')
plt.plot(df3.index,df3['DO (mg/l)'],label=r'Logger 3',color='deepskyblue')
plt.plot(df4.index,df4['DO (mg/l)'],label=r'Logger 4',color='purple')
plt.plot(df5.index,df5['DO (mg/l)'],label=r'Logger 5',color='darkgreen')
plt.xlabel('\nZeit',fontsize=18)
plt.ylabel(r'Konzentration $c~[\mathrm{mg ~ L^{-1}}]$',fontsize=18)
plt.ylim(0,10)
plt.title('Alle Logger',fontsize=18)
plt.legend(loc='upper center',bbox_to_anchor=(0.5, -0.2),fontsize=14,ncol=5)
plt.grid(True)
plt.tick_params(axis='both', labelsize=16) 
ax = plt.gca()
ax.set_xlim(start,ende)
ax.set_xticks(ticks)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m\n%H:%M'))
plt.tight_layout()
plt.show()

# Sauerstoffkonzentrationen an allen vier Messstellen gemessen mit Logger 1,2,3 und 4
plt.figure(figsize=(10,8))
plt.plot(df1.index,df1['DO (mg/l)'],label=r'Logger 1',color='darkorange')
plt.plot(df_before.index,df_before['DO (mg/l)'],label='Logger 2',color='yellowgreen')
plt.plot(df_after.index,df_after['DO (mg/l)'],color='yellowgreen')
plt.plot(df3.index,df3['DO (mg/l)'],label=r'Logger 3',color='deepskyblue')
plt.plot(df4.index,df4['DO (mg/l)'],label=r'Logger 4',color='purple')
plt.xlabel('\nZeit',fontsize=18)
plt.ylabel(r'Konzentration $c~[\mathrm{mg ~ L^{-1}}]$',fontsize=18)
plt.ylim(5,9)
plt.legend(loc='upper center',bbox_to_anchor=(0.5, 0.1),fontsize=15,ncol=4)
plt.grid(True)
plt.tick_params(axis='both', labelsize=16) 
ax = plt.gca()
ax.set_xlim(start,ende)
ax.set_xticks(ticks)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m\n%H:%M'))
plt.tight_layout()
plt.show()

# Strahlung gegen Zeit plotten
plt.figure(figsize=(10,8))
plt.plot(df_s.index, df_s['m2'],label='M1-M2',color='purple')
plt.plot(df_s.index, df_s['m3'],label='M2-M3',color='blue')
plt.plot(df_s.index, df_s['m4'],label='M3-M4',color='green')
plt.plot(df_s.index, df_s['m13'],label='M1-M3',color='orange')
plt.xlabel('Zeit')
plt.ylabel('Strahlung')
plt.ylim(0,600)
plt.title('Strahlung ueber Zeit')
plt.legend()
plt.grid(True)
plt.tick_params(axis='both',labelsize=16) 
ax = plt.gca()
ax.set_xlim(start,ende)
ax.set_xticks(ticks)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m\n%H:%M'))
plt.tight_layout()
plt.show()

#%%
## Verduennung des Goldersbachs von M3 auf M4 berechnen

# Zeitraum festlegen
start_GB = pd.Timestamp("2025-08-12 19:17:00",tz="Europe/Berlin")
ende_GB  = pd.Timestamp("2025-08-14 10:12:00",tz="Europe/Berlin")

# Zeitraum zuschneiden
df3_cut = df3.loc[start_GB:ende_GB,['DO (mg/l)']].rename(columns={'DO (mg/l)':'M3'})
df7_cut = df7.loc[start_GB:ende_GB,['DO (mg/l)']].rename(columns={'DO (mg/l)':'GB39'})

# Fuer jeden Zeitpunkt in df3 den naehsten in df7 suchen
idx = df7_cut.index.get_indexer(df3_cut.index,method="nearest")
df7_zeiten = df7_cut.index[idx]

# Fuer Paar-Zuordnung Dataframe erstellen
df_compare = pd.DataFrame({"Zeit_M3": df3_cut.index,"M3": df3_cut['M3'].values,"Zeit_GB39": df7_zeiten,"GB39": df7_cut['GB39'].values[idx]})

# Lineare Regression berechnen
slope, intercept, r_value, p_value, std_err = linregress(df_compare['M3'], df_compare['GB39'])
x_vals = np.array([df_compare['M3'].min(), df_compare['M3'].max()])
y_vals = slope * x_vals + intercept

# Logger 3 gegen Logger GB 39 plotten
plt.figure(figsize=(11,7))
plt.scatter(df_compare['M3'],df_compare['GB39'],marker='o',s=10,label='Datenpunkte')
plt.plot(x_vals, y_vals,color='red',linewidth=2.5,label=f'Lineare Regression: y = {slope:.2f}x + {intercept:.2f}, $R^2$ = {r_value**2:.3f}')
plt.xlabel(r"$c\mathrm{(O_2)}$ Logger 3 $[\mathrm{mg ~ L^{-1}}]$",fontsize=18)
plt.ylabel(r"$c\mathrm{(O_2)}$ Logger 7 $[\mathrm{mg ~ L^{-1}}]$",fontsize=18)
plt.xlim(6.2,7.6)
plt.tick_params(axis='both',labelsize=17)
plt.grid(True)
plt.legend(fontsize=17)
plt.tight_layout()
plt.show()

print("\nVerhaeltnis zwischen Logger 3 und Logger 7:")
print(f"Lineare Regression: y = {slope:.3f}x + {intercept:.3f}, R² = {r_value**2:.3f}")

# Neuen Dataframe erstellen, um Verduennung miteinzubeziehen
df8 = df3.copy()

# Durchfluss definieren
Q3 = 0.311
Q4 = 0.354
recov = Q3/Q4

# Sauerstoffkonzentrationen mit Verduennung durch Goldersbach berechnen 
df8['DO (mg/l)'] = df3['DO (mg/l)']*(recov+(1-recov)*slope)+(1-recov)*intercept

# Dataframe mit Verduennung als neue Datei speichern
df8.to_csv("M3 Daten inkl. Verduennung Goldersbach.txt", index=False, float_format="%.3f")


## Tagesverlauf von GB 39 auf alle Tage uebertragen mit Beruecksichtigung von Logger 3 (fake Datensatz)

# Sauerstoffwert in Datensatz durch kalibrierten Wert ersetzen
df5["DO (mg/l)_fake"] = slope* df3['DO (mg/l)'] + intercept

# Sauerstoffkonzentrationen Vergleich GB 39, Logger 3 und Fake GB Logger
plt.figure(figsize=(10,8))
plt.plot(df3.index,df3['DO (mg/l)'],label=r'Logger 3',color='deepskyblue')
plt.plot(df7.index,df7['DO (mg/l)'],label='Logger 7',color='crimson',zorder=2)
plt.plot(df8.index,df8['DO (mg/l)'],label = 'Logger 3 inkl. Goldersbach-Verduennung',color='royalblue')
plt.plot(df5.index,df5["DO (mg/l)_fake"], label='Rekonstruierte Daten von Logger 7', color='plum',zorder=1)
plt.xlabel('\nZeit',fontsize=18)
plt.ylabel(r'Konzentration $c~[\mathrm{mg ~ L^{-1}}]$',fontsize=18)
plt.ylim(5.7,9.5)
plt.legend(loc='upper center',bbox_to_anchor=(0.5, 0.15),fontsize=15,ncol=2)
plt.grid(True)
plt.tick_params(axis='both',labelsize=16) 
ax = plt.gca()
ax.set_xlim(start,ende)
ax.set_xticks(ticks)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m\n%H:%M'))
plt.tight_layout()
plt.show()


#%%
## Messabschnitt M1-M2

# Fliesszeit definieren und als Zeitformat darstellen
fliesszeit = 58.89 * 60      # Fliesszeit in Sekunden
fliesszeit_td = pd.to_timedelta(fliesszeit,unit='s')

# Berechnung des Zeitpunkts, an dem das betrachtete Wasserpaket an der naechsten Station ankommt
df1['Zeit_nach_Fluss'] = df1.index + fliesszeit_td

# In df2 Zeitpunkt von ankommendem Wasserpaket finden
idx = df2.index.get_indexer(df1['Zeit_nach_Fluss'],method='nearest')
df2_zeiten = df2.index[idx]

# Zeitpunkte von Wasserpaket an Messstelle 1 und 2 kombinieren
df_paar = pd.DataFrame({'Zeit_df1':df1.index,'Zeit_df2':df2_zeiten})

# Temperaturen und Konzentrationen aus df1 zu df_paar hinzufuegen
df_paar['Temp_df1'] = df1.loc[df_paar['Zeit_df1'],'T (deg C)'].values
df_paar['Konz_df1'] = df1.loc[df_paar['Zeit_df1'],'DO (mg/l)'].values

# Temperaturen und Konzentrationen aus df2 (nach Verschiebung) zu df_paar hinzufuegen
df_paar['Temp_df2'] = df2.loc[df_paar['Zeit_df2'],'T (deg C)'].values
df_paar['Konz_df2'] = df2.loc[df_paar['Zeit_df2'],'DO (mg/l)'].values

# Saettigungskonzentration aus den Temperaturdaten berechnen
def c_sat(T):                # Saettigungskonzentration [mg/L]
    return 468/(31.6+T)

# Saettigungskonzentration als neue Spalte dem Datensatz hinzufuegen
df_paar['Saettigungskonz_df1 [mg/L]'] = c_sat(df_paar['Temp_df1'])
df_paar['Saettigungskonz_df2 [mg/L]'] = c_sat(df_paar['Temp_df2'])

# Spalte mit Saettigungsdefizit hinzufuegen
df_paar['Saettigungsdefizit_df1'] = df_paar['Saettigungskonz_df1 [mg/L]']-df_paar['Konz_df1']
df_paar['Saettigungsdefizit_df2'] = df_paar['Saettigungskonz_df2 [mg/L]']-df_paar['Konz_df2']

# Spalte mit dem Mittelwert der Zeit aus beiden Datensatzen hinzufuegen
df_paar['Zeit_mittel'] = df_paar[['Zeit_df1', 'Zeit_df2']].mean(axis=1)

# Mittelwert fuer das Saettigungsdefizit aus beiden Dataframes berechnen
df_paar['Saettigungsdefizitmittelwert'] = (df_paar['Saettigungsdefizit_df1']+df_paar['Saettigungsdefizit_df2'])/2

# Saettigungsdefizit gegen Zeit plotten
plt.figure(figsize=(8,6))
plt.plot(df_paar['Zeit_mittel'],df_paar['Saettigungsdefizitmittelwert'])
plt.title('Saettigungsdefizit fuer Messabschnitt 1')
plt.xlabel('\nZeit',fontsize=18)
plt.ylabel(r'Saettigungsdefizit $c_\mathrm{sat}-c~[\mathrm{mg ~ L^{-1}}]$',fontsize=18)
plt.ylim(1,4)
plt.grid(True)
plt.tick_params(axis='both',labelsize=16) 
ax = plt.gca()
ax.set_xlim(start,ende)
ax.set_xticks(ticks)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m\n%H:%M'))
plt.tight_layout()
plt.show()

#%% 

## Messabschnitt M1-M2 - Nacht

# Neue Spalte in Dataframe einfuegen, um rauszufiltern, ob der Zeitpunkt in der Nacht liegt
df_paar['ist_Nacht'] = False

# Schleife, um dies bei jedem einzelnen Tag zu ueberpruefen
for tag in df_paar['Zeit_df1'].dt.normalize().unique():
    s = sun(tuebingen.observer,date=tag.date(),tzinfo=tuebingen.timezone)
    sunrise = s['sunrise']
    sunset = s['sunset']
    
    # Daten direkt vor Sonnenaufgang nicht miteinbeziehen 
    sunrise_adj = sunrise - timedelta(hours=2)
    
    # Alle Zeitpunkte markieren, die ausserhalb von Sonnenaufgang/-untergang liegen
    mask = (df_paar['Zeit_df1'].dt.date == tag.date()) & ((df_paar['Zeit_df1'] < sunrise_adj) | (df_paar['Zeit_df1'] > sunset))
    df_paar.loc[mask,'ist_Nacht'] = True

# Neuen Dataframe nur mit den Nachtdaten erstellen
df_paar_nacht = df_paar[df_paar['ist_Nacht']].copy()

# Spalte wieder loeschen
df_paar_nacht.drop(columns='ist_Nacht',inplace=True)

# Mittelwert der Zeit
df_paar_nacht['Zeit_mittel'] = df_paar_nacht[['Zeit_df1','Zeit_df2']].mean(axis=1)

# Alle Daten vor und nach der Tracernacht entfernen
start = pd.Timestamp("2025-08-06 09:00:00",tz="Europe/Berlin")
end = pd.Timestamp("2025-08-10 12:00:00",tz="Europe/Berlin")
df_paar_nacht = df_paar_nacht[(df_paar_nacht['Zeit_mittel'] < start) | (df_paar_nacht['Zeit_mittel'] > end)]

start = pd.Timestamp("2025-08-11 12:00:00",tz="Europe/Berlin")
end = pd.Timestamp("2025-08-15 16:00:00",tz="Europe/Berlin")
df_paar_nacht = df_paar_nacht[(df_paar_nacht['Zeit_mittel'] < start) | (df_paar_nacht['Zeit_mittel'] > end)]

# Mittelwert fuer das Saettigungsdefizit aus beiden Datensaetzen berechnen
df_paar_nacht['Saettigungsdefizitmittelwert'] = (df_paar_nacht['Saettigungsdefizit_df1']+df_paar_nacht['Saettigungsdefizit_df2'])/2

# r_tot berechnen
df_paar_nacht['r_tot'] = -(((df_paar_nacht['Saettigungsdefizit_df2']-df_paar_nacht['Saettigungsdefizit_df1'])/fliesszeit)-((df_paar_nacht['Saettigungskonz_df2 [mg/L]']-df_paar_nacht['Saettigungskonz_df1 [mg/L]'])/fliesszeit))

# Parameter gegen die Zeit plotten
plt.figure()
plt.subplot(2,1,1)
plt.plot(df_paar_nacht['Zeit_mittel'],df_paar_nacht['r_tot'],'.')
plt.xlabel('Zeit')
plt.ylabel(r'$r_{\mathrm{tot}}$ $\left[\frac{\mathrm{mg}}{\mathrm{L} \cdot \mathrm{s}}\right]$')
plt.grid()
plt.xticks(rotation=45)
plt.subplot(2,1,2)
plt.plot(df_paar_nacht['Zeit_mittel'],df_paar_nacht['Saettigungsdefizitmittelwert'],'.')
plt.xlabel('Zeit')
plt.ylabel(r'Saettigungsdefizit $\left[\frac{\mathrm{mg}}{\mathrm{L}}\right]$')
plt.grid()
plt.xticks(rotation=45)

# Lineare Regression
k2, r_zehr = np.polyfit(df_paar_nacht['Saettigungsdefizitmittelwert'],df_paar_nacht['r_tot'],1)

# Residuen berechnen
residuals = df_paar_nacht['r_tot']-(k2*df_paar_nacht['Saettigungsdefizitmittelwert']+r_zehr)
sigma2 = np.sum(residuals**2)/(len(df_paar_nacht)-2)

# Hilfsgroessen definieren
x = df_paar_nacht['Saettigungsdefizitmittelwert']
x_mean = np.mean(x)
Sxx = np.sum((x - x_mean)**2)
n = len(x)

# Standardfehler berechnen
sigma_k2 = np.sqrt(sigma2 / Sxx)
sigma_r_zehr = np.sqrt(sigma2 * (1/n + x_mean**2 / Sxx))

# Werte fuer die Gerade berechnen
x = np.linspace(df_paar_nacht['Saettigungsdefizitmittelwert'].min(),df_paar_nacht['Saettigungsdefizitmittelwert'].max(),100)
y = k2 * x + r_zehr


## Unsicherheitsbereich einfuegen
# Abweichungen und Standardabweichung
abweichung = df_paar_nacht['r_tot']-(k2*df_paar_nacht['Saettigungsdefizitmittelwert']+r_zehr)
sigma = np.std(abweichung)

# Unsicherheitsbereich (nur Parameter)
n = len(df_paar_nacht)
x_mean = np.mean(df_paar_nacht['Saettigungsdefizitmittelwert'])
standardfehler_regression = sigma*np.sqrt(1/n+(x-x_mean)**2/np.sum((df_paar_nacht['Saettigungsdefizitmittelwert']-x_mean)**2))
ci_upper = y + 1.96 * standardfehler_regression
ci_lower = y - 1.96 * standardfehler_regression

# Unsicherheitsbereich (Parameter + Messfehler)
y_upper = y + sigma
y_lower = y - sigma

# Plot mit linearer Regression erstellen
plt.figure(figsize=(9,6))
plt.plot(df_paar_nacht['Saettigungsdefizitmittelwert'],df_paar_nacht['r_tot'],'.', markersize=3)
plt.plot(x,y,label=f'Regression: y = {k2:.2e}x + {r_zehr:.2e}',color='purple')
plt.tick_params(axis='both',labelsize=13) 

plt.fill_between(x,y_lower,y_upper,color='lightblue',alpha=0.4,label='Parameter- und Messfehlerunsicherheit')
plt.fill_between(x,ci_lower,ci_upper,color='darkblue',alpha=0.3, label='Parameterunsicherheit')

plt.xlabel(r'$c_\mathrm{sat} - c ~ [\mathrm{mg ~ L^{-1}}]$',fontsize=14)
plt.ylabel(r'$r_{\mathrm{tot}}$ $[\mathrm{mg ~ L^{-1} ~ s^{-1}}]$',fontsize=14)
plt.legend(fontsize=13) 
plt.grid(True)
plt.xlim(3.135,3.573)
plt.ylim(-0.00006,0.00009)
plt.ticklabel_format(style='sci',axis='y',scilimits=(-10,10))
plt.show()

# Werte fuer k2 und r_zehr ausgeben lassen
print("\nAbschnitt M1-M2")
print("\nParameter aus Nachtdaten:")
print(f"k2 = {k2:.3e} ± {sigma_k2:.3e}")
print(f"r_zehr = {r_zehr:.3e} ± {sigma_r_zehr:.3e}")

#%%
# Messabschnitt M1-M2 - Tag

# Neue Spalte in Dataframe einfuegen, um rauszufiltern, ob der Zeitpunkt am Tag ist
df_paar['ist_Tag'] = False  

# Schleife, um dies bei jedem einzelnen Tag zu ueberpruefen
for tag in df_paar['Zeit_df1'].dt.normalize().unique():
    s = sun(tuebingen.observer,date=tag.date(),tzinfo=tuebingen.timezone)
    sunrise = s['sunrise']
    sunset = s['sunset']
    
    # Daten direkt vor Sonnenaufgang nicht miteinbeziehen
    sunrise_adj = sunrise - timedelta(hours=2)
    
    # Alle Zeitpunkte markieren, die innerhalb von Sonnenaufgang/-untergang liegen
    mask = (df_paar['Zeit_df1'].dt.date == tag.date()) & ((df_paar['Zeit_df1'] >= sunrise_adj) & (df_paar['Zeit_df1'] <= sunset))
    df_paar.loc[mask,'ist_Tag'] = True

# Neuen Dataframe nur mit den Tagesdaten erstellen
df_paar_tag = df_paar[df_paar['ist_Tag']].copy()

# Spalte wieder loeschen
df_paar_tag.drop(columns='ist_Tag', inplace=True)

# Mittelwert der Zeit
df_paar_tag['Zeit_mittel'] = df_paar_tag[['Zeit_df1','Zeit_df2']].mean(axis=1)

# Alle Daten vor und nach der Tracernacht entfernen
start = pd.Timestamp("2025-08-06 09:00:00",tz="Europe/Berlin")
end = pd.Timestamp("2025-08-09 06:00:00",tz="Europe/Berlin")
df_paar_tag = df_paar_tag[(df_paar_tag['Zeit_mittel'] < start) | (df_paar_tag['Zeit_mittel'] > end)]

start = pd.Timestamp("2025-08-11 22:00:00",tz="Europe/Berlin")
end = pd.Timestamp("2025-08-15 12:00:00",tz="Europe/Berlin")
df_paar_tag = df_paar_tag[(df_paar_tag['Zeit_mittel'] < start) | (df_paar_tag['Zeit_mittel'] > end)]

# Naechstgelegene Zeit von df_s zu df_paar_tag finden und hinzufuegen
strahlungs_idx = df_s.index.get_indexer(df_paar_tag['Zeit_mittel'],method='nearest')
df_paar_tag['Strahlung'] = df_s.iloc[strahlungs_idx]['m2'].values

# r_tot berechnen
df_paar_tag['r_tot'] = -(((df_paar_tag['Saettigungsdefizit_df2']-df_paar_tag['Saettigungsdefizit_df1'])/fliesszeit)-((df_paar_tag['Saettigungskonz_df2 [mg/L]']-df_paar_tag['Saettigungskonz_df1 [mg/L]'])/fliesszeit))

# Mittelwert fuer das Saettigungsdefizit aus beiden Dataframes berechnen 
df_paar_tag['Saettigungsdefizitmittelwert'] = (df_paar_tag['Saettigungsdefizit_df1']+df_paar_tag['Saettigungsdefizit_df2'])/2

# r_photo berechnen
df_paar_tag['r_photo'] = df_paar_tag['r_tot']-r_zehr- k2*df_paar_tag['Saettigungsdefizitmittelwert']


## Lineare Regression
# Lineare Regression durch den Ursprung
k_photo = np.sum(df_paar_tag['Strahlung']*df_paar_tag['r_photo'])/np.sum(df_paar_tag['Strahlung']**2)

# Residuen berechnen
residuals = df_paar_tag['r_photo'] - k_photo*df_paar_tag['Strahlung']
sigma2 = np.sum(residuals**2) / (len(df_paar_tag) - 1)

# Standardfehler berechnen
sigma_k_photo = np.sqrt(sigma2 / np.sum(df_paar_tag['Strahlung']**2))

# Werte fuer die Gerade berechnen
x_tag = np.linspace(df_paar_tag['Strahlung'].min(),df_paar_tag['Strahlung'].max(),100)
y_tag = k_photo * x_tag


## Regression mit Michaelis-Menten
# Michaelis-Menten Kinetik definieren
def michaelis_menten(R,r_max,R_halb):
    return r_max * R / (R + R_halb)

# Anfangsschaetzungen fuer r_photo_max und R_0.5 (aus ODE Hausaufgabe)
schaetzung = [10**(-3),100]

# Fit durchfuehren
params, covparams = curve_fit(michaelis_menten,df_paar_tag['Strahlung'],df_paar_tag['r_photo'],p0=schaetzung)
r_photo_max, R_halb = params

y_mm = michaelis_menten(df_paar_tag['Strahlung'],r_photo_max,R_halb)


## Unsicherheitsbereiche einfuegen
# Abweichungen und Standardabweichung fuer lineare Regression
abweichung_tag = df_paar_tag['r_photo']-(k_photo*df_paar_tag['Strahlung'])
sigma_tag = np.std(abweichung_tag)

abweichung_tag_mm = df_paar_tag['r_photo'] - y_mm
sigma_tag_mm = np.sqrt(np.sum(abweichung_tag_mm**2)/(len(y_mm)-2))

y_mm = michaelis_menten(x_tag,r_photo_max,R_halb)

# Unsicherheitsbereich (nur Parameter) fuer lineare Regression
n_tag = len(df_paar_tag)
x_mean_tag = np.mean(df_paar_tag['Strahlung'])
standardfehler_regression_tag = sigma_tag*np.sqrt(1/n_tag+(x_tag-x_mean_tag)**2/np.sum((df_paar_tag['Strahlung']-x_mean_tag)**2))
ci_tag_upper = y_tag + 1.96 * standardfehler_regression_tag
ci_tag_lower = y_tag - 1.96 * standardfehler_regression_tag

# Unsicherheitsbereich (Parameter + Messfehler)
y_tag_upper = y_tag + sigma_tag
y_tag_lower = y_tag - sigma_tag

# Standardabweichungen der Parameter aus Kovarianzmatrix
perr = np.sqrt(np.diag(covparams))  

# Unsicherheitsbereich (nur Parameter) fuer Michaelis-Menten-Fit
def mm_error_propagation(R,r_max,R_halb,Cpp):
    df_drmax = R / (R + R_halb)
    df_dRhalb = -r_max * R / (R + R_halb)**2
    sensi = np.zeros((2,len(R)))
    sensi[0,:] = df_drmax
    sensi[1,:] = df_dRhalb
    prop_var = sensi.T @ Cpp @ sensi
    return np.sqrt(np.diag(prop_var))

mm_std = mm_error_propagation(x_tag,r_photo_max,R_halb,covparams)
ci_upper_mm = y_mm + 1.96 * mm_std
ci_lower_mm = y_mm - 1.96 * mm_std

# Gesamtunsicherheitsbereich (Parameter + Messfehler)
y_upper_mm = y_mm + 1.96*np.sqrt(sigma_tag_mm**2+mm_std**2)
y_lower_mm = y_mm - 1.96*np.sqrt(sigma_tag_mm**2+mm_std**2)

# Tagesdaten mit Unischerheitsbereichen plotten
plt.figure(figsize=(10,7))
plt.plot(df_paar_tag['Strahlung'],df_paar_tag['r_photo'],'.',markersize=3)
plt.tick_params(axis='both',labelsize=15) 

# Lineare Regression
plt.plot(x_tag,y_tag,'r-',label=f'Lineare Regression: y = {k_photo:.2e}x')
plt.fill_between(x_tag,y_tag_lower,y_tag_upper,color='pink',alpha=0.4,label='\nLineare Regression: Parameter- \nund Messfehlerunsicherheit')
plt.fill_between(x_tag,ci_tag_lower,ci_tag_upper,color='red',alpha=0.5,label='\nLineare Regression: \nParameterunsicherheit')

# Michaelis-Menten
plt.plot(x_tag,y_mm,'g-',label='\nMichaelis-Menten Kinetik\n')
plt.fill_between(x_tag,y_lower_mm,y_upper_mm,color='lightgreen',alpha=0.25,label='\nMichaelis Menten: Parameter- \nund Messfehlerunsicherheit')
plt.fill_between(x_tag,ci_lower_mm,ci_upper_mm,color='green',alpha=0.35,label='\nMichaelis Menten: \nParameterunsicherheit')

plt.xlabel(r'$R$ $[\mathrm{W ~ m^{-2}}]$',fontsize=18)
plt.ylabel(r'$r_{\mathrm{photo}}$ $[\mathrm{mg ~ L^{-1} ~ s^{-1}}]$',fontsize=18)
plt.legend(loc='center left',bbox_to_anchor=(1, 0.5),ncol=1,fontsize=16)
plt.grid(True)
plt.xlim(0,530)
plt.ylim(-0.0001,0.001)
plt.show()

# Parameter ausgeben lassen
print("\nParameter aus Tagdaten:")

print("Lineare Regression:")
print(f"k_photo = {k_photo:.3e} ± {sigma_k_photo:.3e}")

print("\nMichaelis-Menten Parameter:")
print(f"r_photo_max = {r_photo_max:.3e} ± {perr[0]:.3e}")
print(f"R_0.5 = {R_halb:.3f} ± {perr[1]:.3f}\n")

# Dataframe mit Parametern erstellen
parameter_namen = ["k2", "r_zehr", "k_photo", "r_photo_max", "R_0.5"]
df_param = pd.DataFrame(index=parameter_namen)

# Werte als Spalte einfuegen
df_param["M1-M2"] = [k2, r_zehr, k_photo, r_photo_max, R_halb]


#%%

## Messabschnitt M1-M3

# Fliesszeit definieren und als Zeitformat darstellen
fliesszeit_13 = (58.89 + 73.06) * 60     # Fliesszeit in Sekunden
fliesszeit_td_13 = pd.to_timedelta(fliesszeit_13,unit='s')

# Berechnung des Zeitpunkts, an dem das betrachtete Wasserpaket an der naechsten Station ankommt
df1['Zeit_nach_Fluss_13'] = df1.index + fliesszeit_td_13

# In df2 Zeitpunkt von ankommendem Wasserpaket finden
idx = df3.index.get_indexer(df1['Zeit_nach_Fluss_13'],method='nearest')
df3_zeiten = df3.index[idx]

# Zeitpunkte von Wasserpaket an Messstelle 1 und 2 kombinieren
df_paar_13 = pd.DataFrame({'Zeit_df1':df1.index,'Zeit_df3':df3_zeiten})

# Temperaturen und Konzentrationen aus df1 zu df_paar hinzufuegen
df_paar_13['Temp_df1'] = df1.loc[df_paar_13['Zeit_df1'],'T (deg C)'].values
df_paar_13['Konz_df1'] = df1.loc[df_paar_13['Zeit_df1'],'DO (mg/l)'].values

# Temperaturen und Konzentrationen aus df2 (nach Verschiebung) zu df_paar hinzufuegen
df_paar_13['Temp_df3'] = df3.loc[df_paar_13['Zeit_df3'],'T (deg C)'].values
df_paar_13['Konz_df3'] = df3.loc[df_paar_13['Zeit_df3'],'DO (mg/l)'].values

# Saettigungskonzentration aus den Temperaturdaten berechnen
def c_sat(T):                # Saettigungskonzentration [mg/L]
    return 468/(31.6+T)

# Saettigungskonzentration als neue Spalte dem Datensatz hinzufuegen
df_paar_13['Saettigungskonz_df1 [mg/L]'] = c_sat(df_paar_13['Temp_df1'])
df_paar_13['Saettigungskonz_df3 [mg/L]'] = c_sat(df_paar_13['Temp_df3'])

# Spalte mit Saettigungsdefizit hinzufuegen
df_paar_13['Saettigungsdefizit_df1'] = df_paar_13['Saettigungskonz_df1 [mg/L]']-df_paar_13['Konz_df1']
df_paar_13['Saettigungsdefizit_df3'] = df_paar_13['Saettigungskonz_df3 [mg/L]']-df_paar_13['Konz_df3']

# Spalte mit dem Mittelwert der Zeit aus beiden Datensaetzen hinzufuegen
df_paar_13['Zeit_mittel'] = df_paar_13[['Zeit_df1','Zeit_df3']].mean(axis=1)

# Mittelwert fuer das Saettigungsdefizit aus beiden Datensaetzen berechnen
df_paar_13['Saettigungsdefizitmittelwert'] = (df_paar_13['Saettigungsdefizit_df1']+df_paar_13['Saettigungsdefizit_df3'])/2

# Saettigungsdefizit gegen Zeit plotten
plt.figure(figsize=(8,6))
plt.plot(df_paar_13['Zeit_mittel'], df_paar_13['Saettigungsdefizitmittelwert'])
plt.title('Saettigungsdefizit fuer Messabschnitt 1-3')
plt.xlabel('\nZeit',fontsize=18)
plt.ylabel(r'Saettigungsdefizit $c_\mathrm{sat}-c~[\mathrm{mg ~ L^{-1}}]$',fontsize=18)
plt.ylim(1,4)
plt.grid(True)
plt.tick_params(axis='both',labelsize=16) 
ax = plt.gca()
ax.set_xlim(start,ende)
ax.set_xticks(ticks)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m\n%H:%M'))
plt.tight_layout()
plt.show()

#%% 

## Messabschnitt M1-M3 - Nacht

# Neue Spalte in Dataframe einfuegen, um rauszufiltern, ob der Zeitpunkt in der Nacht liegt
df_paar_13['ist_Nacht'] = False

# Schleife, um dies bei jedem einzelnen Tag zu ueberpruefen
for tag in df_paar_13['Zeit_df1'].dt.normalize().unique():
    s = sun(tuebingen.observer,date=tag.date(),tzinfo=tuebingen.timezone)
    sunrise = s['sunrise']
    sunset = s['sunset']
    
    # Daten direkt vor Sonnenaufgang nicht miteinbeziehen
    sunrise_adj = sunrise - timedelta(hours=2)
    
    # Alle Zeitpunkte markieren, die ausserhalb von Sonnenaufgang/-untergang liegen
    mask = (df_paar_13['Zeit_df1'].dt.date == tag.date()) & ((df_paar_13['Zeit_df1'] < sunrise_adj) | (df_paar_13['Zeit_df1'] > sunset))
    df_paar_13.loc[mask,'ist_Nacht'] = True

# Neuen Dataframe nur mit den Nachtdaten definieren
df_paar_nacht_13 = df_paar_13[df_paar_13['ist_Nacht']].copy()

# Spalte wieder loeschen
df_paar_nacht_13.drop(columns='ist_Nacht',inplace=True)

# Mittelwert der Zeit
df_paar_nacht_13['Zeit_mittel'] = df_paar_nacht_13[['Zeit_df1','Zeit_df3']].mean(axis=1)

# Alle Daten vor und nach der Tracernacht entfernen
start = pd.Timestamp("2025-08-06 09:00:00",tz="Europe/Berlin")
end = pd.Timestamp("2025-08-10 12:00:00",tz="Europe/Berlin")
df_paar_nacht_13 = df_paar_nacht_13[(df_paar_nacht_13['Zeit_mittel'] < start) | (df_paar_nacht_13['Zeit_mittel'] > end)]

start = pd.Timestamp("2025-08-11 12:00:00",tz="Europe/Berlin")
end = pd.Timestamp("2025-08-15 16:00:00",tz="Europe/Berlin")
df_paar_nacht_13 = df_paar_nacht_13[(df_paar_nacht_13['Zeit_mittel'] < start) | (df_paar_nacht_13['Zeit_mittel'] > end)]

# Mittelwert fuer das Saettigungsdefizit aus beiden Datensaetzen berechnen
df_paar_nacht_13['Saettigungsdefizitmittelwert'] = (df_paar_nacht_13['Saettigungsdefizit_df1']+df_paar_nacht_13['Saettigungsdefizit_df3'])/2

# r_tot berechnen
df_paar_nacht_13['r_tot'] = -(((df_paar_nacht_13['Saettigungsdefizit_df3']-df_paar_nacht_13['Saettigungsdefizit_df1'])/fliesszeit_13)-((df_paar_nacht_13['Saettigungskonz_df3 [mg/L]']-df_paar_nacht_13['Saettigungskonz_df1 [mg/L]'])/fliesszeit_13))

# Parameter gegen die Zeit plotten
plt.figure()
plt.subplot(2,1,1)
plt.plot(df_paar_nacht_13['Zeit_mittel'],df_paar_nacht_13['r_tot'],'.')
plt.xlabel('Zeit')
plt.ylabel(r'$r_{\mathrm{tot}}$ $\left[\frac{\mathrm{mg}}{\mathrm{L} \cdot \mathrm{s}}\right]$')
plt.xticks(rotation=45)
plt.subplot(2,1,2)
plt.plot(df_paar_nacht_13['Zeit_mittel'],df_paar_nacht_13['Saettigungsdefizitmittelwert'],'.')
plt.xlabel('Zeit')
plt.ylabel(r'Saettigungsdefizit $\left[\frac{\mathrm{mg}}{\mathrm{L}}\right]$')
plt.xticks(rotation=45)

# Lineare Regression
k2, r_zehr = np.polyfit(df_paar_nacht_13['Saettigungsdefizitmittelwert'],df_paar_nacht_13['r_tot'], 1)

# Residuen berechnen
residuals = df_paar_nacht_13['r_tot'] - (k2*df_paar_nacht_13['Saettigungsdefizitmittelwert'] + r_zehr)
sigma2 = np.sum(residuals**2) / (len(df_paar_nacht_13) - 2)

# Hilfsgroessen definieren
x = df_paar_nacht_13['Saettigungsdefizitmittelwert']
x_mean = np.mean(x)
Sxx = np.sum((x - x_mean)**2)
n = len(x)

# Standardfehler berechnen
sigma_k2 = np.sqrt(sigma2 / Sxx)
sigma_r_zehr = np.sqrt(sigma2 * (1/n + x_mean**2 / Sxx))

# Werte fuer die Gerade berechnen
x = np.linspace(df_paar_nacht_13['Saettigungsdefizitmittelwert'].min(),df_paar_nacht_13['Saettigungsdefizitmittelwert'].max(),100)
y = k2 * x + r_zehr


## Unsicherheitsbereich einfuegen
# Abweichungen und Standardabweichung
abweichung = df_paar_nacht_13['r_tot']-(k2*df_paar_nacht_13['Saettigungsdefizitmittelwert']+r_zehr)
sigma = np.std(abweichung)

# Unsicherheitsbereich (nur Parameter)
n = len(df_paar_nacht_13)
x_mean = np.mean(df_paar_nacht_13['Saettigungsdefizitmittelwert'])
standardfehler_regression = sigma*np.sqrt(1/n+(x-x_mean)**2/np.sum((df_paar_nacht_13['Saettigungsdefizitmittelwert']-x_mean)**2))
ci_upper = y + 1.96 * standardfehler_regression
ci_lower = y - 1.96 * standardfehler_regression

# Unsicherheitsbereich (Parameter + Messfehler)
y_upper = y + sigma
y_lower = y - sigma

# Plot mit linearer Regression erstellen
plt.figure(figsize=(9,6))
plt.plot(df_paar_nacht_13['Saettigungsdefizitmittelwert'],df_paar_nacht_13['r_tot'],'.',markersize=3)
plt.plot(x,y,label=f'Regression: y = {k2:.2e}x + {r_zehr:.2e}',color='purple')
plt.tick_params(axis='both',labelsize=13) 

plt.fill_between(x,y_lower,y_upper,color='lightblue',alpha=0.4,label='Parameter- und Messfehlerunsicherheit')
plt.fill_between(x,ci_lower,ci_upper,color='darkblue',alpha=0.3,label='Parameterunsicherheit')

plt.xlabel(r'$c_\mathrm{sat} - c ~ [\mathrm{mg ~ L^{-1}}]$',fontsize=14)
plt.ylabel(r'$r_{\mathrm{tot}}$ $[\mathrm{mg ~ L^{-1} ~ s^{-1}}]$',fontsize=14)
plt.legend(fontsize=13) 
plt.grid(True)
plt.xlim(2.92,3.3)
plt.ylim(0.000033,0.00012)
plt.show()

# Werte fuer k2 und r_zehr ausgeben lassen
print("\nAbschnitt M1-M3")
print("\nParameter aus Nachtdaten:")
print(f"k2 = {k2:.3e} ± {sigma_k2:.3e}")
print(f"r_zehr = {r_zehr:.3e} ± {sigma_r_zehr:.3e}")

#%%
# Messabschnitt M1-M3 - Tag

# Neue Spalte in Dataframe einfuegen, um rauszufiltern, ob der Zeitpunkt am Tag ist
df_paar_13['ist_Tag'] = False  

# Schleife, um dies bei jedem einzelnen Tag zu ueberpruefen
for tag in df_paar_13['Zeit_df1'].dt.normalize().unique():
    s = sun(tuebingen.observer,date=tag.date(),tzinfo=tuebingen.timezone)
    sunrise = s['sunrise']
    sunset = s['sunset']
    
    # Daten direkt vor Sonnenaufgang nicht miteinbeziehen
    sunrise_adj = sunrise - timedelta(hours=2)
    
    # Alle Zeitpunkte markieren, die innerhalb von Sonnenaufgang/-untergang liegen
    mask = (df_paar_13['Zeit_df1'].dt.date == tag.date()) & ((df_paar_13['Zeit_df1'] >= sunrise_adj) & (df_paar_13['Zeit_df1'] <= sunset))
    df_paar_13.loc[mask,'ist_Tag'] = True

# Neuen Dataframe nur mit den Tagesdaten erstellen
df_paar_tag_13 = df_paar_13[df_paar_13['ist_Tag']].copy()

# Spalte wieder loeschen
df_paar_tag_13.drop(columns='ist_Tag',inplace=True)

# Mittelwert der Zeit
df_paar_tag_13['Zeit_mittel'] = df_paar_tag_13[['Zeit_df1','Zeit_df3']].mean(axis=1)

# Daten vor und nach der Tracernacht loeschen
start = pd.Timestamp("2025-08-06 09:00:00",tz="Europe/Berlin")
end = pd.Timestamp("2025-08-09 06:00:00",tz="Europe/Berlin")
df_paar_tag_13 = df_paar_tag_13[(df_paar_tag_13['Zeit_mittel'] < start) | (df_paar_tag_13['Zeit_mittel'] > end)]

start = pd.Timestamp("2025-08-11 22:00:00",tz="Europe/Berlin")
end = pd.Timestamp("2025-08-15 12:00:00",tz="Europe/Berlin")
df_paar_tag_13 = df_paar_tag_13[(df_paar_tag_13['Zeit_mittel'] < start) | (df_paar_tag_13['Zeit_mittel'] > end)]

# Naechstgelegene Zeit von df_s zu df_paar_tag finden und hinzufuegen
strahlungs_idx = df_s.index.get_indexer(df_paar_tag_13['Zeit_mittel'],method='nearest')
df_paar_tag_13['Strahlung'] = df_s.iloc[strahlungs_idx]['m13'].values

# r_tot berechnen
df_paar_tag_13['r_tot'] = -(((df_paar_tag_13['Saettigungsdefizit_df3']-df_paar_tag_13['Saettigungsdefizit_df1'])/fliesszeit_13)-((df_paar_tag_13['Saettigungskonz_df3 [mg/L]']-df_paar_tag_13['Saettigungskonz_df1 [mg/L]'])/fliesszeit_13))

# Mittelwert fuer das Saettigungsdefizit aus beiden Dataframes berechnen 
df_paar_tag_13['Saettigungsdefizitmittelwert'] = (df_paar_tag_13['Saettigungsdefizit_df1']+df_paar_tag_13['Saettigungsdefizit_df3'])/2

# r_photo berechnen
df_paar_tag_13['r_photo'] = df_paar_tag_13['r_tot']-r_zehr-k2*df_paar_tag_13['Saettigungsdefizitmittelwert']


## Lineare Regression
# Lineare Regression durch den Ursprung
k_photo = np.sum(df_paar_tag_13['Strahlung']*df_paar_tag_13['r_photo'])/np.sum(df_paar_tag_13['Strahlung']**2)

# Residuen berechnen
residuals = df_paar_tag_13['r_photo'] - k_photo*df_paar_tag_13['Strahlung']
sigma2 = np.sum(residuals**2) / (len(df_paar_tag_13) - 1)

# Standardfehler berechnen
sigma_k_photo = np.sqrt(sigma2 / np.sum(df_paar_tag_13['Strahlung']**2))

# Werte fuer die Gerade berechnen
x_tag = np.linspace(df_paar_tag_13['Strahlung'].min(),df_paar_tag_13['Strahlung'].max(),100)
y_tag = k_photo * x_tag

## Regression mit Michaelis-Menten

# Anfangsschaetzungen fuer r_photo_max und R_0.5 (aus ODE Hausaufgabe)
schaetzung = [10**(-3),100]

# Fit durchfuehren
params, covparams = curve_fit(michaelis_menten,df_paar_tag_13['Strahlung'],df_paar_tag_13['r_photo'],p0=schaetzung)
r_photo_max, R_halb = params

y_mm = michaelis_menten(df_paar_tag_13['Strahlung'],r_photo_max,R_halb)


## Unsicherheitsbereiche einfuegen
# Abweichungen und Standardabweichung fuer lineare Regression
abweichung_tag = df_paar_tag_13['r_photo']-(k_photo*df_paar_tag_13['Strahlung'])
sigma_tag = np.std(abweichung_tag)

abweichung_tag_mm = df_paar_tag_13['r_photo']-y_mm
sigma_tag_mm = np.sqrt(np.sum(abweichung_tag**2)/(len(y_mm)-2))

y_mm = michaelis_menten(x_tag,r_photo_max,R_halb)

# Unsicherheitsbereich (nur Parameter) fuer lineare Regression
n_tag = len(df_paar_tag_13)
x_mean_tag = np.mean(df_paar_tag_13['Strahlung'])
standardfehler_regression_tag = sigma_tag*np.sqrt(1/n_tag+(x_tag-x_mean_tag)**2/np.sum((df_paar_tag_13['Strahlung']-x_mean_tag)**2))
ci_tag_upper = y_tag + 1.96 * standardfehler_regression_tag
ci_tag_lower = y_tag - 1.96 * standardfehler_regression_tag

# Unsicherheitsbereich (Parameter + Messfehler)
y_tag_upper = y_tag + sigma_tag
y_tag_lower = y_tag - sigma_tag

# Standardabweichungen der Parameter aus Kovarianzmatrix
perr = np.sqrt(np.diag(covparams))  

mm_std = mm_error_propagation(x_tag,r_photo_max,R_halb,covparams)
ci_upper_mm = y_mm + 1.96 * mm_std
ci_lower_mm = y_mm - 1.96 * mm_std

# Gesamtunsicherheitsbereich (Parameter + Messfehler)
y_upper_mm = y_mm + 1.96*np.sqrt(sigma_tag_mm**2+mm_std**2)
y_lower_mm = y_mm - 1.96*np.sqrt(sigma_tag_mm**2+mm_std**2)

# Tagesdaten mit Unsicherheitsbereichen plotten
plt.figure(figsize=(10,7))
plt.plot(df_paar_tag_13['Strahlung'],df_paar_tag_13['r_photo'],'.',markersize=3)
plt.tick_params(axis='both',labelsize=15)

# Lineare Regression
plt.plot(x_tag,y_tag,'r-',label=f'Lineare Regression: y = {k_photo:.2e}x')
plt.fill_between(x_tag,y_tag_lower,y_tag_upper,color='pink',alpha=0.4,label='\nLineare Regression: Parameter- \nund Messfehlerunsicherheit')
plt.fill_between(x_tag,ci_tag_lower,ci_tag_upper,color='red',alpha=0.5,label='\nLineare Regression: \nParameterunsicherheit')

# Michaelis-Menten
plt.plot(x_tag,y_mm,'g-',label='\nMichaelis-Menten Kinetik\n')
plt.fill_between(x_tag,y_lower_mm,y_upper_mm,color='lightgreen',alpha=0.25,label='\nMichaelis Menten: Parameter- \nund Messfehlerunsicherheit')
plt.fill_between(x_tag,ci_lower_mm,ci_upper_mm,color='green',alpha=0.35,label='\nMichaelis Menten: \nParameterunsicherheit')

plt.xlabel(r'$R$ $[\mathrm{W ~ m^{-2}}]$',fontsize=18)
plt.ylabel(r'$r_{\mathrm{photo}}$ $[\mathrm{mg ~ L^{-1} ~ s^{-1}}]$',fontsize=18)
plt.legend(loc='center left',bbox_to_anchor=(1, 0.5),ncol=1,fontsize=16)
plt.grid(True)
plt.xlim(0,415)
plt.ylim(-0.00005,0.0003)
plt.show()

# Parameter ausgeben lassen
print("\nParameter aus Tagdaten:")

print("Lineare Regression:")
print(f"k_photo = {k_photo:.3e} ± {sigma_k_photo:.3e}")

print("\nMichaelis-Menten Parameter:")
print(f"r_photo_max = {r_photo_max:.3e} ± {perr[0]:.3e}")
print(f"R_0.5 = {R_halb:.3f} ± {perr[1]:.3f}\n")

# Werte als Spalte einfuegen
df_param["M1-M3"] = [k2, r_zehr, k_photo, r_photo_max, R_halb]


#%%

## Messabschnitt M2-M3

# Fliesszeit definieren und als Zeitformat darstellen
fliesszeit_2 = 73.06 * 60    # Fliesszeit in Sekunden
fliesszeit_td_2 = pd.to_timedelta(fliesszeit_2,unit='s')

# Berechnung des Zeitpunkts, an dem das betrachtete Wasserpaket an der naechsten Station ankommt
df2['Zeit_nach_Fluss'] = df2.index + fliesszeit_td_2

# In df2 Zeitpunkt von ankommendem Wasserpaket finden
idx = df3.index.get_indexer(df2['Zeit_nach_Fluss'],method='nearest')
df3_zeiten = df3.index[idx]

# Zeitpunkte von Wasserpaket an Messstelle 1 und 2 kombinieren
df_paar_2 = pd.DataFrame({'Zeit_df2':df2.index,'Zeit_df3':df3_zeiten})

# Temperaturen und Konzentrationen aus df1 zu df_paar hinzufuegen
df_paar_2['Temp_df2'] = df2.loc[df_paar_2['Zeit_df2'],'T (deg C)'].values
df_paar_2['Konz_df2'] = df2.loc[df_paar_2['Zeit_df2'],'DO (mg/l)'].values

# Temperaturen und Konzentrationen aus df2 (nach Verschiebung) zu df_paar hinzufuegen
df_paar_2['Temp_df3'] = df3.loc[df_paar_2['Zeit_df3'],'T (deg C)'].values
df_paar_2['Konz_df3'] = df3.loc[df_paar_2['Zeit_df3'],'DO (mg/l)'].values

# Saettigungskonzentration aus den Temperaturdaten berechnen
def c_sat(T):                # Saettigungskonzentration [mg/L]
    return 468/(31.6+T)

# Saettigungskonzentration als neue Spalte dem Datensatz hinzufuegen
df_paar_2['Saettigungskonz_df2 [mg/L]'] = c_sat(df_paar_2['Temp_df2'])
df_paar_2['Saettigungskonz_df3 [mg/L]'] = c_sat(df_paar_2['Temp_df3'])

# Spalte mit Saettigungsdefizit hinzufuegen
df_paar_2['Saettigungsdefizit_df2'] = df_paar_2['Saettigungskonz_df2 [mg/L]']-df_paar_2['Konz_df2']
df_paar_2['Saettigungsdefizit_df3'] = df_paar_2['Saettigungskonz_df3 [mg/L]']-df_paar_2['Konz_df3']

# Spalte mit dem Mittelwert der Zeit aus beiden Datensaetzen hinzufuegen
df_paar_2['Zeit_mittel'] = df_paar_2[['Zeit_df2','Zeit_df3']].mean(axis=1)

# Mittelwert fuer das Saettigungsdefizit aus beiden Datensaetzen berechnen
df_paar_2['Saettigungsdefizitmittelwert'] = (df_paar_2['Saettigungsdefizit_df2']+df_paar_2['Saettigungsdefizit_df3'])/2

# Saettigungsdefizit gegen Zeit plotten
plt.figure(figsize=(8,6))
plt.plot(df_paar_2['Zeit_df2'],df_paar_2['Saettigungsdefizit_df2'])
plt.title('Saettigungsdefizit fuer Messabschnitt 2')
plt.xlabel('\nZeit',fontsize=18)
plt.ylabel(r'Saettigungsdefizit $c_\mathrm{sat}-c~[\mathrm{mg ~ L^{-1}}]$',fontsize=18)
plt.ylim(1,4)
plt.grid(True)
plt.tick_params(axis='both',labelsize=16) 
ax = plt.gca()
ax.set_xlim(start,ende)
ax.set_xticks(ticks)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m\n%H:%M'))
plt.tight_layout()
plt.show()

#%% 

## Messabschnitt M2-M3 - Nacht

# Neue Spalte in Dataframe einfuegen, um rauszufiltern, ob der Zeitpunkt in der Nacht liegt
df_paar_2['ist_Nacht'] = False

# Schleife, um dies bei jedem einzelnen Tag zu ueberpruefen
for tag in df_paar_2['Zeit_df2'].dt.normalize().unique():
    s = sun(tuebingen.observer,date=tag.date(),tzinfo=tuebingen.timezone)
    sunrise = s['sunrise']
    sunset = s['sunset']
    
    # Daten direkt vor Sonnenaufgang nicht miteinbeziehen
    sunrise_adj = sunrise - timedelta(hours=2)
    
    # Alle Zeitpunkte markieren, die ausserhalb von Sonnenaufgang/-untergang liegen
    mask = (df_paar_2['Zeit_df2'].dt.date == tag.date()) & ((df_paar_2['Zeit_df2'] < sunrise_adj) | (df_paar_2['Zeit_df2'] > sunset))
    df_paar_2.loc[mask, 'ist_Nacht'] = True

# Neuen Dataframe nur mit den Nachtdaten definieren
df_paar_nacht_2 = df_paar_2[df_paar_2['ist_Nacht']].copy()

# Spalte wieder loeschen
df_paar_nacht_2.drop(columns='ist_Nacht',inplace=True)

# Mittelwert der Zeit
df_paar_nacht_2['Zeit_mittel'] = df_paar_nacht_2[['Zeit_df2','Zeit_df3']].mean(axis=1)

# Daten vor und nach der Tracernacht loeschen
start = pd.Timestamp("2025-08-06 09:00:00",tz="Europe/Berlin")
end = pd.Timestamp("2025-08-10 12:00:00",tz="Europe/Berlin")
df_paar_nacht_2 = df_paar_nacht_2[(df_paar_nacht_2['Zeit_mittel'] < start) | (df_paar_nacht_2['Zeit_mittel'] > end)]

start = pd.Timestamp("2025-08-11 12:00:00",tz="Europe/Berlin")
end = pd.Timestamp("2025-08-15 16:00:00",tz="Europe/Berlin")
df_paar_nacht_2 = df_paar_nacht_2[(df_paar_nacht_2['Zeit_mittel'] < start) | (df_paar_nacht_2['Zeit_mittel'] > end)]

# Mittelwert fuer das Saettigungsdefizit aus beiden Datensaetzen berechnen
df_paar_nacht_2['Saettigungsdefizitmittelwert'] = (df_paar_nacht_2['Saettigungsdefizit_df2']+df_paar_nacht_2['Saettigungsdefizit_df3'])/2

# r_tot berechnen
df_paar_nacht_2['r_tot'] = -(((df_paar_nacht_2['Saettigungsdefizit_df3']-df_paar_nacht_2['Saettigungsdefizit_df2'])/fliesszeit_2)-((df_paar_nacht_2['Saettigungskonz_df3 [mg/L]']-df_paar_nacht_2['Saettigungskonz_df2 [mg/L]'])/fliesszeit_2))

# Parameter gegen die Zeit plotten
plt.figure()
plt.subplot(2,1,1)
plt.plot(df_paar_nacht_2['Zeit_mittel'],df_paar_nacht_2['r_tot'],'.')
plt.xlabel('Zeit')
plt.ylabel(r'$r_{\mathrm{tot}}$ $\left[\frac{\mathrm{mg}}{\mathrm{L} \cdot \mathrm{s}}\right]$')
plt.xticks(rotation=45)
plt.subplot(2,1,2)
plt.plot(df_paar_nacht_2['Zeit_mittel'],df_paar_nacht_2['Saettigungsdefizitmittelwert'],'.')
plt.xlabel('Zeit')
plt.ylabel(r'Saettigungsdefizit $\left[\frac{\mathrm{mg}}{\mathrm{L}}\right]$')
plt.xticks(rotation=45)

# Lineare Regression
k2, r_zehr = np.polyfit(df_paar_nacht_2['Saettigungsdefizitmittelwert'],df_paar_nacht_2['r_tot'], 1)

# Residuen berechnen
residuals = df_paar_nacht_2['r_tot'] - (k2*df_paar_nacht_2['Saettigungsdefizitmittelwert'] + r_zehr)
sigma2 = np.sum(residuals**2) / (len(df_paar_nacht_2) - 2)

# Hilfsgroessen definieren
x = df_paar_nacht_2['Saettigungsdefizitmittelwert']
x_mean = np.mean(x)
Sxx = np.sum((x - x_mean)**2)
n = len(x)

# Standardfehler berechnen
sigma_k2 = np.sqrt(sigma2 / Sxx)
sigma_r_zehr = np.sqrt(sigma2 * (1/n + x_mean**2 / Sxx))

# Werte fuer die Gerade berechnen
x = np.linspace(df_paar_nacht_2['Saettigungsdefizitmittelwert'].min(),df_paar_nacht_2['Saettigungsdefizitmittelwert'].max(),100)
y = k2 * x + r_zehr


## Unsicherheitsbereich einfuegen
# Abweichungen und Standardabweichung
abweichung = df_paar_nacht_2['r_tot']-(k2*df_paar_nacht_2['Saettigungsdefizitmittelwert']+r_zehr)
sigma = np.std(abweichung)

# Unsicherheitsbereich (nur Parameter)
n = len(df_paar_nacht_2)
x_mean = np.mean(df_paar_nacht_2['Saettigungsdefizitmittelwert'])
standardfehler_regression = sigma*np.sqrt(1/n+(x-x_mean)**2/np.sum((df_paar_nacht_2['Saettigungsdefizitmittelwert']-x_mean)**2))
ci_upper = y + 1.96 * standardfehler_regression
ci_lower = y - 1.96 * standardfehler_regression

# Unsicherheitsbereich (Parameter + Messfehler)
y_upper = y + sigma
y_lower = y - sigma

# Plot mit linearer Regression erstellen
plt.figure(figsize=(9,6))
plt.plot(df_paar_nacht_2['Saettigungsdefizitmittelwert'],df_paar_nacht_2['r_tot'],'.',markersize=3)
plt.plot(x,y,label=f'Regression: y = {k2:.2e}x + {r_zehr:.2e}',color='purple')
plt.tick_params(axis='both',labelsize=13) 

plt.fill_between(x,y_lower,y_upper,color='lightblue',alpha=0.4,label='Parameter- und Messfehlerunsicherheit')
plt.fill_between(x,ci_lower,ci_upper,color='darkblue',alpha=0.3,label='Parameterunsicherheit ')

plt.xlabel(r'$c_\mathrm{sat} - c ~ [\mathrm{mg ~ L^{-1}}]$',fontsize=14)
plt.ylabel(r'$r_{\mathrm{tot}}$ $[\mathrm{mg ~ L^{-1} ~ s^{-1}}]$',fontsize=14)
plt.legend(fontsize=13) 
plt.grid(True)
plt.xlim(2.905,3.162)
plt.ylim(0.00007,0.00015)
plt.show()

# Werte fuer k2 und r_zehr ausgeben lassen
print("\nAbschnitt M2-M3")
print("\nParameter aus Nachtdaten:")
print(f"k2 = {k2:.3e} ± {sigma_k2:.3e}")
print(f"r_zehr = {r_zehr:.3e} ± {sigma_r_zehr:.3e}")

#%%
# Messabschnitt M2-M3 - Tag

# Neue Spalte in Dataframe einfuegen, um rauszufiltern, ob der Zeitpunkt am Tag ist
df_paar_2['ist_Tag'] = False  

# Schleife, um dies bei jedem einzelnen Tag zu ueberpruefen
for tag in df_paar_2['Zeit_df2'].dt.normalize().unique():
    s = sun(tuebingen.observer,date=tag.date(),tzinfo=tuebingen.timezone)
    sunrise = s['sunrise']
    sunset = s['sunset']
    
    # Daten direkt vor Sonnenaufgang nicht miteinbeziehen
    sunrise_adj = sunrise - timedelta(hours=2)
    
    # Alle Zeitpunkte markieren, die innerhalb von Sonnenaufgang/-untergang liegen
    mask = (df_paar_2['Zeit_df2'].dt.date == tag.date()) & ((df_paar_2['Zeit_df2'] >= sunrise_adj) & (df_paar_2['Zeit_df2'] <= sunset))
    df_paar_2.loc[mask,'ist_Tag'] = True

# Neuen Dataframe nur mit den Tagesdaten erstellen
df_paar_tag_2 = df_paar_2[df_paar_2['ist_Tag']].copy()

# Spalte wieder loeschen
df_paar_tag_2.drop(columns='ist_Tag',inplace=True)

# Mittelwert der Zeit
df_paar_tag_2['Zeit_mittel'] = df_paar_tag_2[['Zeit_df2','Zeit_df3']].mean(axis=1)

# Daten vor und nach der Tracernacht loeschen
start = pd.Timestamp("2025-08-06 09:00:00",tz="Europe/Berlin")
end = pd.Timestamp("2025-08-09 06:00:00",tz="Europe/Berlin")
df_paar_tag_2 = df_paar_tag_2[(df_paar_tag_2['Zeit_mittel'] < start) | (df_paar_tag_2['Zeit_mittel'] > end)]

start = pd.Timestamp("2025-08-11 22:00:00",tz="Europe/Berlin")
end = pd.Timestamp("2025-08-15 12:00:00",tz="Europe/Berlin")
df_paar_tag_2 = df_paar_tag_2[(df_paar_tag_2['Zeit_mittel'] < start) | (df_paar_tag_2['Zeit_mittel'] > end)]

# Naechstgelegene Zeit von df_s zu df_paar_tag finden und hinzufuegen
strahlungs_idx = df_s.index.get_indexer(df_paar_tag_2['Zeit_mittel'],method='nearest')
df_paar_tag_2['Strahlung'] = df_s.iloc[strahlungs_idx]['m3'].values

# r_tot berechnen
df_paar_tag_2['r_tot'] = -(((df_paar_tag_2['Saettigungsdefizit_df3']-df_paar_tag_2['Saettigungsdefizit_df2'])/fliesszeit_2)-((df_paar_tag_2['Saettigungskonz_df3 [mg/L]']-df_paar_tag_2['Saettigungskonz_df2 [mg/L]'])/fliesszeit_2))

# Mittelwert fuer das Saettigungsdefizit aus beiden Dataframes berechnen 
df_paar_tag_2['Saettigungsdefizitmittelwert'] = (df_paar_tag_2['Saettigungsdefizit_df2']+df_paar_tag_2['Saettigungsdefizit_df3'])/2

# r_photo berechnen
df_paar_tag_2['r_photo'] = df_paar_tag_2['r_tot']-r_zehr-k2*df_paar_tag_2['Saettigungsdefizitmittelwert']


## Lineare Regression
# Lineare Regression durch den Ursprung
k_photo = np.sum(df_paar_tag_2['Strahlung']*df_paar_tag_2['r_photo'])/np.sum(df_paar_tag_2['Strahlung']**2)

# Residuen berechnen
residuals = df_paar_tag_2['r_photo'] - k_photo*df_paar_tag_2['Strahlung']
sigma2 = np.sum(residuals**2) / (len(df_paar_tag_2) - 1)

# Standardfehler von k_photo
sigma_k_photo = np.sqrt(sigma2 / np.sum(df_paar_tag_2['Strahlung']**2))

# Werte fuer die Gerade berechnen
x_tag = np.linspace(df_paar_tag_2['Strahlung'].min(),df_paar_tag_2['Strahlung'].max(),100)
y_tag = k_photo * x_tag

## Regression mit Michaelis-Menten

# Anfangsschaetzungen fuer r_photo_max und R_0.5 (aus ODE Hausaufgabe)
schaetzung = [10**(-3),100]

# Fit durchfuehren
params, covparams = curve_fit(michaelis_menten,df_paar_tag_2['Strahlung'],df_paar_tag_2['r_photo'],p0=schaetzung)
r_photo_max, R_halb = params

y_mm = michaelis_menten(df_paar_tag_2['Strahlung'],r_photo_max,R_halb)

## Unsicherheitsbereiche einfuegen
# Abweichungen und Standardabweichung fuer lineare Regression
abweichung_tag = df_paar_tag_2['r_photo']-(k_photo*df_paar_tag_2['Strahlung'])
sigma_tag = np.std(abweichung_tag)

abweichung_tag_mm = df_paar_tag_2['r_photo'] - y_mm
sigma_tag_mm = np.sqrt(np.sum(abweichung_tag_mm**2)/(len(y_mm)-2))

y_mm = michaelis_menten(x_tag,r_photo_max,R_halb)

# Unsicherheitsbereich (nur Parameter) fuer lineare Regression
n_tag = len(df_paar_tag_2)
x_mean_tag = np.mean(df_paar_tag_2['Strahlung'])
standardfehler_regression_tag = sigma_tag*np.sqrt(1/n_tag+(x_tag-x_mean_tag)**2/np.sum((df_paar_tag_2['Strahlung']-x_mean_tag)**2))
ci_tag_upper = y_tag + 1.96 * standardfehler_regression_tag
ci_tag_lower = y_tag - 1.96 * standardfehler_regression_tag

# Unsicherheitsbereich (Parameter + Messfehler)
y_tag_upper = y_tag + sigma_tag
y_tag_lower = y_tag - sigma_tag

# Standardabweichungen der Parameter aus Kovarianzmatrix
perr = np.sqrt(np.diag(covparams))  

mm_std = mm_error_propagation(x_tag,r_photo_max,R_halb,covparams)
ci_upper_mm = y_mm + 1.96 * mm_std
ci_lower_mm = y_mm - 1.96 * mm_std

# Gesamtunsicherheitsbereich (Parameter + Messfehler)
y_upper_mm = y_mm + 1.96 * np.sqrt(sigma_tag_mm**2 + mm_std**2)
y_lower_mm = y_mm - 1.96 * np.sqrt(sigma_tag_mm**2 + mm_std**2)

# Tagesdaten mit Unsicherheitsberichen plotten
plt.figure(figsize=(10,7))
plt.plot(df_paar_tag_2['Strahlung'],df_paar_tag_2['r_photo'],'.',markersize=3)
plt.tick_params(axis='both',labelsize=15) 

# Lineare Regression
plt.plot(x_tag,y_tag,'r-',label=f'Lineare Regression: y = {k_photo:.2e}x')
plt.fill_between(x_tag,y_tag_lower,y_tag_upper,color='pink',alpha=0.4,label='\nLineare Regression: Parameter- \nund Messfehlerunsicherheit')
plt.fill_between(x_tag,ci_tag_lower,ci_tag_upper,color='red',alpha=0.5,label='\nLineare Regression: \nParameterunsicherheit')

# Michaelis-Menten
plt.plot(x_tag,y_mm,'g-',label='\nMichaelis-Menten Kinetik\n')
plt.fill_between(x_tag,y_lower_mm,y_upper_mm,color='lightgreen',alpha=0.25,label='\nMichaelis Menten: Parameter- \nund Messfehlerunsicherheit')
plt.fill_between(x_tag,ci_lower_mm,ci_upper_mm,color='green',alpha=0.35, label='\nMichaelis Menten: \nParameterunsicherheit')

plt.xlabel(r'$R$ $[\mathrm{W ~ m^{-2}}]$',fontsize=18)
plt.ylabel(r'$r_{\mathrm{photo}}$ $[\mathrm{mg ~ L^{-1} ~ s^{-1}}]$',fontsize=18)
plt.legend(loc='center left',bbox_to_anchor=(1, 0.5),ncol=1,fontsize=16)
plt.grid(True)
plt.xlim(0,315)
plt.ylim(-0.00005,0.0003)
plt.show()

# Parameter ausgeben lassen
print("\nParameter aus Tagdaten:")

print("Lineare Regression:")
print(f"k_photo = {k_photo:.3e} ± {sigma_k_photo:.3e}")

print("\nMichaelis-Menten Parameter:")
print(f"r_photo_max = {r_photo_max:.3e} ± {perr[0]:.3e}")
print(f"R_0.5 = {R_halb:.3f} ± {perr[1]:.3f}\n")


# Werte als Spalte einfuegen
df_param["M2-M3"] = [k2, r_zehr, k_photo, r_photo_max, R_halb]


#%%

## Messabschnitt M3-M4

# Fliesszeit definieren und als Zeitformat darstellen
fliesszeit_3 = 54.54 * 60    # Fliesszeit in Sekunden
fliesszeit_td_3 = pd.to_timedelta(fliesszeit_3,unit='s')

# Berechnung des Zeitpunkts, an dem das betrachtete Wasserpaket an der naechsten Station ankommt
df8['Zeit_nach_Fluss'] = df8.index + fliesszeit_td_3

# In df2 Zeitpunkt von ankommendem Wasserpaket finden
idx = df4.index.get_indexer(df8['Zeit_nach_Fluss'],method='nearest')
df4_zeiten = df4.index[idx]

# Zeitpunkte von Wasserpaket an Messstelle 1 und 2 kombinieren
df_paar_3 = pd.DataFrame({'Zeit_df3': df8.index,'Zeit_df4': df4_zeiten})

# Temperaturen und Konzentrationen aus df1 zu df_paar hinzufuegen
df_paar_3['Temp_df3'] = df8.loc[df_paar_3['Zeit_df3'],'T (deg C)'].values
df_paar_3['Konz_df3'] = df8.loc[df_paar_3['Zeit_df3'],'DO (mg/l)'].values

# Temperaturen und Konzentrationen aus df2 (nach Verschiebung) zu df_paar hinzufuegen
df_paar_3['Temp_df4'] = df4.loc[df_paar_3['Zeit_df4'],'T (deg C)'].values
df_paar_3['Konz_df4'] = df4.loc[df_paar_3['Zeit_df4'],'DO (mg/l)'].values

# Saettigungskonzentration aus den Temperaturdaten berechnen
def c_sat(T):                # Saettigungskonzentration [mg/L]
    return 468/(31.6+T)

# Saettigungskonzentration als neue Spalte dem Datensatz hinzufuegen
df_paar_3['Saettigungskonz_df3 [mg/L]'] = c_sat(df_paar_3['Temp_df3'])
df_paar_3['Saettigungskonz_df4 [mg/L]'] = c_sat(df_paar_3['Temp_df4'])

# Spalte mit Saettigungsdefizit hinzufuegen
df_paar_3['Saettigungsdefizit_df3'] = df_paar_3['Saettigungskonz_df3 [mg/L]']-df_paar_3['Konz_df3']
df_paar_3['Saettigungsdefizit_df4'] = df_paar_3['Saettigungskonz_df4 [mg/L]']-df_paar_3['Konz_df4']

# Spalte mit dem Mittelwert der Zeit aus beiden Datensaetzen hinzufuegen
df_paar_3['Zeit_mittel'] = df_paar_3[['Zeit_df3','Zeit_df4']].mean(axis=1)

# Mittelwert fuer das Saettigungsdefizit aus beiden Datensaetzen berechnen
df_paar_3['Saettigungsdefizitmittelwert'] = (df_paar_3['Saettigungsdefizit_df3']+df_paar_3['Saettigungsdefizit_df4'])/2

# Saettigungsdefizit gegen Zeit plotten
plt.figure(figsize=(8,6))
plt.plot(df_paar_3['Zeit_df3'],df_paar_3['Saettigungsdefizit_df3'])
plt.title('Saettigungsdefizit fuer Messabschnitt 3')
plt.xlabel('\nZeit',fontsize=18)
plt.ylabel(r'Saettigungsdefizit $c_\mathrm{sat}-c~[\mathrm{mg ~ L^{-1}}]$',fontsize=18)
plt.ylim(1,4)
plt.grid(True)
plt.tick_params(axis='both', labelsize=16) 
ax = plt.gca()
ax.set_xlim(start,ende)
ax.set_xticks(ticks)
ax.xaxis.set_major_formatter(mdates.DateFormatter('%d.%m\n%H:%M'))
plt.tight_layout()
plt.show()

#%% 

## Messabschnitt M3-M4 - Nacht

# Neue Spalte in Dataframe einfuegen, um rauszufiltern, ob der Zeitpunkt in der Nacht liegt
df_paar_3['ist_Nacht'] = False

# Schleife, um dies bei jedem einzelnen Tag zu ueberpruefen
for tag in df_paar_3['Zeit_df3'].dt.normalize().unique():
    s = sun(tuebingen.observer,date=tag.date(),tzinfo=tuebingen.timezone)
    sunrise = s['sunrise']
    sunset = s['sunset']
    
    # Daten direkt vor Sonnenaufgang nicht miteinbeziehen
    sunrise_adj = sunrise - timedelta(hours=5)
    
    # Alle Zeitpunkte markieren, die ausserhalb von Sonnenaufgang/-untergang liegen
    mask = (df_paar_3['Zeit_df3'].dt.date == tag.date()) & ((df_paar_3['Zeit_df3'] < sunrise_adj) | (df_paar_3['Zeit_df3'] > sunset))
    df_paar_3.loc[mask,'ist_Nacht'] = True

# Neuen Dataframe nur mit den Nachtdaten definieren
df_paar_nacht_3 = df_paar_3[df_paar_3['ist_Nacht']].copy()

# Spalte wieder loeschen
df_paar_nacht_3.drop(columns='ist_Nacht',inplace=True)

# Mittelwert der Zeit
df_paar_nacht_3['Zeit_mittel'] = df_paar_nacht_3[['Zeit_df3','Zeit_df4']].mean(axis=1)

# Daten vor und nach der Tracernacht loeschen
start = pd.Timestamp("2025-08-06 09:00:00",tz="Europe/Berlin")
end = pd.Timestamp("2025-08-10 12:00:00",tz="Europe/Berlin")
df_paar_nacht_3 = df_paar_nacht_3[(df_paar_nacht_3['Zeit_mittel'] < start) | (df_paar_nacht_3['Zeit_mittel'] > end)]

start = pd.Timestamp("2025-08-11 12:00:00",tz="Europe/Berlin")
end = pd.Timestamp("2025-08-15 16:00:00",tz="Europe/Berlin")
df_paar_nacht_3 = df_paar_nacht_3[(df_paar_nacht_3['Zeit_mittel'] < start) | (df_paar_nacht_3['Zeit_mittel'] > end)]

# Mittelwert fuer das Saettigungsdefizit aus beiden Datensaetzen berechnen
df_paar_nacht_3['Saettigungsdefizitmittelwert'] = (df_paar_nacht_3['Saettigungsdefizit_df3']+df_paar_nacht_3['Saettigungsdefizit_df4'])/2

# r_tot berechnen
df_paar_nacht_3['r_tot'] = -(((df_paar_nacht_3['Saettigungsdefizit_df4']-df_paar_nacht_3['Saettigungsdefizit_df3'])/fliesszeit_3)-((df_paar_nacht_3['Saettigungskonz_df4 [mg/L]']-df_paar_nacht_3['Saettigungskonz_df3 [mg/L]'])/fliesszeit_3))

# Parameter gegen die Zeit plotten
plt.figure()
plt.subplot(2,1,1)
plt.plot(df_paar_nacht_3['Zeit_mittel'],df_paar_nacht_3['r_tot'],'.')
plt.xlabel('Zeit')
plt.ylabel(r'$r_{\mathrm{tot}}$ $\left[\frac{\mathrm{mg}}{\mathrm{L} \cdot \mathrm{s}}\right]$')
plt.xticks(rotation=45)
plt.subplot(2,1,2)
plt.plot(df_paar_nacht_3['Zeit_mittel'],df_paar_nacht_3['Saettigungsdefizitmittelwert'],'.')
plt.xlabel('Zeit')
plt.ylabel(r'Saettigungsdefizit $\left[\frac{\mathrm{mg}}{\mathrm{L}}\right]$')
plt.xticks(rotation=45)

# Lineare Regression
k2, r_zehr = np.polyfit(df_paar_nacht_3['Saettigungsdefizitmittelwert'],df_paar_nacht_3['r_tot'],1)

# Residuen berechnen
residuals = df_paar_nacht_3['r_tot'] - (k2*df_paar_nacht_3['Saettigungsdefizitmittelwert'] + r_zehr)
sigma2 = np.sum(residuals**2) / (len(df_paar_nacht_3) - 2)

# Hilfsgroessen definieren
x = df_paar_nacht_3['Saettigungsdefizitmittelwert']
x_mean = np.mean(x)
Sxx = np.sum((x - x_mean)**2)
n = len(x)

# Standardfehler berechnen
sigma_k2 = np.sqrt(sigma2 / Sxx)
sigma_r_zehr = np.sqrt(sigma2 * (1/n + x_mean**2 / Sxx))

# Werte fuer die Gerade berechnen
x = np.linspace(df_paar_nacht_3['Saettigungsdefizitmittelwert'].min(),df_paar_nacht_3['Saettigungsdefizitmittelwert'].max(),100)
y = k2 * x + r_zehr


## Unsicherheitsbereich einfuegen
# Abweichungen und Standardabweichung
abweichung = df_paar_nacht_3['r_tot']-(k2*df_paar_nacht_3['Saettigungsdefizitmittelwert']+r_zehr)
sigma = np.std(abweichung)

# Unsicherheitsbereich (nur Parameter)
n = len(df_paar_nacht_3)
x_mean = np.mean(df_paar_nacht_3['Saettigungsdefizitmittelwert'])
standardfehler_regression = sigma*np.sqrt(1/n+(x-x_mean)**2/np.sum((df_paar_nacht_3['Saettigungsdefizitmittelwert']-x_mean)**2))
ci_upper = y + 1.96 * standardfehler_regression
ci_lower = y - 1.96 * standardfehler_regression

# Unsicherheitsbereich (Parameter + Messfehler)
y_upper = y + sigma
y_lower = y - sigma

# Plot mit linearer Regression erstellen
plt.figure(figsize=(9,6))
plt.plot(df_paar_nacht_3['Saettigungsdefizitmittelwert'],df_paar_nacht_3['r_tot'],'.', markersize=3)
plt.plot(x,y,label=f'Regression: y = {k2:.2e}x + {r_zehr:.2e}',color='purple')
plt.tick_params(axis='both',labelsize=13) 

plt.fill_between(x,y_lower,y_upper,color='lightblue',alpha=0.4,label='Parameter- und Messfehlerunsicherheit')
plt.fill_between(x,ci_lower,ci_upper,color='darkblue',alpha=0.3,label='Parameterunsicherheit')

plt.xlabel(r'$c_\mathrm{sat} - c ~ [\mathrm{mg ~ L^{-1}}]$',fontsize=14)
plt.ylabel(r'$r_{\mathrm{tot}}$ $[\mathrm{mg ~ L^{-1} ~ s^{-1}}]$',fontsize=14)
plt.legend(fontsize=13) 
plt.grid(True)
plt.xlim(3.033,3.187)
plt.ylim(-0.000315,-0.000245)
plt.show()

# Werte fuer k2 und r_zehr ausgeben lassen
print("\nAbschnitt M3-M4")
print("\nParameter aus Nachtdaten:")
print(f"k2 = {k2:.3e} ± {sigma_k2:.3e}")
print(f"r_zehr = {r_zehr:.3e} ± {sigma_r_zehr:.3e}")

#%%
# Messabschnitt M3-M4 - Tag

# Neue Spalte in Dataframe einfuegen, um rauszufiltern, ob der Zeitpunkt am Tag ist
df_paar_3['ist_Tag'] = False  

# Schleife, um dies bei jedem einzelnen Tag zu ueberpruefen
for tag in df_paar_3['Zeit_df3'].dt.normalize().unique():
    s = sun(tuebingen.observer,date=tag.date(),tzinfo=tuebingen.timezone)
    sunrise = s['sunrise']
    sunset = s['sunset']
    
    # Daten direkt vor Sonnenaufgang nicht miteinbeziehen
    sunrise_adj = sunrise - timedelta(hours=5)
    
    # Alle Zeitpunkte markieren, die innerhalb von Sonnenaufgang/-untergang liegen
    mask = (df_paar_3['Zeit_df3'].dt.date == tag.date()) & ((df_paar_3['Zeit_df3'] >= sunrise_adj) & (df_paar_3['Zeit_df3'] <= sunset))
    df_paar_3.loc[mask,'ist_Tag'] = True

# Neuen Dataframe nur mit den Tagesdaten erstellen
df_paar_tag_3 = df_paar_3[df_paar_3['ist_Tag']].copy()

# Spalte wieder loeschen
df_paar_tag_3.drop(columns='ist_Tag', inplace=True)

# Mittelwert der Zeit
df_paar_tag_3['Zeit_mittel'] = df_paar_tag_3[['Zeit_df3','Zeit_df4']].mean(axis=1)

# Daten vor und nach der Tracernacht loeschen
start = pd.Timestamp("2025-08-06 09:00:00",tz="Europe/Berlin")
end = pd.Timestamp("2025-08-09 06:00:00",tz="Europe/Berlin")
df_paar_tag_3 = df_paar_tag_3[(df_paar_tag_3['Zeit_mittel'] < start) | (df_paar_tag_3['Zeit_mittel'] > end)]

start = pd.Timestamp("2025-08-11 22:00:00",tz="Europe/Berlin")
end = pd.Timestamp("2025-08-15 12:00:00",tz="Europe/Berlin")
df_paar_tag_3 = df_paar_tag_3[(df_paar_tag_3['Zeit_mittel'] < start) | (df_paar_tag_3['Zeit_mittel'] > end)]

# Naechstgelegene Zeit von df_s zu df_paar_tag finden und hinzufuegen
strahlungs_idx = df_s.index.get_indexer(df_paar_tag_3['Zeit_mittel'],method='nearest')
df_paar_tag_3['Strahlung'] = df_s.iloc[strahlungs_idx]['m4'].values

# r_tot berechnen
df_paar_tag_3['r_tot'] = -(((df_paar_tag_3['Saettigungsdefizit_df4']-df_paar_tag_3['Saettigungsdefizit_df3'])/fliesszeit_3)-((df_paar_tag_3['Saettigungskonz_df4 [mg/L]']-df_paar_tag_3['Saettigungskonz_df3 [mg/L]'])/fliesszeit_3))

# Mittelwert fuer das Saettigungsdefizit aus beiden Dataframes berechnen 
df_paar_tag_3['Saettigungsdefizitmittelwert'] = (df_paar_tag_3['Saettigungsdefizit_df3']+df_paar_tag_3['Saettigungsdefizit_df4'])/2

# r_photo berechnen
df_paar_tag_3['r_photo'] = df_paar_tag_3['r_tot']-r_zehr-k2*df_paar_tag_3['Saettigungsdefizitmittelwert']


## Lineare Regression
# Lineare Regression durch den Ursprung
k_photo = np.sum(df_paar_tag_3['Strahlung']*df_paar_tag_3['r_photo'])/np.sum(df_paar_tag_3['Strahlung']**2)

# Residuen berechnen
residuals = df_paar_tag_3['r_photo'] - k_photo*df_paar_tag_3['Strahlung']
sigma2 = np.sum(residuals**2) / (len(df_paar_tag_3) - 1)

# Standardfehler berechnen
sigma_k_photo = np.sqrt(sigma2 / np.sum(df_paar_tag_3['Strahlung']**2))

# Werte fuer die Gerade berechnen
x_tag = np.linspace(df_paar_tag_3['Strahlung'].min(),df_paar_tag_3['Strahlung'].max(),100)
y_tag = k_photo * x_tag


## Regression mit Michaelis-Menten

# Anfangsschaetzungen fuer r_photo_max und R_0.5 (aus ODE Hausaufgabe)
schaetzung = [10**(-3),100]

# Fit durchfuehren
params, covparams = curve_fit(michaelis_menten,df_paar_tag_3['Strahlung'],df_paar_tag_3['r_photo'],p0=schaetzung)
r_photo_max, R_halb = params

y_mm = michaelis_menten(df_paar_tag_3['Strahlung'],r_photo_max,R_halb)


## Unsicherheitsbereiche einfuegen
# Abweichungen und Standardabweichung fuer lineare Regression
abweichung_tag = df_paar_tag_3['r_photo']-(k_photo*df_paar_tag_3['Strahlung'])
sigma_tag = np.std(abweichung_tag)

abweichung_tag_mm = df_paar_tag['r_photo'] - y_mm
sigma_tag_mm = np.sqrt(np.sum(abweichung_tag**2)/(len(y_mm)-2))

y_mm = michaelis_menten(x_tag,r_photo_max,R_halb)

# Unsicherheitsbereich (nur Parameter) fuer lineare Regression
n_tag = len(df_paar_tag_3)
x_mean_tag = np.mean(df_paar_tag_3['Strahlung'])
standardfehler_regression_tag = sigma_tag*np.sqrt(1/n_tag+(x_tag-x_mean_tag)**2/np.sum((df_paar_tag_3['Strahlung']-x_mean_tag)**2))
ci_tag_upper = y_tag + 1.96 * standardfehler_regression_tag
ci_tag_lower = y_tag - 1.96 * standardfehler_regression_tag

# Unsicherheitsbereich (Parameter + Messfehler)
y_tag_upper = y_tag + sigma_tag
y_tag_lower = y_tag - sigma_tag

# Standardabweichungen der Parameter aus Kovarianzmatrix
perr = np.sqrt(np.diag(covparams))  

mm_std = mm_error_propagation(x_tag,r_photo_max,R_halb,covparams)
ci_upper_mm = y_mm + 1.96 * mm_std
ci_lower_mm = y_mm - 1.96 * mm_std

# Gesamtunsicherheitsbereich (Parameter + Messfehler)
y_upper_mm = y_mm + 1.96*np.sqrt(sigma_tag_mm**2 + mm_std**2)
y_lower_mm = y_mm - 1.96*np.sqrt(sigma_tag_mm**2 + mm_std**2)

# Tagesdaten mit Unsicherheitsbereichen plotten
plt.figure(figsize=(10,7))
plt.plot(df_paar_tag_3['Strahlung'],df_paar_tag_3['r_photo'],'.',markersize=3)
plt.tick_params(axis='both', labelsize=15) 

# Lineare Regression
plt.plot(x_tag,y_tag,'r-',label=f'Lineare Regression: y = {k_photo:.2e}x')
plt.fill_between(x_tag,y_tag_lower,y_tag_upper,color='pink',alpha=0.4,label='\nLineare Regression: Parameter- \nund Messfehlerunsicherheit')
plt.fill_between(x_tag,ci_tag_lower,ci_tag_upper,color='red',alpha=0.5,label='\nLineare Regression: \nParameterunsicherheit')

# Michaelis-Menten
plt.plot(x_tag,y_mm,'g-',label='\nMichaelis-Menten Kinetik\n')
plt.fill_between(x_tag,y_lower_mm,y_upper_mm,color='lightgreen',alpha=0.25,label='\nMichaelis Menten: Parameter- \nund Messfehlerunsicherheit')
plt.fill_between(x_tag,ci_lower_mm,ci_upper_mm,color='green',alpha=0.35,label='\nMichaelis Menten: \nParameterunsicherheit')

plt.xlabel(r'$R$ $[\mathrm{W ~ m^{-2}}]$',fontsize=18)
plt.ylabel(r'$r_{\mathrm{photo}}$ $[\mathrm{mg ~ L^{-1} ~ s^{-1}}]$',fontsize=18)
plt.legend(loc='center left',bbox_to_anchor=(1, 0.5),ncol=1,fontsize=16)
plt.grid(True)
plt.xlim(0,460)
plt.ylim(-0.0002,0.00113)
plt.show()

# Parameter ausgeben lassen
print("\nParameter aus Tagdaten:")

print("Lineare Regression:")
print(f"k_photo = {k_photo:.3e} ± {sigma_k_photo:.3e}")

print("\nMichaelis-Menten Parameter:")
print(f"r_photo_max = {r_photo_max:.3e} ± {perr[0]:.3e}")
print(f"R_0.5 = {R_halb:.3f} ± {perr[1]:.3f}\n")

# Werte als Spalte einfuegen
df_param["M3-M4"] = [k2, r_zehr, k_photo, r_photo_max, R_halb]

print(df_param)


