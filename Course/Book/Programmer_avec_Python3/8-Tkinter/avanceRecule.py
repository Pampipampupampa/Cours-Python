#! /usr/bin/env python
# -*- coding:Utf8 -*-*




" PETIT PROGRAMME FAISANT FAIRE DES ALLER RETOUR A UNE BALLE "




################################################################
############# Importation fonction et modules : ################
################################################################



from tkinter import *
from math import sin, cos




###################################################################################################
############# Gestion d'évènements : définition de différentes fonctions utiliées  : ##############
###################################################################################################



def avance(pas = 20):
	global x1, y1, i # nécessaire afin de pas avoir ces variables de réinitialiées à chaque appels de la fonction
	if i == 1:
		if x1+rayon*2 >= longueur: # si la balle sort du canevas alors on inverse le sens de déplacement
			i = 0
		else: # tant que la balle n'est pas hors du canevas (vers la droite)
			x1 = x1+pas
			can1.coords(balle, x1-rayon, y1-rayon, x1+rayon, y1+rayon)
			can1.create_line(x1-pas, y1, x1, y1, fill = 'dark blue') # trace la trajectoire de la balle
	if i == 0:
		if x1-rayon*2 <= 0: # si la balle sort du canevas alors on inverse le sens de déplacement
			i = 1
		else: # tant que la balle est pas hors du canevas (vers la gauche)
			x1 = x1-pas
			can1.coords(balle, x1-rayon, y1-rayon, x1+rayon, y1+rayon)
			can1.create_line(x1, y1, x1+pas, y1, fill = 'dark blue')



def cercle():
	global x1, y1, ang
	" Extrémité du cercle afin qu'il ne dépase pas (marche sous cette forme car la fonction sin ou cos ne donne jamais une valeur supérieur à 1) "
	rayoncercle, centre = hauteur/2, hauteur/2 # l'appel de la variable hauteur permet d'automatiquement adapter la figure au canevas
	xvar, yvar = x1, y1 # mémorise les anciennes coordonnées
	ang = ang + 0.1 # décalage de 0.1 radian
	x1, y1 = sin(ang), cos(ang)
	x1, y1 = x1*rayoncercle + centre, y1*rayoncercle + centre
	can1.coords(balle, x1-rayon, y1-rayon, x1+rayon, y1+rayon)
	can1.create_line(xvar, yvar, x1, y1, fill = 'blue') # trace la trajectoire de la balle



def lissajous():
	global x1, y1, ang
	" Extrémité du cercle afin qu'il ne dépase pas (marche sous cette forme car la fonction sin ou cos ne donne jamais une valeur supérieur à 1) "
	rayoncercle, centre = hauteur/2, hauteur/2
	xvar, yvar = x1, y1 # mémorise les anciennes coordonnées
	ang = ang + 0.1 # décalage de 0.1 radian
	x1, y1 = sin(2*ang), cos(3*ang) # avec f1/f2 = 2/3 : fonction de lissajous
	x1, y1 = x1*rayoncercle + centre, y1*rayoncercle + centre
	can1.coords(balle, x1-rayon, y1-rayon, x1+rayon, y1+rayon)
	can1.create_line(xvar, yvar, x1, y1, fill = 'yellow') # trace la trajectoire de la balle



def effacer(): # efface et restaure les éléments et paramètres par défaut
	global balle, x1, y1, i, ang
	can1.delete(ALL)
	x1, y1, i, ang = x0, y0, 1, 0
	balle = can1.create_oval(x1-rayon, y1-rayon, x1+rayon, y1+rayon, width = 2, fill = 'red')



######################################################
############## Programme principal : #################
######################################################



" VARIABLE BASES "
x0, y0 = 200, 200 # permet de remettre le dessin à l'état initial
i = 1 # initialise le déplacement de la balle
x1, y1 = 200, 200
rayon = 10
ang = 0
hauteur = 400
longueur = 400



" PRINCIPAUX ELEMENTS "
fen1 = Tk()
fen1.title("Aller et retour")
can1 = Canvas(fen1, width = longueur, height = hauteur, bg = 'grey') # Ne pas directement affecter ".grid" à "can1"
can1.grid(row = 1, column = 1, columnspan = 4, padx = 20, pady = 20)
balle = can1.create_oval(x1-rayon, y1-rayon, x1+rayon, y1+rayon, width = 2, fill = 'red')



" ACTIONS POSSIBLES "
Button(fen1, text = 'Décalage', bg = 'dark orange', command = avance).grid(row = 2, column = 1)
Button(fen1, text = 'Effacer', bg = 'dark orange', command = effacer).grid(row = 2, column = 4)
Button(fen1, text = 'Cercle', bg = 'dark orange', command = cercle).grid(row = 2, column = 2)
Button(fen1, text = 'Lissajous', bg = 'dark orange', command = lissajous).grid(row = 2, column = 3)

Button(fen1, text = 'Quitter', bg = 'dark green', command = fen1.quit).grid(row = 3, column = 2, columnspan = 2)



" RECEPTIONNEUR D'EVENEMENTS "
fen1.mainloop()
