#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""POGRAMME INITIANT AU DEPLACEMENT D'ÉLÉMENTS DU CANEVAS"""
"COUR 14 EVENEMENT ET CANEVAS"

#########################################
### Importation fonction et modules : ###
#########################################


from tkinter import *
from random import randrange


############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


# ----- Création des Classes ----- #


##### CLASSE PRINCIPALE #####


class BacSable(Canvas):
    """Prise en compte d'actions de la souris"""
    def __init__(self, boss, width=80, height=80, bg='white'):
        Canvas.__init__(self, boss, width=width, height=height, bg=bg)
        self.boss = boss
        self.width = width
        self.height = height
        self.bg = bg
        self.bind("<Button-1>", self.mouseDown)
        self.bind("<Button1-Motion>", self.mouseMove)
        self.bind("<Button1-ButtonRelease>", self.mouseUp)

    def mouseDown(self, event):
        """Opération lorsque clic gauche utilisé"""
        self.x1, self.y1 = event.x, event.y  # Coordonnées du clic
        # La méthode fin.closest() renvoie référence du dessin le plus proche
        self.selObject = self.find_closest(self.x1, self.y1)
        # On met en valeur l'objet selectionné
        self.itemconfig(self.selObject, width=3)
        # On met au premier plan l'élément selectionné
        self.lift(self.selObject)

    def mouseMove(self, event):
        """Opération lors d'un déplacement avec maointient du clic gauche"""
        x2, y2 = event.x, event.y
        dx, dy = x2 - self.x1, y2 - self.y1
        if self.selObject:
            self.move(self.selObject, dx, dy)  # On décale de dx et dy
            self.x1, self.y1 = x2, y2  # On modifie les coordonnées initiales

    def mouseUp(self, event):
        """Opération lorsque on relache l'object"""
        if self.selObject:
            # On retire la mise en valeur par la bordure
            self.itemconfig(self.selObject, width=1)
            self.selObject = None  # On déselectionne l'élément


#############################
### Programme principal : ###
#############################


if __name__ == '__main__':
    couleurs = ("red", "orange", "yellow", "green", "cyan", "dark blue", "light blue", "violet", "purple")
    fen = Tk()
    # Mise en place du canvas avec 15 ellipses en position aléatoire
    bac = BacSable(fen, width=400, height=400, bg='ivory')
    bac.pack(padx=8, pady=8)
    # Trace des 15 ellipses par une boucle
    for el in range(15):
        coul = couleurs[randrange(len(couleurs))]
        x1, y1 = randrange(300), randrange(300)
        x2, y2 = x1 + randrange(10, 150), y1 + randrange(10, 150)
        bac.create_oval(x1, y1, x2, y2, fill=coul)
    fen.mainloop()
