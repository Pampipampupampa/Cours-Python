#! /usr/bin/env python
# -*- coding:Utf8 -*-

############################################
##                                        ##
##  Initiation aux interfaces graphiques  ##
##                                        ##
############################################


"""PREMIER PAS"""

from tkinter import * # importe les fonction du module tkinter
fen1 = Tk() # création d'une fenêtre

# ajout d'un texte esclave de la fenêtre et de couleur bleu
tex1 = Label(fen1, text = "Bonjour bonhomme !! ", fg = "blue")
tex1.pack() # permet de réduire la fenêtre afin de voir l'ensembl

# ajout d'une boutton pour quitter la fenêtre
bou1 = Button(fen1, text = "Commencer", command = fen1.destroy)
bou1.pack()
fen1.mainloop() # permet d'initier la boucle du réceptionneur d'évènements (permet de scruter clavier, souris, ect)




"""TRACE DE LIGNE DE CANEVAS"""


# ----- gestionnaire d'évènements : definition des fonctions ----- #

def drawline():
    "trace une ligne dans le canevas can1"
    global x1, y1, x2, y2, coul
    can1.create_line(x1,y1,x2,y2,width=2,fill=coul)
    y2, y1 = y2 - 5, y1 - 5 # modification des coordonnées pour la ligne suivante

def changecolor():
    "changement aléatoire de la couleur"
    global coul
    pal = ["purple", "cyan", "maroon", "green", "red", "blue", "orange", "yellow"]
    c = randrange(1,7) # génère un nombre aléatoire entre 0 et 7
    coul = pal[c] # assigne la couleur correspondante au numéro tiré aléatoirement

def drawline2():
    "trace une croix au centre de la zone de tracage"
    hx1, hy1, hx2, hy2= 0, 325, 400, 325, 
    vx1, vy1, vx2, vy2= 200, 525, 200, 125
    can1.create_line(hx1,hy1,hx2,hy2,width=2,fill=coul)
    can1.create_line(vx1,vy1,vx2,vy2,width=2,fill=coul)
    

# ----- Programme principal ----- #

from tkinter import *
from random import randrange # importe la fonction aléatoire

# utiliation de manière globale les variables ci dessous
x1, y1, x2, y2 = 0, 650, 400, 650 # coordonnées ligne
coul = "grey"
# création du widget maître
fen1 = Tk()
# création des widgets esclaves
can1 = Canvas(fen1,bg="dark grey", height = 650, width = 400)
can1.pack(side=LEFT)
bou1 = Button(fen1, text = "Quitter", command = fen1.quit)
bou1.pack(side=BOTTOM)
bou2 = Button(fen1, text="Tracer une ligne", command=drawline)
bou2.pack()
bou3 = Button(fen1, text="Autre couleur", command=changecolor)
bou3.pack()
bou4 = Button(fen1, text = "Viseur", command = drawline2)
bou4.pack()

fen1.mainloop() # démarrage du receptionnaire d'évènements

fen1.destroy()




"""CREER LES ANNEAUX DES JEUX OLYMPIQUES"""

# ----- Définitions des fonctions ----- #

def dessine_cercle(i):
    x1, y1 = coord[i][0], coord[i][1]
    can1.create_oval(x1, y1, x1 + 100, y1 + 100, outline = coul[i], width = 2)

def a1():
    dessine_cercle(0)

def a2():
    dessine_cercle(1)

def a3():
    dessine_cercle(2)

def a4():
    dessine_cercle(3)

def a5():
    dessine_cercle(4)

# ----- Programme principal ----- #

# coordonnées des anneaux
coord = [[20,30], [120,30], [220,30], [70,80], [170,80]]
# couleur des anneaux
coul = ["red", "yellow", "blue", "green", "black"]


base = Tk()
bou1 = Button(base, text = "Quitter", command = base.destroy)
bou1.pack(side=BOTTOM)
can1 = Canvas(base, bg="white", height = 200, width = 335)
can1.pack(side=LEFT)

# les différents boutons
Button(base, text = "1", command = a1).pack(side = LEFT)
Button(base, text = "2", command = a2).pack(side = LEFT)
Button(base, text = "3", command = a3).pack(side = LEFT)
Button(base, text = "4", command = a4).pack(side = LEFT)
Button(base, text = "5", command = a5).pack(side = LEFT)

    
base.mainloop()
    
    

























