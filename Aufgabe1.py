#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  2 15:46:57 2022

@author: Alexander Stroh
"""

###############################################################################
### Imports
###############################################################################
import matplotlib.pyplot as mpl
###############################################################################
###############################################################################
### Definitionen der Klassen und Funktionen
###############################################################################

# Leere Klasse für Datenobjekt
class simData(object):
    pass

def readRANSresults(foldername):
    """
    This function reads the output file of a simulation
    """
    # Datenobjekt definieren
    rans_data = simData()
    rans_data.y_plus = []
    rans_data.U = []
    rans_data.k = []
    rans_data.uv = []
    
    # Postprocessing Datei einlesen
    with open(foldername+'/wallNormal.xy') as fin:
        # Zeilen einlesen
        data_lines = fin.readlines()
        
        # Zeile für Zeile verarbeiten
        for line in data_lines:              
            if line.startswith('#'):
                pass
            else:
                #Splitten, wenn kein Delimiter spezifiziert werden Leerzeichen verwendet:
                split_line = line.split()                
                # die benötigten Daten in die Variablen abspeichern (1. und 2. Spalte)
                rans_data.y_plus.append(float(split_line[0]))
                rans_data.U.append(float(split_line[1]))
                # TKE einlesen           
                # die benötigten Daten in die Variable abspeichern (5. Spalte)
                rans_data.k.append(float(split_line[4]))
                # Reynolds-Spannungen einlesen             
                # die benötigten Daten in die Variable abspeichern (7. Spalte)
                rans_data.uv.append(float(split_line[6]))
        
            
    # Datenobjekt zurückgeben
    return rans_data

def plotData(rans_data,foldertosave):
    """
    This function plots the data given data object
    """
    # Geschwindigkeit plotten
    mpl.figure(1)
    mpl.plot(rans_data.y_plus, rans_data.U)
    # Achsenbeschriftung
    mpl.xlabel('$y^+$')
    mpl.ylabel(r'$\bar{U}^+$') # 'r' vor dem Text inkludiert backslash, sonst wird die Zeile falsch interpretiert, siehe https://docs.python.org/2/reference/lexical_analysis.html#string-literals
    # Abspeichern als PNG
    mpl.savefig(foldertosave+'/U.png',format="png")
    
    # TKE und uv
    mpl.figure(2)
    mpl.plot(rans_data.y_plus, rans_data.k, label='RANS $k^+$')
    mpl.plot(rans_data.y_plus, rans_data.uv, label=r'RANS $\overline{u^\prime v^\prime}^+$')
    # Achsenbeschriftung
    mpl.xlabel('$y^+$')
    mpl.ylabel('$k^+$, $\overline{u^\prime v^\prime}^+$')
    # Legende aktivieren
    mpl.legend()
    # Abspeichern als PNG
    mpl.savefig(foldertosave+'/k_uv.png',format="png")

def main():
    """
    this is the function used to call all functions necessary for the task
    """
    
    # Ordner mit den Datensätzen
    data_path = './postProcessing/sample/509/'
    
    # Datensatz einlesen
    rans = readRANSresults(data_path)
    
    # Datensatz plotten und abspeichern
    plotData(rans,'./')

###############################################################################
### Führt die main-Funktion aus nachdem Einlesen aller Funktionen und Definitionen 
###############################################################################    
if __name__ == "__main__":
    main()        
