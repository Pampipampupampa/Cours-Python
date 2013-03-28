#! /usr/bin/env python
# -*- coding:Utf8 -*-

"DEUX DESSINS ALTERNES"


############# Importation fonction et modules : ################

from tkinter import *

############# Gestion d'évènements : définition de différentes fonctions utiliées  : ##############

def cercle_concentrique(x, y, r, coul = "black"):
	"trace un ensemble de cercle concentriques"
	can.create_oval(x - r, y - r, x + r, y + r, outline = coul)

def figure_1():
	"efface dessin précédent afin d'avoir un espace propre"
	can.delete(ALL)

	"trace une cible au centre du canevas"
	can.create_line(100, 0, 100, 200, fill = "blue")
	can.create_line(0, 100, 200, 100, fill = "blue")

	"trace un ensemble de cercle concentrique"
	rayon = 15
	while rayon < 100:
		cercle_concentrique(100, 100, rayon)
		rayon += 15
		pass

def figure_2():
	"efface dessin précédent afin d'avoir un espace propre"
	can.delete(ALL)

	"liste des éléments du visage"
	visage = [[100, 95, 80, 'red'], # tête
	[100, 95, 15, 'red'], # nez
	[70, 70, 15, 'red'], # yeux
	[130, 70, 15, 'red'],
	[70, 70, 5, 'red'],
	[130, 70, 5, 'red'],
	[100, 145, 30, 'red'], # bouche
	[156, 115, 20, 'red'], # joue
	[44, 115, 20, 'red']]

	"trace le visage"
	i = 0
	while i < len(visage):
		el = visage[i]
		cercle_concentrique(el[0], el[1], el[2], el[3])
		i += 1
		pass

############## Programme principal : #################

fen = Tk()
can = Canvas (fen, width = 200, height = 200, bg = "dark grey")
can.pack(side = TOP, padx = 5, pady = 5)
b1 = Button(fen, text = "dessin 1", command = figure_1)
b1.pack(side = LEFT, padx = 3, pady = 3)
b2 = Button(fen, text = "dessin 2", command = figure_2)
b2.pack(side = RIGHT, padx = 3, pady = 3)
fen.mainloop()

	







