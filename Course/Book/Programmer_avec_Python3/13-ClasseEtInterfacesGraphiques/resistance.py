#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""PROGRAMME ILLUSTRANT LES CLASSES EN UTILISANT TKINTER"""
"EXERCICE 13.1 À 13.5"

###########################################
#### Importation fonction et modules : ####
###########################################


from tkinter import *
from math import log10


###############################################################################
#### Gestion d'évènements : définition de différentes Fonctions/Classes : #####
###############################################################################


############# Création des Classes #############


class Application(object):
    """Regroupe l'interface graphique du programme"""
    def __init__(self, echelle=1):
        """Construction de l'interface"""
        self.echelle = echelle  # Modification de l'échelle de l'interface
        self.root = Tk()
        self.root.title("Code des couleurs")
        self.dessineResistance()
        Label(self.root, text="Entrez la valeur de la résistance, en ohms :"
              ).grid(row=2, column=1, columnspan=3)
        Button(self.root, text='Montrer', command=self.changeCouleurs
               ).grid(row=3, column=1)
        Button(self.root, text='Quitter', command=self.root.quit
               ).grid(row=3, column=3)
        self.entree = Entry(self.root, width=14)
        self.entree.grid(row=3, column=2)
        # Création d'un raccourci pour finaliser le calcul
        self.entree.bind("<Return>", self.changeCouleurs)
        # Code des couleurs pour les valeurs de zéro à neuf :
        self.cc = ['black', 'brown', 'red', 'orange', 'yellow',
                   'green', 'blue', 'purple', 'grey', 'white']
        self.root.mainloop()

    def dessineResistance(self):
        """Canevas avec un modèle de résistance à trois lignes colorées"""
        #
        # self.can = Canvas(self.root, width=250, height=100, bg='ivory')
        """Modification de la couleur de fond"""
        self.can = Canvas(self.root, width=250*self.echelle,
                          height=100*self.echelle, bg='light blue')
        self.can.grid(row=1, column=1, columnspan=3, pady=5, padx=5)
        #
        # self.can.create_line(10, 50, 240, 50, width=5)  # fils
        """Modification de l'épaisseur de la ligne représentant le fil"""
        self.can.create_line(10*self.echelle, 50*self.echelle,
                             240*self.echelle, 50*self.echelle, width=2)
        #
        # self.can.create_rectangle(65, 30, 185, 70, fill='light grey',
        #                           width=2)
        """Modification de la couleur de la resistance"""
        self.can.create_rectangle(65*self.echelle, 30*self.echelle,
                                  185*self.echelle, 70*self.echelle,
                                  fill='beige', width=2)
        # Dessin des trois lignes colorées (noires au départ) :
        self.ligne = []  # on mémorisera les trois lignes dans 1 liste
        for x in range(85*self.echelle, 150*self.echelle, 24*self.echelle):
            #
            # self.ligne.append(self.can.create_rectangle(x, 30, x+12, 70,
            #                   fill='black', width=0))
            """Modification de l'épaisseur des bandes"""
            self.ligne.append(self.can.create_rectangle(x, 30*self.echelle,
                              x+16, 70*self.echelle, fill='black', width=0))

    def changeCouleurs(self, event):  # Event pour évaluer avec <Enter>
        """Affichage des couleurs correspondant à la valeur entrée"""
        # Cette méthode renvoie une chaîne
        self.v1ch = self.entree.get()
        try:
            v = float(self.v1ch)  # Conversion en valeur numérique
        except:
            err = 1  # Erreur : entrée non numérique
        else:
            err = 0
        if err == 1 or v < 10 or v > 1e11:
            self.signaleErreur()  # Entrée incorrecte ou hors limites
        else:
            li = [0]*3  # liste des 3 codes à afficher
            logv = int(log10(v))  # partie entière du logarithme
            ordgr = 10**logv  # ordre de grandeur
            # extraction du premier chiffre significatif :
            li[0] = int(v/ordgr)  # partie entière
            decim = v/ordgr - li[0]  # partie décimale
            # extraction du second chiffre significatif :
            li[1] = int(decim*10 + .5)  # +.5 pour arrondir correctement
            # nombre de zéros à accoler aux 2 chiffres significatifs :
            li[2] = logv - 1
            # Coloration des 3 lignes :
            for n in range(3):
                self.can.itemconfigure(self.ligne[n],
                                       fill=self.cc[li[n]])

    def signaleErreur(self):
        """Associé à une erreur d'entrée dans le champs"""
        self.entree.configure(bg='red')
        # Temporisation sur l'appel de la fonction suivante
        self.root.after(1000, self.videEntree)

    def videEntree(self):
        """Nettoie le canvas"""
        # rétablir le fond blanc
        self.entree.configure(bg='white')
        # enlever les caractères présents
        self.entree.delete(0, len(self.v1ch))
        # Réinitialise le canvas
        for n in range(3):
            self.can.itemconfigure(self.ligne[n], fill='black')


############# Création des Fonctions #############


###############################
#### Programme principal : ####
###############################

# Exercices 13.1 à 13.5 : Modification du script
# Programme principal :
if __name__ == '__main__':
    f = Application(4)  # Lancement de l'application
