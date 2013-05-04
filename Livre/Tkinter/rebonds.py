#! /usr/bin/env python
# -*- coding:Utf8 -*-

"PROGRAMME SIMULANT UNE BALLE REBONDISSANT À L'INFINI"

################################################################
############# Importation fonction et modules : ################
################################################################



from tkinter import *




###################################################################################################
############# Gestion d'évènements : définition de différentes fonctions utiliées  : ##############
###################################################################################################

def move():
	global x1, y1, v, dx, dv, flag
	"Permet d'éviter la sortie de la balle du canevas"
	if x1 > largeur-20 or x1 < 20:
		dx = -dx #Inversement du déplacement
	"Déplacement horizontal"
	x1 = x1 + dx
	"Modification de la vitesse"
	v = v + dv
	"Déplacement vertical"
	y1 = y1 + v
	"Permet d'éviter la sortie de la balle verticalement"
	if y1 > hauteur-20:
		y1 = hauteur-20
		v = -v #Inversement du déplacement
	"Modification de la position de la balle"
	can1.coords(oval1, x1-15, y1-15, x1+15, y1+15)
	"Permet de mettre en arrêt le déplacement de la balle"
	if flag > 0:
		fen1.after(50, move)



def stop_it():
	"arrêt de l'animation"
	global flag
	flag = 0




def start_it():
	"démarrage de l'animation"
	global flag
	if flag == 0: #Verification permettant de ne lancer qu'une seule boucle (si stop_it n'est pas utilisé avant cette fonction ne fait rien)
		flag = 1
		move()




######################################################
############## Programme principal : #################
######################################################

"Variable à utilisation globale"
x1, y1, dx, dv, flag, v = 20, 20, 5, 5, 0, 0 # Mettre moins de 20 enferme la balle dans une boucle sans fin dans son petit coin tout seul^^

"Dimensions du canevas"
hauteur = 400
largeur = 400

"Élements de l'interface"
fen1 = Tk()
fen1.title("Récursivité avec une balle")
can1 = Canvas(fen1, bg = 'dark grey', height = hauteur, width = largeur)
can1.grid(row = 1, column = 1, columnspan = 3, padx = 5, pady = 5)
oval1 = can1.create_oval(x1, y1, x1+30, y1+30, width = 2, fill = 'red')
bou2 = Button(fen1, text = 'Démarrer', width = 8, command = start_it).grid(row = 2, column = 1)
bou3 = Button(fen1, text = 'Arrêter', width = 8, command = stop_it).grid(row = 2, column = 2)
bou1 = Button(fen1, text = 'Quitter', width = 8, command = fen1.quit).grid(row = 2, column = 3)


fen1.mainloop()
