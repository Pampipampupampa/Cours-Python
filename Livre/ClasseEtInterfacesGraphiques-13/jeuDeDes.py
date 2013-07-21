#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""PROGRAMME RÉALISANT UN PETIT JEU DE DÉS"""
"EXERCICE 13.23"

#########################################
### Importation fonction et modules : ###
#########################################


from tkinter import *


############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


# ----- Création des Classes ----- #


class FaceDom(object):
    """Création de dominos avec différents nombre de points"""
    def __init__(self, can, val, position, taille=70):
        self.can = can
        self.val = val
        self.taille = taille
        # Récupération des coordonnées du point
        x, y, c = position[0], position[1], taille/2
        d = taille/3
        can.create_rectangle(x-c, y-c, x+c, y+c, fill='ivory', width=2)
        # Création du receptionneur de références
        self.pList = []
        # Position des points sur les dés
        pDispo = [((0, 0),),
                  ((-d, d), (d, -d)),
                  ((-d, -d), (0, 0), (d, d))]
        disp = pDispo[val-1]  # Permet de retenir que les points utiles
        # Ajout des point au dé
        for p in disp:
            self.cercle(x+p[0], y+p[1], taille/10, 'red')

    def cercle(self, x, y, r, coul):
        self.pList.append(self.can.create_oval(x-r, y-r, x+r, y+r, fill=coul))

    def effacer(self):
        for p in self.pList:
            self.can.delete(p)


##### CLASSE PRINCIPALE #####


class Application(Frame):
    """Gestionnaire des évènement et interface graphique"""
    def __init__(self, larg=600, haut=600):
        Frame.__init__(self)
        self.larg = larg
        self.haut = haut
        self.can = Canvas(self, bg='dark green', width=larg, height=haut)
        self.can.pack(padx=5, pady=5)
        # Liste des bouttons avec leur texte
        bList = [("A", self.boutA), ("B", self.boutB), ("C", self.boutC),
                 ("D", self.boutD), ("Quitter", self.boutQuitter)]
        for b in reversed(bList):  # Parcours inverse de la liste
            Button(self, text=b[0], command=b[1]).pack(side=RIGHT,
                                                       padx=5, pady=5)
        self.pack()

    def boutA(self):
        self.d3 = FaceDom(self.can, 3, (100, 100), 50)

    def boutB(self):
        self.d2 = FaceDom(self.can, 2, (200, 100), 80)

    def boutC(self):
        self.d1 = FaceDom(self.can, 1, (350, 100), 110)

    def boutD(self):
        self.d3.effacer()

    def boutQuitter(self):
        self.master.destroy()


#############################
### Programme principal : ###
#############################


Application().mainloop()
