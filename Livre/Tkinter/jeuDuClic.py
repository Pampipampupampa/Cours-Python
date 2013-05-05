#! /usr/bin/env python
# -*- coding:Utf8 -*-

"PETIT JEU OÙ IL FAUT CLIQUER SUR UNE BALLE QUI VA DE PLUS EN PLUS VITE"

################################################################
############# Importation fonction et modules : ################
################################################################



from tkinter import *
from random import randrange
from math import cos, sin



###################################################################################################
############# Gestion d'évènements : définition de différentes fonctions utiliées  : ##############
###################################################################################################



def move():
	"deplacement de la balle"
	global x1, y1, dy, dx, flag, vitesse
	x1, y1 = x1 + dx, y1 + dy

	if x1>largeur-50 or x1<50:
		dx = -dx
	if y1>hauteur-50 or y1<50:
		dy = -dy
	if x1>=20 and x1<=largeur-20:
		dx = randrange(-50, 50, 1)
		dy = randrange(-50, 50, 1)
	if y1>=20  and y1<=hauteur-20:
		dx = randrange(-50, 50, 1)
		dy = randrange(-50, 50, 1)


	can1.coords(oval1, x1-balle, y1-balle, x1+balle, y1+balle)
	if flag > 0:
		fen1.after(vitesse, move) #Déclenche l'appel à la fonction après un laps de temps défini dans la variable vitesse



def stop_it():
	"arrêt de l'animation"
	global flag
	flag = 0



def start_it():
	"démarrage de l'animation"
	global flag
	"Afin d'éviter de déclencher l'appel à la fonction move de plus en plus souvent lorsque on clic sur Démarrer il faut mettre cette sécurité"
	"Si on n'ajoute pas cette condition alors on 'cumule' les fonctions move et on voit donc la balle qui accélère de plus en plus à chaques clic"
	if flag == 0: #Verification permettant de ne lancer qu'une seule boucle (si stop_it n'est pas utilisé avant cette fonction ne fait rien)
		flag = 1
		move()



def cercle_start_it():
	"démarrage de l'animation"
	global flag
	if flag == 0: #Verification permettant de ne lancer qu'une seule boucle (si stop_it n'est pas utilisé avant cette fonction ne fait rien)
		flag = 1
		move_cercle()
 


def clicBalle(event):
    global x, y, score, flag, vitesse
 
    if flag == 1:
 
        if event.x >= x1-detection and event.x <= x1+detection and event.y >= y1-detection and event.y <= y1+detection:
            score += 1
            vitesse -= 25

            afficheScore.configure(text= "Points: "+str(score))
            gameOver()



def gameOver():
    global score, flag
 
    if score == 10:
        afficheScore.configure(text= "Bravo! Score Final: "+str(score))
        stop_it()



def recommence():
	"Permet de relancer le jeu"
	global flag, vitesse, score, x1, y1
	"Afin d'éviter de déclencher l'appel à la fonction move de plus en plus souvent lorsque on clic sur Démarrer il faut mettre cette sécurité"
	"Si on n'ajoute pas cette condition alors on 'cumule' les fonctions move et on voit donc la balle qui accélère de plus en plus à chaques clic"
	if flag == 0: #Verification permettant de ne lancer qu'une seule boucle (si stop_it n'est pas utilisé avant cette fonction ne fait rien)
		vitesse, score = 250, 0
		x1, y1 = largeur/2, hauteur/2
		afficheScore.configure(text= "Points: "+str(score))
		flag = 1
		move()



######################################################
############## Programme principal : #################
######################################################

"Taille du canevas (vérifier que la balle a des coordonnées de départ qui y rentre)"
hauteur = 800
largeur = 800

"Variable à utilisation globale"
x1, y1, dx, dy, flag, ang = largeur/2, hauteur/2, 10, 0, 0, 0 #dx et dy représente le pas de déplacement et flag le commutateur on off

"Autres variables"
vitesse = 250
score = 0
balle = 15
detection = 20

"Fenêtre et éléments principaux"
fen1 = Tk()
fen1.title("Seras tu assez rapide pour gagner ?")
can1 = Canvas(fen1, bg = 'dark grey', height = hauteur, width = largeur)
can1.grid(row = 1, column = 1, rowspan= 3, padx = 5, pady = 5)

"Création du score"
can1.bind("<Button-1>", clicBalle)
afficheScore = Label(fen1, text= "Points: 0")
afficheScore.grid(row = 4, column = 1, columnspan = 4, padx = 10, pady = 10)

"Balle"
oval1 = can1.create_oval(x1-balle, y1-balle, x1+balle, y1+balle, width = 2, fill = 'red')

"Bouttons"
bou2 = Button(fen1, text = 'Démarrer', width = 8, command = start_it).grid(row = 1, column = 4)
bou4 = Button(fen1, text = 'Arrêter', width = 8, command = stop_it).grid(row = 3, column = 4)
bou4 = Button(fen1, text = 'Relancer', width = 8, command = recommence).grid(row = 2, column = 4)

bou1 = Button(fen1, text = 'Quitter', width = 8, command = fen1.quit).grid(row = 4, column = 4)


fen1.mainloop()
