#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""UTILISATION DE LA CLASSE OSCILLOGRAPHE"""
"EXERCICE 13.8"

###########################################
#### Importation fonction et modules : ####
###########################################


from oscillo import *


###############################################################################
#### Gestion d'évènements : définition de différentes Fonctions/Classes : #####
###############################################################################


############# Création des Classes #############


############# Création des Fonctions #############


###############################
#### Programme principal : ####
###############################

root = Tk()
g1 = OscilloGraphe()
g1.pack()

g2 = OscilloGraphe(haut=200, larg=250)
g2.pack()
g2.traceCourbe()

g3 = OscilloGraphe(larg=220)
g3.configure(bg='white', bd=3, relief=SUNKEN)
g3.pack(padx=5, pady=5)
g3.traceCourbe(phase=1.57, coul='purple')
g3.traceCourbe(phase=3.14, coul='dark green')


# Exercice 13.8 : Trace des courbes mon ami, trace !!
g4 = OscilloGraphe(larg=400, haut=300)
g4.pack()
g4.configure(bg='yellow')
g4.traceCourbe(ampl=12, freq=2, coul='dark green')
g4.traceCourbe(ampl=15, freq=1, coul='blue')
g4.traceCourbe(ampl=10, freq=1.5, coul='purple')
g4.traceCourbe(ampl=7, freq=2, coul='black')
root.mainloop()
