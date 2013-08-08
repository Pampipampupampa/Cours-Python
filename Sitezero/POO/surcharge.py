#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""SURCHARGE D'OBJET"""
"CLASSES SDZ"

#########################################
### Importation fonction et modules : ###
#########################################


############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


# ----- Création des Classes ----- #


class Duree:
    """Classe contenant des durées sous la forme d'un nombre de minutes
    et de secondes"""

    def __init__(self, min=0, sec=0):
        """Constructeur de la classe"""
        self.min = min  # Nombre de minutes
        self.sec = sec  # Nombre de secondes

    def __str__(self):
        """Affichage un peu plus joli de nos objets"""
        return "{0:02}:{1:02}".format(self.min, self.sec)

    def __add__(self, objet_a_ajouter):
        """L'objet à ajouter est un entier, le nombre de secondes
        On surcharge (modifie l'action du <+>) afin d'obtenir une durée
        cohérente"""
        nouvelle_duree = Duree()
        # On va copier self dans l'objet créé pour avoir la même durée
        nouvelle_duree.min = self.min
        nouvelle_duree.sec = self.sec
        # On ajoute la durée
        nouvelle_duree.sec += objet_a_ajouter
        # Si le nombre de secondes >= 60
        if nouvelle_duree.sec >= 60:
            nouvelle_duree.min += nouvelle_duree.sec // 60
            nouvelle_duree.sec = nouvelle_duree.sec % 60
        # On renvoie la nouvelle durée
        return nouvelle_duree

    def __iadd__(self, objet_a_ajouter):
        """ Surcharge de <+=>
        L'objet à ajouter est un entier, le nombre de secondes"""
        # On travaille directement sur self cette fois
        # On ajoute la durée
        self.sec += objet_a_ajouter
        # Si le nombre de secondes >= 60
        if self.sec >= 60:
            self.min += self.sec // 60
            self.sec = self.sec % 60
        # On renvoie self
        return self

    def __eq__(self, autre_duree):
        """Surcharge de <==>
        Test si self et autre_duree sont égales"""
        return self.sec == autre_duree.sec and self.min == autre_duree.min

    def __gt__(self, autre_duree):
        """Surcharge de >
        Test si self > autre_duree"""
        # On calcule le nombre de secondes de self et autre_duree
        nb_sec1 = self.sec + self.min * 60
        nb_sec2 = autre_duree.sec + autre_duree.min * 60
        return nb_sec1 > nb_sec2


##### CLASSE PRINCIPALE #####


# ----- Création des Fonctions ----- #


def __radd__(self, objet_a_ajouter):
        """Cette méthode est appelée si on écrit 4 + objet et que
        le premier objet (4 dans cet exemple) ne sait pas comment ajouter
        le second. On se contente de rediriger sur __add__ puisque,
        ici, cela revient au même : l'opération doit avoir le même résultat,
        posée dans un sens ou dans l'autre"""
        return self + objet_a_ajouter


#############################
### Programme principal : ###
#############################


if __name__ == '__main__':
    d1 = Duree(12, 18)
    print(d1)
    # d1 = d1 + 54 ou d1 = d1.__add__(54) : cela revient au même (surcharge)
    print(d1 + 54)  # Attention 54 + d1 ne fonctionnera pas (mauvais attribut)


"""
Sachez que sur le même modèle, il existe les méthodes :
__add__ : surcharge de l'opérateur + ;
__sub__ : surcharge de l'opérateur - ;
__mul__ : surcharge de l'opérateur * ;
__truediv__ : surcharge de l'opérateur / ;
__floordiv__ : surcharge de l'opérateur // (division entière) ;
__mod__ : surcharge de l'opérateur % (modulo) ;
__pow__ : surcharge de l'opérateur ** (puissance) ;
…
"""
