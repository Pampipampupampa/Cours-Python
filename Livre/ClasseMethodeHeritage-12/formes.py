
#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""MODULES DE FORMES GEOMETRIQUES"""

###########################################
#### Importation fonction et modules : ####
###########################################


###############################################################################
#### Gestion d'évènements : définition de différentes Fonctions/Classes : #####
###############################################################################


############# Création des Classes #############


class Rectangle(object):
    "Classe de rectangles"
    def __init__(self, longueur=0, largeur=0):
        self.L = longueur
        self.l = largeur
        self.nom = "rectangle"

    def perimetre(self):
        return "({0:d} + {1:d}) * 2 = {2:d}"\
               .format(self.L, self.l, (self.L + self.l)*2)

    def surface(self):
        return "{0:d} * {1:d} = {2:d}".format(self.L, self.l, self.L*self.l)

    def mesures(self):
        print("Un {0} de {1:d} sur {2:d}".format(self.nom, self.L, self.l))
        print("a une surface de {0}".format(self.surface()))
        print("et un périmètre de {0}\n".format(self.perimetre()))


class Carre(Rectangle):
    "Classe de carrés"
    def __init__(self, cote):
        Rectangle.__init__(self, cote, cote)
        self.nom = "carré"


############# Création des Fonctions #############


###############################
#### Programme principal : ####
###############################


if __name__ == "__main__":  # Non effectué lors de l'import
    r1 = Rectangle(15, 30)
    r1.mesures()
    c1 = Carre(13)
    c1.mesures()
