#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""PROGRAMME AUTOUR DE L'UTILISATION DES CLASSES"""
"EXERCICE 11.1"

###########################################
#### Importation fonction et modules : ####
###########################################


from math import sqrt


###############################################################################
#### Gestion d'évènements : définition de différentes Fonctions/Classes : #####
###############################################################################


############# Création des Classes #############


class Point(object):
    """Définition d'un point géométrique"""


############# Création des Fonctions #############


def distance(deb, fin):
    distance = sqrt((abs(fin.x) - abs(deb.x))**2 +
                    (abs(fin.y) - abs(deb.y))**2)
    return distance


###############################
#### Programme principal : ####
###############################


# Exercice 11.1 : Calcul de distance à l'aide de classes
debut = Point()
fin = Point()
debut.x, debut.y = 1, 1
fin.x, fin.y = 3, 3
print(distance(debut, fin))
