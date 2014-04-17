#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""PROGRAMME UTILISANT LES CLASSES DES FICHIER OSCILLO ET CURSEURS"""
"COURS 13 : CRÉATION D'UN GESTIONNAIRE D'ÉVÈNEMENTS"

###########################################
#### Importation fonction et modules : ####
###########################################

from oscillo import *
from curseurs import *

###############################################################################
#### Gestion d'évènements : définition de différentes Fonctions/Classes : #####
###############################################################################


############# Création des Classes #############


class ShowVibra(Frame):
    """Evaluationgraphique d'un mouvement vibratoire harmonique"""
    def __init__(self, boss=None, nbrCourbe=3):
        Frame.__init__(self)     # Construction de la classe parente
        self.nbrCourbe = nbrCourbe
        self.couleur = ['dark green', 'red', 'purple', 'grey', 'blue',
                        'orange', 'brown', '#0AA187']
        self.trace = [0] * nbrCourbe     # liste du nombre de courbes
        self.controle = [0] * nbrCourbe  # liste du nombre de panneaux de contrôle
        # Instanciation du canevas contenant les courbes
        self.graph = OscilloGraphe(self, larg=400, haut=300)
        self.graph.configure(bg='light blue', bd=2, relief=SOLID)
        self.graph.pack(side=TOP, pady=10)
        # Instanciation des panneaux de contrôle
        for i in range(nbrCourbe):
            self.controle[i] = ChoixVibratoire(self, coul=self.couleur[i])
            self.controle[i].configure(relief=GROOVE, bd=2)
            self.controle[i].pack(padx=10, pady=10)
        # Mappage de l'évènement principal (déclencheur)
        # On vient détecter l'évènement à la fenêtre principale avec <master>
        self.master.bind('<Control-Z>', self.montreCourbes)
        self.master.title("Mouvement Vibratoires Harmoniques")
        self.pack()

    def montreCourbes(self, event):
        """Réaffichage des différents graphiques"""
        for i in range(self.nbrCourbe):
            self.graph.delete(self.trace[i])  # On efface l'ancien tracé
            if self.controle[i].chk.get():
                freq, phase, ampl = self.controle[i].valeurs()
                self.trace[i] = self.graph.traceCourbe(coul=self.couleur[i],
                                                       freq=freq,
                                                       phase=phase,
                                                       ampl=ampl)

############# Création des Fonctions #############


###############################
#### Programme principal : ####
###############################


# La fenêtre Tkinter est instancié directement à l'intérieur des Classes
if __name__ == '__main__':
    ShowVibra(nbrCourbe=5).mainloop()
