#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  3 11:20:51 2022

@author: Alexander Stroh
"""
# Module importieren
import numpy
from math import pi
import matplotlib.pyplot as plt
import rosenhead

# Hauptefinitionen
U=1;
nvort = 12
lambd = 2 * pi
ampl = 0.1 * lambd
dt=0.05*lambd/U
nt=8

# Initialisierung der Koordinaten für Wirbelzentren

vortpos_x = numpy.linspace(lambd/nvort,lambd,nvort)
vortpos_y = ampl * numpy.sin(vortpos_x)

# Initialisierung der induzierten Geschwindigkeiten

u=numpy.zeros(numpy.size(vortpos_x))
v=numpy.zeros(numpy.size(vortpos_x))

# Erstellung der Achsenumgeung mit subplots
fig, axs = plt.subplots(nt,sharex=True,figsize=(5, 10))
fig.tight_layout(pad=3.0)

# Hilfe zur Funktionbenutzung (Beispiel)
help(rosenhead.compVelocity)

# Iterieren in der Zeit - ab hier ergänzen
