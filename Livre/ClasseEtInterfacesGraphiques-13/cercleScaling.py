#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""PROGRAMME PERMETTANT DE FAIRE VARIER LA TAILLE D'UN DISQUE"""
"EXERCICE 13.20"

###########################################
#### Importation fonction et modules : ####
###########################################


from tkinter import *


###############################################################################
#### Gestion d'évènements : définition de différentes Fonctions/Classes : #####
###############################################################################


############# Création des Classes #############


class ParametreCercle(Frame):
    """Génère les paramètres du cercle"""
    def __init__(self, boss=None, couleur='navy'):
        Frame.__init__(self)
        self.couleur = couleur
        self.rayon = 0
        # Création de la case à cocher afin d'afficher le cercle
        self.chk = IntVar()  # Instanciation d'un Objet variable tkinter
        Checkbutton(self, text='Afficher', variable=self.chk, fg=couleur,
                    command=self.active).pack(side=LEFT)
        # Création du curseur
        Scale(self, length=500, orient=HORIZONTAL, label='Rayon du cercle :',
              troughcolor=couleur, sliderlength=20, showvalue=1, from_=0,
              to=300, tickinterval=20, resolution=1,
              command=self.setRayon).pack(side=LEFT, padx=10, pady=10)

    def active(self):
            """Création d'un évènement pour indiquer que la case est cochée"""
            self.event_generate('<Control-Z>')

    def setRayon(self, r):
            """Modification de la valeur du rayon"""
            self.rayon = float(r)
            self.event_generate('<Control-Z>')

    def valeurs(self):
        """Tuple des paramètres du cercle"""
        return (self.rayon)


class DessineCercle(Canvas):
    """Génère un canevas avec ajout de cercle possible"""
    def __init__(self, boss=None, larg=600, haut=600):
        Canvas.__init__(self)
        self.configure(width=larg, height=haut)
        self.larg = larg
        self.haut = haut

    def traceCercle(self, rayon):
        """Dessine le cercle dans le canevas"""
        ref = self.create_oval(self.larg/2-rayon, self.haut/2-rayon,
                               self.larg/2+rayon, self.haut/2+rayon,
                               width=2, fill='orange')
        return ref


#####################
# CLASSE PRINCIPALE #
#####################
class Root(Frame):
    """Classe principale + gestionnaire d'évènement"""
    def __init__(self, master=None):
        Frame.__init__(self)
        # Ajout du canevas contenant le cercle
        self.dessin = DessineCercle(Root)
        self.dessin.configure(bg='navy', relief=SOLID, bd=2)
        self.dessin.pack(padx=5, pady=5, side=TOP)
        # Ajout du bloc contenant les paramètres du cercle
        self.parametre = ParametreCercle(Root)
        self.parametre.configure(relief=GROOVE, bd=2)
        self.parametre.pack(padx=10, pady=10)
        # Ajout de l'évènement déclenchant le tracé du cercle
        self.master.bind('<Control-Z>', self.montreCercle)
        # Ajout du titre grâce à <master>
        self.master.title("Cercle Magique")
        # Mémorisation du cercle créé
        self.trace = [0]
        # Position dans la fenêtre (utile si on veut le réutiliser)
        self.pack(padx=10, pady=10)

    def montreCercle(self, event):
        """Modification de la valeur du rayon"""
        # Suppression du cercle grâce à sa reférence
        self.dessin.delete(self.trace[0])
        if self.parametre.chk.get():  # Vérification de la case à cocher

            # Méthode non recommandée (obtention directement de la valeur
            # du rayon du rayon à l'intérieur de la classe parametre)
            "self.trace[0] = self.dessin.traceCercle(rayon=\
                                                     self.parametre.rayon)"

            # Méthode recommandée (utilise une méthode de la classe
            # afin de définir le rayon)
            rayon = self.parametre.valeurs()
            self.trace[0] = self.dessin.traceCercle(rayon=rayon)


############# Création des Fonctions #############


###############################
#### Programme principal : ####
###############################


if __name__ == '__main__':
    Root().mainloop()
