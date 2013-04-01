#! /usr/bin/env python
# -*- coding:Utf8 -*-



"PROGRAMME AUTOUR DE L'ATTRACTION TERRESTRE"


################################################################
############# Importation fonction et modules : ################
################################################################


from tkinter import *
from math import sqrt



###################################################################################################
############# Gestion d'évènements : définition de différentes fonctions utiliées  : ##############
###################################################################################################


def avance(n, xcoord, ycoord):
	"Procédure générale"
	global x, y
	x[n], y[n] = x[n] + xcoord, y[n] + ycoord
	can1.coords(astre[n], x[n], y[n], x[n]+30, y[n]+30)
	"distance entre le 2 astres"
	distanceastres = mesuredistance(x[0], x[1], y[0], y[1])
	"distance en km entre les 2 astres"
	distancereele = distanceastres * 1e9 # assimile 1 pixel à 1 000 000 de km
	"force gravittionelle entre les 2 astres"
	force =  forceG(m1, m2, distancereele)
	distance.configure(text = 'Distance de ' + str(distancereele) + ' Km')
	forcegrav.configure(text = 'Force de ' + str(force) + ' KN')
	decalage = distanceastres / 10


def forceG(m1, m2, distanceastres):
	"force de gravitation s'exerçant entre m1 et m2 pour une distance di"
	return int((m1*m2*6.67e-11/distanceastres**2)/1000)

def mesuredistance(x1, x2, y1, y2):
	d = int(sqrt((x2 - x1)**2 + (y2 - y1)**2))
	return d


def deplacement_gauche1():
	avance(0, -decalage, 0)

def deplacement_droite1():
	avance(0, decalage, 0)

def deplacement_bas1():
	avance(0, 0, decalage)

def deplacement_haut1():
	avance(0, 0, -decalage)

def deplacement_gauche2():
	avance(1, -decalage, 0)

def deplacement_droite2():
	avance(1, decalage, 0)

def deplacement_bas2():
	avance(1, 0, decalage)

def deplacement_haut2():
	avance(1, 0, -decalage)




######################################################
############## Programme principal : #################
######################################################


"coordonnées de base"
x = [50, 10] # liste pour les coordonnées en x des astres
y = [100, 50] # liste pour les coordonnées en y des astres


"taille pointeur"
xx, yy = 30, 30


"masse des astres"
m1 = 6e24
m2 = 6e24

"décalage de base"
decalage = 5

"Liste permettant de mémoriser les indices du dessin"
astre = [0]*2 # liste servant à mémoriser les références des dessins


"widgets"
fen1 = Tk()
fen1.title("Attration atrale")
can1 = Canvas(fen1, width = 400, height = 200, bg = 'grey')
can1.grid(row =2, column =1, columnspan =3, padx = 20, pady = 20)
astre[0] = can1.create_oval(x[0], y[0], x[0]+xx, y[0]+yy, width = 2, fill = 'blue')
astre[1] = can1.create_oval(x[1], y[1], x[1]+xx, y[1]+yy, width = 2, fill = 'green')



"textes des différentes fenêtres"
valmasse1 = Label(fen1, text = 'Astre 1 : '+ str(m1) + ' Kg')
valmasse2 = Label(fen1, text = 'Astre 2 : '+ str(m2) + ' Kg')
distance = Label(fen1)
forcegrav = Label(fen1)
valmasse1.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = W)
valmasse2.grid(row = 1, column = 3, padx = 5, pady = 5, sticky = E)
distance.grid(row = 4, column = 1, padx = 5, pady = 5)
forcegrav.grid(row = 4, column = 3, padx = 5, pady = 5)


############################################

"GROUPE ASTRE 1 AVEC 4 BOUTTONS"
fra1 = Frame(fen1) # association dans un cadre un ensemble de bouttons
fra1.grid(row = 3, column = 1, sticky = W, padx = 10, pady = 10)

Button(fra1, fg = 'blue', command = deplacement_bas1, text = 'v').pack(side = LEFT)
Button(fra1, fg = 'blue', command = deplacement_haut1, text = '^').pack(side = LEFT)
Button(fra1, fg = 'blue', command = deplacement_droite1, text = '->').pack(side = LEFT)
Button(fra1, fg = 'blue', command = deplacement_gauche1, text = '<-').pack(side = LEFT)


"GROUPE ASTRE 2 AVEC 4 BOUTTONS"
fra2 = Frame(fen1)
fra2.grid(row = 3, column = 3, sticky = E, padx = 10, pady = 10)

Button(fra2, fg = 'green', command = deplacement_bas2, text = 'v').pack(side =LEFT)
Button(fra2, fg = 'green', command = deplacement_haut2, text = '^').pack(side =LEFT)
Button(fra2, fg = 'green', command = deplacement_droite2, text = '->').pack(side =LEFT)
Button(fra2, fg = 'green', command = deplacement_gauche2, text = '<-').pack(side =LEFT)

#############################################

Button(fen1, command = fen1.quit, text = 'Quitter').grid(row = 5, column = 3)

fen1.mainloop()

















