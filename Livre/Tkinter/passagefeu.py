#! /usr/bin/env python
# -*- coding:Utf8 -*-


"PROGRAMME PERMETTANT DE FAIRE ALTERNER 2 FEUX DE CIRCULATION"

################################################################
############# Importation fonction et modules : ################
################################################################



from tkinter import *



###################################################################################################
############# Gestion d'évènements : définition de différentes fonctions utiliées  : ##############
###################################################################################################

"Fonction permettant d'alterner la couleurs des 4 feux"

def changement():
	global i, v1, p1, v1, v2 # Si ces variables ne sont pas en global rien ne se passera
	compteur = 1 # Permet de ne pas avoir l'action qui tourne en boucle
	if i==0 and compteur==1:
		p1 = can0.create_oval(60, 335, 90, 365, fill = '#367E2C')
		v1 = can0.create_oval(60, 235, 90, 265, fill = '#DD1616')
		p2 = can3.create_oval(10, 235, 40, 265, fill = '#367E2C')
		v2 = can3.create_oval(10, 335, 40, 365, fill = '#DD1616')
		i = 1
		compteur = 0
	if i==1 and compteur==1:
		p1 = can0.create_oval(60, 335, 90, 365, fill = '#DD1616')
		v1 = can0.create_oval(60, 235, 90, 265, fill = '#367E2C')
		p2 = can3.create_oval(10, 235, 40, 265, fill = '#DD1616')
		v2 = can3.create_oval(10, 335, 40, 365, fill = '#367E2C')
		i = 0
		compteur = 0
	else:
		pass

######################################################
############## Programme principal : #################
######################################################

i = 0

"couleur des feux de base"
pieton = 'red'
voiture = 'green'



"WIDGET"

fen = Tk()
fen.title('Passage pour piétons')


"Passage piétons"
can1 = Canvas(fen, width = 190, height = 600, bg = '250, 250, 250')
can1.grid(row = 1, column = 2, padx = 0, pady = 0)

# Création du pssage pour piétons
can1.create_rectangle(10, 350, 30, 250, fill = '#B8B812')
can1.create_rectangle(40, 350, 60, 250, fill = '#B8B812')
can1.create_rectangle(70, 350, 90, 250, fill = '#B8B812')
can1.create_rectangle(100, 350, 120, 250, fill = '#B8B812')
can1.create_rectangle(130, 350, 150, 250, fill = '#B8B812')
can1.create_rectangle(160, 350, 180, 250, fill = '#B8B812')

"Feux de gauche"
can0 = Canvas(fen, width = 100, height = 600, bg = 'dark grey')
can0.grid(row = 1, column = 1, padx = 0, pady = 0)
p1 = can0.create_oval(60, 335, 90, 365, fill = '#DD1616')
v1 = can0.create_oval(60, 235, 90, 265, fill = '#367E2C')

"Feux de droite"
can3 = Canvas(fen, width = 100, height = 600, bg = 'dark grey')
can3.grid(row = 1, column = 3, padx = 0, pady = 0)
p2 = can3.create_oval(10, 235, 40, 265, fill = '#DD1616')
v2 = can3.create_oval(10, 335, 40, 365, fill = '#367E2C')

"Bouttons pour alterner les feux et pour quitter"
Button(fen, text = 'Changer', bg = '#CD8321', command = changement).grid(row = 2, column = 1)
Button(fen, text = 'Quitter', bg = '#CD8321', command = fen.quit).grid(row = 2, column = 3)

fen.mainloop()

















