#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""PROGRAMME RÉALISANT UN PETIT JEU DE DÉS"""
"EXERCICE 13.23 PARTIE A "

#########################################
### Importation fonction et modules : ###
#########################################


from tkinter import *
from random import randrange


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
        self.carre = can.create_rectangle(x-c, y-c, x+c, y+c, fill='ivory',
                                          width=2)
        # Création du receptionneur de références
        self.pList = []
        # Position des points sur les dés
        pDispo = [((0, 0),),
                  ((-d, d), (d, -d)),
                  ((-d, -d), (0, 0), (d, d)),
                  ((-d, -d), (-d, d), (d, -d), (d, d)),
                  ((-d, -d), (-d, d), (d, -d), (d, d), (0, 0)),
                  ((-d, -d), (-d, d), (d, -d), (d, d), (d, 0), (-d, 0))]
        disp = pDispo[val-1]  # Permet de retenir que les points utiles
        # Ajout des point au dé
        for p in disp:
            self.cercle(x+p[0], y+p[1], taille/10, 'red')

    def cercle(self, x, y, r, coul):
        self.pList.append(self.can.create_oval(x-r, y-r, x+r, y+r, fill=coul))

    def effacer(self, flag=0):
        for p in self.pList:
            self.can.delete(p)
        if flag:
            self.can.delete(self.carre)


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
        self.des = []  # Contient les références des différents dés
        self.valAl = []  # Conteneur des valeurs des dés
        self.positionX = 0
        self.pack()

    def boutA(self):
        self.valAl = ""
        decalage = 150
        self.positionX += 40
        for nbr in range(3):
            nbrAl = randrange(1, 7)
            self.valAl += str(nbrAl)
            self.des.append(FaceDom(self.can, nbrAl,
                                   (self.positionX, decalage), 20))
            decalage += 150
        if self.verifResultat(self.valAl) == "win":
            self.texte = self.can.create_text(self.larg/2, self.haut,
                                              text="GAGNÉ", anchor="s",
                                              font=("Purisa", 40))

    def verifResultat(self, val):
        resultat = 0
        if val[0] != val[1] and val[0] != val[2] and val[1] != val[2]:
            for car in val:
                if car in '421':
                    resultat += 1
        if resultat == 3:
            return "win"
        else:
            return "try again"

    def boutB(self):
        self.d2 = FaceDom(self.can, 6, (40, 300), 80)

    def boutC(self):
        for i in range(len(self.des)):
            pass

    def boutD(self):
        for i in range(len(self.des)):
            self.des[i].effacer(1)
        self.des = []
        self.positionX = 0
        try:
            self.texte
        except AttributeError:
            pass
        else:
            self.can.delete(self.texte)

    def boutQuitter(self):
        self.master.destroy()


#############################
### Programme principal : ###
#############################


Application().mainloop()
