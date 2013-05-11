#! /usr/bin/env python
# -*- coding:Utf8 -*-

" DETECTION DU CLIC ET ALERTE SUR SA POSITION "

############# Importation fonction et modules : ################

from tkinter import *


############# Gestion d'évènements : définition de différentes fonctions utiliées  : ##############

def pointeur(event):
	"relève les coordonnées du clic souris"
	chaine.configure(text = "Clic détecté en X = " + str(event.x) +\
                                ", Y = " + str(event.y))

def alerte(event):
	"Ajoute un cercle sur la position du curseur"
	zone.delete(ALL)
	zone.create_oval(float(event.x - taille), float(event.y - taille), float(event.x) \
		+ taille, float(event.y) + taille, fill = "red")

############## Programme principal : #################

taille = 5

fen = Tk()
cadre = Frame(fen, width = 200, height = 150, bg = "light yellow")
cadre.bind("<Button-1>", pointeur)
cadre.pack()
chaine = Label(fen)
chaine.pack()
fen.mainloop()


fen2 = Tk()
zone = Canvas(fen2, width = 200, height = 150, bg = "white")
zone.bind("<Button-1>", pointeur)
zone.bind("<Button-2>", alerte)
zone.pack()
chaine = Label(fen2)
chaine.pack()
fen2.mainloop()













