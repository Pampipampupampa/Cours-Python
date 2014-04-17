#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""ENSEMBLE DE COURS SUR LE CHAPITRE : CLASSES, OBJETS, ATTRIBUTS"""
"COURS 11"

###########################################
#### Importation fonction et modules : ####
###########################################


###############################################################################
#### Gestion d'évènements : définition de différentes Fonctions/Classes : #####
###############################################################################


############# Création des Classes #############


# On utilisera toujours une majuscule pour définir une classe par convention
class Point(object):
    """Définition d'un point géométrique"""


class Rectangle(object):
    """Définition d'une classe de rectancles"""


############# Création des Fonctions #############


def trouveCentre(box):
    p = Point()
    p.x = box.coin.x + box.largeur/2.0
    p.y = box.coin.y + box.hauteur/2.0
    return p


###############################
#### Programme principal : ####
###############################


# Ici on assigne à la varaible p9 la classe Point
p9 = Point()
# On affiche son type, son emplacement dans la mémoire sous forme
# Hexadécimale, et son lieu de création ici main.
# Enfin on ajoute l'affichage de la docstring de la classe
print(p9, p9.__doc__)


# On peut accéder à un élément de la classe et à sa contenance directement
p9.x = 3.0
p9.y = 4.0
print(p9.x)


# Similitude et Unicité :
p1 = Point()
p2 = Point()
p1.x = 1
p2.y = 3
p1.x = 1
p2.y = 3
# Le fait d'appliquer les même paramètres et la même classe à une variable
# ne rend pas ces 2 variable identiques (comme les listes)
print(p1 == p2, p1, p2)  # Resultat = False car occupation mémoire différente
# Attention aux fausses ressemblances


# Si on veut que les 2 éléménts référence le même objet et donc au même espace
# mémoire il faut se servir de l'égalité et ainsi former un alias
p1 = p2  # création d'un alias
print(p1 == p2, p1, p2)  # Résultat = True et même occupation en mémoire


# Objets composés d'objets :
boite = Rectangle()
boite.largeur = 50.0
boite.hauteur = 35.0
boite.coin = Point()
boite.coin.x = 12.0
boite.coin.y = 27.0
# Utilisation de fonction pour transmettre une instance comme valeur de retour
centre = trouveCentre(boite)
print(centre.x, centre.y)
