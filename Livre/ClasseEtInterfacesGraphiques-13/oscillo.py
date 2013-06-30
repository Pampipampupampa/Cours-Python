#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""WIDGET TKINTER SPÉCIALISÉ DANS LA RÉALISATION DE GRAPHE D'ÉLONGATION"""
"EXERCICES 13.9 À 13.12 (13.12 NON COMPRIS)"

###########################################
#### Importation fonction et modules : ####
###########################################


from tkinter import *
from math import sin, pi


###############################################################################
#### Gestion d'évènements : définition de différentes Fonctions/Classes : #####
###############################################################################


############# Création des Classes #############


class OscilloGraphe(Canvas):
    """Canevas pour le dessin de courbes élongation/temps"""
    def __init__(self, boss=None, larg=400, haut=250):
        """Constructeur du graphique : axes et échelle horizontale"""
        Canvas.__init__(self)
        self.configure(width=larg, height=haut)
        self.boss = boss
        self.larg = larg
        self.haut = haut
        # Tracé d'une échelle avec 8 graduations sur l'horizontale
        pas = (larg-25)/8  # Intervalle des graduations
        for t in range(1, 9):
            stx = 10 + t*pas  # + 10 permet de commencer sur le début de l'axe
            self.create_line(stx, haut, stx, 15, fill='grey')
        # Tracé d'une échelle avec 10 graduations sur la verticale
        pas = (haut-25)/10
        for t in range(-5, 6):
            sty = haut/2 - t*pas
            self.create_line(6, sty, larg-15, sty, fill='grey')
        self.axes()

    def axes(self):
        """Création des axes de références"""
        # Création de l'axe X
        self.create_line(10, self.haut/2, self.larg, self.haut/2,
                         arrow=LAST, fill='black')
        self.create_text(20, 10, text="e", anchor=CENTER)
        # Création de l'axe Y
        self.create_line(10, self.haut-5, 10, 5, arrow=LAST, fill='black')
        self.create_text(self.larg-5, self.haut/2-10, text="t", anchor=CENTER)

    def traceCourbe(self, freq=1, phase=0, ampl=10, coul='red'):
        """Tracé d'un graphique élongation/temps sur 1 seconde"""
        curve = []  # Mémorisation de la liste des coordonnées
        pas = (self.larg-25)/1000  # Passage en milliseconde
        for t in range(0, 1001, 5):
            e = ampl*sin(2*pi*freq*t/1000 - phase)
            x = 10 + t*pas
            # Pour <y> il faut se mettre au centre horizontalement
            # puis ajouter ou soustraire l'élongation
            y = self.haut/2 - e*self.haut/25  # /25 --> modification échelle
            curve.append((x, y))  # Ajout de chaques points
        n = self.create_line(curve, fill=coul, smooth=1)
        return n


############# Création des Fonctions #############


###############################
#### Programme principal : ####
###############################


if __name__ == '__main__':
    root = Tk()
    graph = OscilloGraphe(root, larg=500, haut=500)
    graph.pack()
    graph.configure(bg='ivory', bd=2, relief=SUNKEN)
    graph.traceCourbe(2, 1.2, 10, 'purple')
    root.mainloop()
