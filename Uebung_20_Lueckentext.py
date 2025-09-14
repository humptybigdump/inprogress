"""
Uebung 2.0

Autor: Mark-Patrick Mühlhausen

Datum: 2025-08-04
"""

"""
Was ist Numpy?

Sammlung von Werkzeugen zur professionellen Erzeugung, Veränderung und Verarbeitung
von multidimensionalen Arrays. Die Stärke liegt neben der Vielseitigkeit in der
Performance (manchmal schneller als Matlab)

Wichtige Links:

http://docs.scipy.org/doc/numpy-1.10.1/index.html
"""

# Zunaechst muss NumPy importiert werden
import numpy as np

# Ausgangsbasis ist ein Numpy-Array beliebiger Form

m1 = np.array([1,2,3])
m2 = np.array([[1,4],[7,3]])
m3 = np.array([[11,12,13],[21,22,23],[31,32,33]])

# Es ist natürlich auch möglich spezielle Arrays zu definieren

m4 = np.zeros([5,5])
m5 = np.zeros([5])
m6 = np.ones([5,5])
m7 = np.identity(6)
m8 = np.random.rand(3,2)

# Um ein NumPy Array mit einer Sequenz an Zahlen zu erhalten exisitiert analog
# arange oder linspace

seq1   = np.arange(3)
seq2   = np.arange(3,8)
seq3   = np.arange(3.0)
seq4   = np.arange(3,11,2)
seq5   = np.arange(11,3,-2)

lsp1 = np.linspace(2.0, 3.0, num=10)

# Der Zugriff auf die Elemente des Arrays kann so erfolgen
'''
??    # Zeile 1, erste Spalte
??    # Alles, davon Zeile 1
??     # Alle Zeilen Spalte 1
??    # 0. Zeile, letztes Element
??   # 0. Zeile, letzte beiden Elemente
??   # Jede zweite Spalte
'''
# Rechnen

e1 = 5 * m1
e2 = m2 * 5
e3 = m1 / 3.0

e4 = np.dot(m1,m1)
e5 = np.cross([1,0,0],[0,1,0])

e6 = np.linalg.norm(m1,ord=2)

e7 = m3 * m1

e8 = np.sqrt(m1)
e9 = m1**2

