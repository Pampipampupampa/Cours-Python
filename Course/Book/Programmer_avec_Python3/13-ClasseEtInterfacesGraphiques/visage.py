#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""PROGRAMME AFFICHANT UN VISAGE QUI FERME ET OUVRE LA BOUCHE"""
"EXERCICE 13.21"

#########################################
### Importation fonction et modules : ###
#########################################


from tkinter import *


############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


# ----- Création des Classes ----- #

class Visage(Canvas):
    """Création d'un visage simpliste"""
    def __init__(self, boss=None, haut=400, larg=400, rayonTete=100):
        Canvas.__init__(self)
        self.configure(height=haut, width=larg)
        self.rayonTete = rayonTete
        self.haut = haut
        self.larg = larg
        # Conteneur des coordonnees des elements du visage (x, y , r, couleur)
        # Ordre : tête, yeux, bouche
        self.coordVisage = [[larg/2, haut/2, rayonTete, 'pink'],
                            [0.7*larg/2, 0.8*haut/2, 0.15*rayonTete, 'pink'],
                            [1.3*larg/2, 0.8*haut/2, 0.15*rayonTete, 'pink'],
                            [larg/2, 1.20*haut/2, 0.30*rayonTete, 'red']]
        self.nbrRond = len(self.coordVisage)

    def dessineTete(self, selecteur):
        """Dessine un des éléments de <self.coordVisage>"""
        # Selection de l'élément <selecteur> du visage correspondant
        parameter = self.coordVisage[selecteur]
        ref = self.create_oval(parameter[0]-parameter[2],
                               parameter[1]-parameter[2],
                               parameter[0]+parameter[2],
                               parameter[1]+parameter[2],
                               fill=parameter[3], width=3)
        return ref

    def fermeBouche(self, selecteur):
        """Remplace <selecteur> par la référence d'une ligne horizontale"""
        # Selection de l'élément du visage correspondant
        parameter = self.coordVisage[selecteur]
        ref = self.create_line(parameter[0]-parameter[2], parameter[1],
                               parameter[0]+parameter[2], parameter[1],
                               fill=parameter[3], width=5)
        return ref


##### CLASSE PRINCIPALE #####


class Application(Frame):
    """Reception et création des différents widgets"""
    def __init__(self):
        Frame.__init__(self)
        self.master.title("Animation d'un visage")
        # Ajout du canevas
        self.canevas = Visage(Application)
        self.canevas.configure(bg='light blue')
        self.canevas.pack(side=TOP)
        # Ajout des bouttons
        Button(self, text='Ouvre la Bouche !', bg='light blue', fg='black',
               command=self.ouvreBouche, activebackground='pink').pack()
        Button(self, text='Ferme la Bouche !', bg='light blue', fg='black',
               command=self.fermeBouche, activebackground='pink').pack()
        # Ajout du visage
        self.trace = []
        for i in range(self.canevas.nbrRond):
            self.trace.append(self.canevas.dessineTete(i))
        # Ajout du flag vérifiant l'état actuel du visage
        self.etat = 1  # 1 = bouche ouverte, 0 bouche fermée
        # Position de la frame
        self.pack()

    def ouvreBouche(self):
        """Ouvre la Bouche du visage si fermée"""
        if not self.etat:
            # Efface un élément du canevas à partir de sa référence
            self.canevas.delete(self.trace[3])
            # Remplace l'élément effacé précédemment
            self.trace[3] = self.canevas.dessineTete(3)
            self.etat = 1

    def fermeBouche(self):
        """Ferme la bouche du visage si ouverte"""
        if self.etat:
            # Efface un élément du canevas à partir de sa référence
            self.canevas.delete(self.trace[3])
            # Remplace l'élément effacé précédemment
            self.trace[3] = self.canevas.fermeBouche(3)
            self.etat = 0


#############################
### Programme principal : ###
#############################


Application().mainloop()
