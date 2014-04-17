#! /usr/bin/env python
# -*- coding:Utf8 -*-

" PROGRAMME D'ANIMATION PAR BUTTONS"

############# Importation fonction et modules : ################


from tkinter import *


############# Gestion d'évènements : définition de différentes fonctions utiliées  : ##############

def avance(xcoord, ycoord):
	"Procédure générale"
	global x1, y1
	x1, y1 = x1 + xcoord, y1 + ycoord
	can1.coords(pointeur, x1, y1, x1+30, y1+30)

def deplacement_gauche():
	avance(-10, 0)

def deplacement_droite():
	avance(10, 0)

def deplacement_bas():
	avance(0, 10)

def deplacement_haut():
	avance(0, -10)


############## Programme principal : #################

"coordonnées de base"
x1, y1 = 50, 50 # variable utilisées de façon globales

"Taille pointeur"
xx, yy = 30, 30


"widgets"
fen1 = Tk()
fen1.title("Animation par boutton")
can1 = Canvas(fen1, width = 200, height = 200, bg = 'dark grey')
pointeur = can1.create_oval(x1, y1, x1+xx, y1+yy, width = 2, fill = 'blue')
can1.pack(side = LEFT)
Button(fen1, command = deplacement_bas, text = 'Bas').pack()
Button(fen1, command = deplacement_haut, text = 'Haut').pack()
Button(fen1, command = deplacement_droite, text = 'Droite').pack()
Button(fen1, command = deplacement_gauche, text = 'Gauche').pack()
Button(fen1, command = fen1.quit, text = 'Quitter').pack(side = BOTTOM)

fen1.mainloop()

