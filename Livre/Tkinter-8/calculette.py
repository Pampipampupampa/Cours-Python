#! /usr/bin/env python
# -*- coding:Utf8 -*-


" CREATION D'UNE CALCULETTE"


############# Importation fonction et modules : ################


from math import *
from tkinter import *


############# Gestion d'évènements : définition de différentes fonctions utiliées  : ##############


def evaluer(event):
	"Permet de modifier la variable chaine afin d'ajouter le résultat du calcul"
	chaine.configure(text = "Résultat = " + str(eval(entree.get())))


############## Programme principal : #################


fenetre = Tk()
entree = Entry(fenetre) # ajoute un champs dans la fenêtre où l'utilisateur peut rentrer la formule
entree.bind("<Return>", evaluer) # création d'un raccourci pour finaliser le calcul
chaine = Label(fenetre) # ajoute un emplacement pour du texte sur l'interface
entree.pack()
chaine.pack()
fenetre.mainloop()


