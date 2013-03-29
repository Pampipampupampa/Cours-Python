#! /usr/bin/env python
# -*- coding:Utf8 -*-

"CREATION D'UN DAMIER"


############# Importation fonction et modules : ################


from tkinter import *
from random import randrange


############# Gestion d'évènements : définition de différentes fonctions utiliées  : ##############


def damier():
	"Trace le damier"
	y = 0
	while y < 10:
		if y % 2 == 0: # Décale une fois sur deux 
			x = 0      # la position du premier carré noir
		else:
			x = 1
		carre_noir(x*taille_carre, y*taille_carre)
		y += 1



def carre_noir(x, y):
	"Trace les carrés noirs"
	i = 0
	while i < 5:
		can.create_rectangle(x, y, x+taille_carre, y+taille_carre, fill = "black")
		i += 1
		x += taille_carre * 2


def pion():
	"Dessine un pion au hazard sur le damier"
	x = taille_carre/2 + randrange(10) * taille_carre
	y = taille_carre/2 + randrange(10) * taille_carre
	creation_pion(x, y, taille_carre/3, "yellow")


def creation_pion(x, y, r, coul):
	"Trace un pion"
	can.create_oval(x-r, y-r, x+r, y+r, fill = coul)


############## Programme principal : #################


taille_carre = 60 # permet de définir une taille de damier modifiable
fen = Tk()
can = Canvas(fen, width = taille_carre * 10, height = taille_carre * 10, bg = "white")
can.pack(side = TOP, padx = 5, pady = 5)
b1 = Button(fen, text = "damier", command = damier)
b1.pack(side = LEFT, padx = 5, pady = 5) 
b2 = Button(fen, text = "Pion", command = pion)
b2.pack(side = RIGHT, padx = 5, pady = 5)
fen.mainloop()



