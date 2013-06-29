#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""PROGRAMME UTILISANT L'HÉRITAGE ET L'ÉCHANGE D'INFORMATIONS"""
"PETIT TRAIN COURS 13 ET EXERCICES 13.6 ET 13.7"

###########################################
#### Importation fonction et modules : ####
###########################################


from tkinter import *


###############################################################################
#### Gestion d'évènements : définition de différentes Fonctions/Classes : #####
###############################################################################


############# Création des Classes #############

class Application(Tk):
    """Génération de la fenêtre principale du programme"""
    def __init__(self):
        Tk.__init__(self)  # Constructeur de la classe parente
        self.can = Canvas(self, width=475, height=130, bg='white')
        self.can.pack(side=TOP, padx=5, pady=5)
        Button(self, text="Train", command=self.dessine).pack(side=LEFT)
        Button(self, text="Hello", command=self.coucou).pack(side=LEFT)
        Button(self, text='Lumière',
               command=self.eclairement134).pack(side=LEFT)

    def dessine(self):
        """Instanciation des 4 wagons"""
        self.w1 = Wagon(self.can, 10, 30, 'red')
        self.w2 = Wagon(self.can, 130, 30, 'red')
        self.w3 = Wagon(self.can, 250, 30, 'red')
        self.w4 = Wagon(self.can, 370, 30, 'red')

    def coucou(self):
        """Fait apparaître des personnages dans les wagons"""
        try:  # On vérifie l'existence des wagons
            self.w1
        except AttributeError:  # Si ils existent pas on les ajoutes
            self.dessine()
        self.w1.perso(3)  # 1er wagon, 3ème fenêtre
        self.w3.perso(1)  # 3er wagon, 1ème fenêtre
        self.w3.perso(2)  # 3er wagon, 2ème fenêtre
        self.w4.perso(1)  # 4er wagon, 1ème fenêtre

    def eclairement134(self):
        """Allumage des wagons 1, 2, et 3"""
        try:  # On vérifie l'existence des wagons
            self.w1
        except AttributeError:  # Si ils existent pas on les ajoutes
            self.dessine()
        self.w1.allumer()
        self.w3.allumer()
        self.w4.allumer()


class Wagon(object):
    """Générateur du train et des passagers"""
    def __init__(self, canev, x, y, couleur):
        """Dessin du train dans le canevas <canev>"""
        self.canev = canev
        self.x = x
        self.y = y
        self.couleur = couleur
        # Création du bloc du wagon
        canev.create_rectangle(x, y, x+95, y+60, fill=couleur)
        # Création des fenêtres
        self.fen = []
        for xf in range(x+5, x+90, 30):
            self.fen.append(canev.create_rectangle(xf, y+5,
                                                   xf+25, y+40, fill='black'))
        print(self.fen)  # Permet de voir ce qui est mémorisé
        # Création des roues
        cercle(canev, x+18, y+73, 12, 'grey')
        cercle(canev, x+77, y+73, 12, 'grey')

    def perso(self, fen):
        """Apparition d'un personnage à la fenêtre"""
        # Détermination du centre de chaques fenêtres
        xf = self.x + fen*30 - 12
        yf = self.y + 25
        cercle(self.canev, xf, yf, 10, 'pink')     # Visage
        cercle(self.canev, xf-5, yf-3, 2)  # Oeil Gauche
        cercle(self.canev, xf+5, yf-3, 2)  # Oeil Droit
        cercle(self.canev, xf, yf+5, 3)    # Bouche

    def allumer(self):
        """Allumage d'un wagon"""
        for fenetre in self.fen:
            self.canev.itemconfigure(fenetre, fill='yellow')


############# Création des Fonctions #############


def cercle(can, x, y, r, couleur='white'):
    """Dessin d'un cercle de rayon <r> en <x, y> dans le canvevas <can>"""
    can.create_oval(x-r, y-r, x+r, y+r, fill=couleur)


###############################
#### Programme principal : ####
###############################


Application().mainloop()
