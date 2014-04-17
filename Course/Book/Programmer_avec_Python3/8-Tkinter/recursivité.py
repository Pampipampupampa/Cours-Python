#! /usr/bin/env python
# -*- coding:Utf8 -*-


"INITIATION À LA RECURSIVITÉ"


################################################################
############# Importation fonction et modules : ################
################################################################



from tkinter import *
from math import sin, cos




###################################################################################################
############# Gestion d'évènements : définition de différentes fonctions utiliées  : ##############
###################################################################################################

def move():
	"deplacement de la balle"
	global x1, y1, dy, dx, flag
	x1, y1 = x1 + dx, y1 + dy
	if x1>largeur-40:
		x1, dx, dy = largeur-40, 0, 15
		can1.itemconfig(oval1, fill ='blue') # méthode permettant de modifier une class ici sa couleur (méthode très utile !!!!!!!!!!!!)
	if y1>hauteur-40:
		can1.itemconfig(oval1, fill ='green') # méthode permettant de modifier une class ici sa couleur (méthode très utile !!!!!!!!!!!!)
		y1, dx, dy = hauteur-40, -15, 0
	if x1<10:
		can1.itemconfig(oval1, fill ='orange') # méthode permettant de modifier une class ici sa couleur (méthode très utile !!!!!!!!!!!!)
		x1, dx, dy = 10, 0, -15
	if y1<10:
		can1.itemconfig(oval1, fill ='red') # méthode permettant de modifier une class ici sa couleur (méthode très utile !!!!!!!!!!!!)
		y1, dx, dy = 10, 15, 0
	can1.coords(oval1, x1, y1, x1+30, y1+30)
	if flag > 0:
		fen1.after(50, move) #Déclenche l'appel à la fonction après un laps de temps défini (ici 50 millisecondes)




def move_zigzag():
	global x1, y1, dy, dx, flag
	x1, y1 = x1 + dx, y1 + dy
	if x1>largeur-40:
		x1, dx, dy = largeur-40, -10, 15
		can1.itemconfig(oval1, fill ='blue') # méthode permettant de modifier une class ici sa couleur (méthode très utile !!!!!!!!!!!!)
	if y1>hauteur-40:
		can1.itemconfig(oval1, fill ='green') # méthode permettant de modifier une class ici sa couleur (méthode très utile !!!!!!!!!!!!)
		y1, dx, dy = hauteur-40, -15, -3
	if x1<10:
		can1.itemconfig(oval1, fill ='orange') # méthode permettant de modifier une class ici sa couleur (méthode très utile !!!!!!!!!!!!)
		x1, dx, dy = 10, 10, -15
	if y1<10:
		can1.itemconfig(oval1, fill ='red') # méthode permettant de modifier une class ici sa couleur (méthode très utile !!!!!!!!!!!!)
		y1, dx, dy = 10, 15, 3
	can1.coords(oval1, x1, y1, x1+30, y1+30)
	if flag > 0:
		fen1.after(50, move_zigzag) #Déclenche l'appel à la fonction après un laps de temps défini (ici 50 millisecondes)




def move_cercle():
	global x1, y1, flag, ang
	passage = 1
	" Extrémité du cercle afin qu'il ne dépase pas (marche sous cette forme car la fonction sin ou cos ne donne jamais une valeur supérieur à 1) "
	larg, haut = largeur, hauteur
	rayoncercle, centre = haut/2-30, larg/2-30 # l'appel de la variable hauteur permet d'automatiquement adapter la figure au canevas
	if haut>larg:
		passage = haut
		larg = haut
		haut = passage
		ang = ang + 0.1 # décalage de 0.1 radian
		x1, y1 = sin(ang), cos(ang)
		x1, y1 = x1*centre + centre+30, y1*centre + rayoncercle
		can1.coords(oval1, x1-15, y1-15, x1+15, y1+15)
	else:
		ang = ang + 0.1 # décalage de 0.1 radian
		x1, y1 = sin(ang), cos(ang)
		x1, y1 = x1*rayoncercle + centre, y1*rayoncercle + rayoncercle+30
		can1.coords(oval1, x1-15, y1-15, x1+15, y1+15)
	if flag > 0:
		fen1.after(50, move_cercle) #Déclenche l'appel à la fonction après un laps de temps défini (ici 50 millisecondes)




def stop_it():
	"arrêt de l'animation"
	global flag
	flag = 0




def normal_start_it():
	"démarrage de l'animation"
	global flag
	"Afin d'éviter de déclencher l'appel à la fonction move de plus en plus souvent lorsque on clic sur Démarrer il faut mettre cette sécurité"
	"Si on n'ajoute pas cette condition alors on 'cumule' les fonctions move et on voit donc la balle qui accélère de plus en plus à chaques clic"
	if flag == 0: #Verification permettant de ne lancer qu'une seule boucle (si stop_it n'est pas utilisé avant cette fonction ne fait rien)
		flag = 1
		move()



def zigzag_start_it():
	"démarrage de l'animation"
	global flag
	if flag == 0: #Verification permettant de ne lancer qu'une seule boucle (si stop_it n'est pas utilisé avant cette fonction ne fait rien)
		flag = 1
		move_zigzag()




def cercle_start_it():
	"démarrage de l'animation"
	global flag
	if flag == 0: #Verification permettant de ne lancer qu'une seule boucle (si stop_it n'est pas utilisé avant cette fonction ne fait rien)
		flag = 1
		move_cercle()


######################################################
############## Programme principal : #################
######################################################

"Variable à utilisation globale"
x1, y1, dx, dy, flag, ang = 10, 10, 15, 0, 0, 0 #dx et dy représente le pas de déplacement et flag le commutateur on off

hauteur = 250
largeur = 500

fen1 = Tk()
fen1.title("Récursivité avec une balle")

can1 = Canvas(fen1, bg = 'dark grey', height = hauteur, width = largeur)
can1.grid(row = 1, column = 1, rowspan= 5, padx = 5, pady = 5)
oval1 = can1.create_oval(x1, y1, x1+30, y1+30, width = 2, fill = 'red')
bou2 = Button(fen1, text = 'Normal', width = 8, command = normal_start_it).grid(row = 1, column = 2)
bou3 = Button(fen1, text = 'Zig-Zag', width = 8, command = zigzag_start_it).grid(row = 2, column = 2)
bou3 = Button(fen1, text = 'Circulaire', width = 8, command = cercle_start_it).grid(row = 3, column = 2)

bou3 = Button(fen1, text = 'Arrêter', width = 8, command = stop_it).grid(row = 4, column = 2)
bou1 = Button(fen1, text = 'Quitter', width = 8, command = fen1.quit).grid(row = 6, column = 2)

fen1.mainloop()
