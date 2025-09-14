############################################################
# Allgemeines zu Dateien und Strings
############################################################
# Beispiel anhand der Datei "rot13.txt"
filename = "rot13.txt"

print("Datei Zeilenweise mit for-Schleife lesen")
# die Datei "tt_rot13.txt" (ist in Variable filename hinterlegt) im Lesemodus ("r" = read) oeffnen
f = open(filename, "r")
# f referenziert nun ein Dateiobjekt zu tt_rot13.txt
for line in f:
    print(line)
# das Dateiobjekt schließen!
f.close()
print()

print("Datei Zeilenweise mit for-Schleife lesen (mit with)")
# Analog zur obigen Vorgehensweise kann auch das 'with'-statement verwendet werden.
# Dies ist die bevorzugte Variante.
# Beim Verlassen des Blocks wird hier automatisch 'close()' auf dem file-Objekt aufgerufen.
with open(filename, "r") as f:
    # f referenziert nun ein Dateiobjekt zu tt_rot13.txt
    for line in f:
        print(line)
print()

#-----------------------------------------------------------

print("Gesamten Dateiinhalt in einen String lesen")
# die Datei "tt_rot13.txt" (ist in Variable filename hinterlegt) im Lesemodus ("r" = read) oeffnen,
with open(filename, "r") as f:
    # f referenziert nun ein Dateiobjekt zu tt_rot13.txt
    # Inhalt der ganzen Datei als String auslesen
    inhalt = f.read()
print(inhalt)
print()

print("String nach Trennzeichen teilen")
# zunaechst fuehrende und anhaengende 'whitespaces' entfernen
inhalt = inhalt.strip()
# beim Zeilenvorschub trennen
geteilt = inhalt.split("\n")
print(geteilt)

#-----------------------------------------------------------

# Text in eine Datei schreiben

# Die Datei "schreiben.txt" im Schreibmodus ("w" = write) oeffnen.
# Sie wird hierbei erstellt oder, falls bereits vorhanden, überschrieben.
with open("schreiben.txt", "w") as f:   
    # Der string wird ohne Zeilenumbruch in die Datei geschrieben, 
    # deshalb ist es notwendig, diesen manuell einzufuegen.
    f.write("Dieser string wird in die Datei geschrieben. ")
    f.write("Auch Sonderzeichen wie ein \nZeilenumbruch funktionieren.")
    
    print("Alternativ kann man auch die print-Funktion benutzen,", file=f)
    print("indem man dem Parameter 'file' das Dateiobjekt übergibt.", file=f)
    
    

