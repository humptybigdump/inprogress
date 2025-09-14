"""
Uebung 1.0

Einführung in Python 

Autor: Mark-Patrick Mühlhausen

Datum: 2025-08-04
"""

# Einleitung

"""
Was ist Python?

- Skriptsprache, ähnlich Matlab
- Objektorientiert und funktional
- Entwickelt von Guido van Rossum (1989)

Wo liegen die Stärken von Python?

- Python ist gratis
- Python ist leicht erlernbar
- Gute Lesbarkeit (Keine Block-Klammmern bei Kontrollstrukturen, Keine Semikolons zum Befehlsabschluss)
- Gute Strukturierung (Einrückungen) und daher auch einfache rzu dokumentieren
- Quellcode ist im allgemeinen kürzer als bei vergleichbaren Sprachen
- Python besitzt keine Typeninitialisierung von Variablen
- Große (sehr aktive) Community
- Leistungsfähigkeit, da einige Module spezialisierten und kompilierten C-Code enthalten (Matrixoperationen)
- Kontinuierliche Weiterentwicklung (aktuelle Versionen 3.8 - 3.11)
- Sehr viele Module für alle möglichen Einsatzszeanrien (z.B. SciPy, NumPy, Django, PyQt, Cython)
- Python ist plattformunabhängig und auf Linux bereits vorinstalliert

Wichtige Links

www.python.org
https://pypi.python.org/pypi
https://www.continuum.io/
"""
# Zunächst werdne verschiedene Variablen definiert. Der Typ der Variable
# wird automatisch gewählt.

a          = 1
b          = 2
c          = 3.0
text       = "Hier steht ein Text"

# Zunaechst erstmal schauen, welche Typen ausgewählt wurden.

type(a)
type(c)
type(text)

# Ist der Datentyp nicht richtg gewählt worden kann man diesen nachträglich
# ändern. Wichtig ist, dass es sich hierbei um "InPlace" Ändeurngen handelt. 
# Die eigentlich Variable wird dabei nicht verändert.

float(a)
str(a)

# Mit den verschiedenen Variablen kann man nun Rechnen.

e1 = a + b
e3 = a/c       

# Möchte man mehrere Elemente zusammenfügen gibt es in Python grundsätzlich drei
# Möglichkeiten: Listen, Sets und Dictionaries, die jeweils unterschiedliche
# Eigenschaften besitzen
# Listen : Elemente haben eine Reihenfolge, jedes Element kann beliebig oft vorkommen
# Sets   : (Mengen) Elemente haben keine Reihenfolge, Jedes Element kann nur einmal vorkommen
# Dictionaries : Elemente haben eine Reihenfolge, Bestehend aus Key:Value-Paaren

Liste1     = list([1,2,3])
Set1       = set([3,2,1])
Dict1      = {99:'Montag', 100:'Dienstag'}

# Jeder dieser Datentypen verfügt über besondere Methoden für Verarbeitung und
# Zugriff. Da Sets keine Reihenfolge haben, ist ein Index-Zugriff nicht möglich.
# Bei allen "Mengen"-Datentypen fängt der Index immer mit 0 an!

Liste1[0]
Dict1[99]

# Die Veränderung der Variablen funktioniert über das Anwenden einer Methode auf
# die jeweilige Variable

Liste1.append(99)
Dict1[3] = 'Mittwoch'

# Im Folgenden soll es aber nur noch Listen gehen. Um herauszufinden, welche
# Methoden ein Datentyp mitbringt soll im Folgenden eine Liste angelegt werden

Liste2 = list([1,3,6,9,8,2,5,7,8,9,3,5,6,4,8,7,9,6,2,1,5,4,8,7,6,3,5,0])

# Die verfügbaren Methoden finden Sie, wenn wenn Sie Liste2. eingeben und dann
# die Tab-Taste drücken. Für die Folgenden Fragen suchen Sie 

'''
?? # Wie oft kommt die 1 in der Liste vor?
?? # An welcher Stelle taucht die 7 das erste mal auf
?? # Wie lang ist die Liste2? (Hinweis len())
?? # Entfernen Sie die 0 aus der Liste
?? # Entfernen sie das erste Element aus der Liste Hinweis del()
?? # Greifen Sie auf die ersten 5 Elemente zu
?? # Greifen Sie auf die letzten 5 Elemente zu
?? # Wählen Sie ausgehend vom 1. Element jedes zweite bis zum 6.
'''

# Arbeiten mit Funktionen: Wir im Funktionsaufruf ein Wert hinterlegt, wird dieser
# verwendet, sofern kein Wert übergeben wird. Es ist auch möglich zwei Werte
# zurückzugeben. Man beachte die Einrückung, die unbedingt notwendig ist!

def addieren(x,y=12):
    ''' Addiere zwei Werte '''
    return x + y
    
def subtrahieren(x,y):
    return x - y
    
# Der Aufruf einer Funktion erfolgt     
e4 = addieren(5)
e5 = addieren(5,1)

# Arbeiten mit Schleifen: Bei einer for-Schleife kann man den Werte-Bereich mit
# dem Range-Operator festlegen

range(50)
range(40,50)
range(5,50,5)

for i in list(range(50)):
    print(i)
    
x = 10
while x > 1:
    print(x)
    x -= 1
    
x= 10
while x > 5:
    print(x)
    x -= 1
else:
    print("Das ist der Else-Block " + str(x))
    x -= 1
    
# Arbeiten mit Kontrollstrukturen

x = 4
if x > 5:
    print("Wert ist 5")
elif x < 0:
    print("Wert ist < 0")
else:
    print("Wert ist anders")
    
d = 7
((d < 10) & (d > 0)) & False
(d < 10) | (d > 0)
    
# Arbeiten mit Diagrammen
    
import matplotlib.pyplot as plt
import math

x = list(range(500))
y = [math.sin(0.01*i) for i in x]
    
plt.figure()    
plt.plot(x,y,linewidth=4)
plt.title('Titel',fontsize=25)
plt.xlabel('x [s]',fontsize=22)
plt.ylabel('y [m]',fontsize=22)
plt.tick_params(axis='both', which='major', labelsize=15)
plt.xlim([0,500])
plt.ylim([-1,1])
plt.grid(True)
plt.show()
plt.savefig('beispiel.png',dpi=300)
    
# Aufgabe: Schreiben Sie eine Funktion, der ein Integer übergeben wird und die
# die Fakultät berechnet.