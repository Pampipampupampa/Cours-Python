#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""ENSEMBLE DE COURS SUR LE CHAPITRE : CLASSES, METHODES, HERITAGE"""
"COURS 12"

###########################################
#### Importation fonction et modules : ####
###########################################


import formes


###############################################################################
#### Gestion d'évènements : définition de différentes Fonctions/Classes : #####
###############################################################################


############# Création des Classes #############


class TimeBase(object):
    """Définition d'objets temporels"""


class TimeMethode(object):
    """Définition d'objets temporels"""
    # On recommande de toujours utilisé <self> comme variable d'instance
    def afficheHeure(self):
        """Affiche la variable d'entrée en format heure:minute:seconde"""
        print("{0} : {1} : {2}"
              .format(self.heure, self.minute, self.seconde))


class Time(object):
    """Définition d'objets temporels"""
    def __init__(self, hh=12, mm=0, ss=0):
        self.heure = hh
        self.minute = mm
        self.seconde = ss

    # On recommande de toujours utilisé <self> comme variable d'instance
    def afficheHeure(self):
        """Affiche la variable d'entrée en format heure:minute:seconde"""
        print("{0} : {1} : {2}"
              .format(self.heure, self.minute, self.seconde))


class Espaces(object):
    aa = 33

    def affiche(self):
        print(aa, Espaces.aa, self.aa)


# 1
class Mammifere(object):
    """Class mammifère"""
    carac1 = "Il allaite ses petits ;"


class Carnivore(Mammifere):
    """Classe héritant de la classe <Mammifere>"""
    carac2 = "Il mange de la viande ;"


class chien(Carnivore):
    """Classe héritant de la classe <Mammifere> et <Carnivore>"""
    carac3 = "Son cri est l'aboiement ;"


class Atome:
    """atomes simplifiés, choisis parmi les 10 premiers éléments du TP"""
    table = [None, ('hydrogène', 0), ('hélium', 2), ('lithium', 4),
             ('béryllium', 5), ('bore', 6), ('carbone', 6), ('azote', 7),
             ('oxygène', 8), ('fluor', 10), ('néon', 10)]

    def __init__(self, nat):
        "le n° atomique détermine le n. de protons, d'électrons et de neutrons"
        self.np, self.ne = nat, nat  # nat = numéro atomique
        self.nn = Atome.table[nat][1]

    def affiche(self):
        print()
        print("Nom de l'élément :", Atome.table[self.np][0])
        print("{0} protons, {1} électrons, {2} neutrons"
              .format(self.np, self.ne, self.nn))


class Ion(Atome):
    """les ions sont des atomes qui ont gagné ou perdu des électrons"""
    def __init__(self, nat, charge):
        "le n° atomique et la charge électrique déterminent l'ion"
        Atome.__init__(self, nat)   # On initialise avec la classe parente
        self.ne = self.ne - charge  # On initialise de nouveaux éléments
        self.charge = charge        # avec la classe enfant

    def affiche(self):
        Atome.affiche(self)
        print("Particule électrisée. Charge =", self.charge)

############# Création des Fonctions #############


def afficheHeure(temps):
    """Affiche la variable d'entrée en format heure:minute:seconde"""
    print("{0} : {1} : {2}".format(temps.heure, temps.minute, temps.seconde))


###############################
#### Programme principal : ####
###############################

# Objet = Attribut + Methode
instant = TimeBase()
instant.heure = 11
instant.minute = 34
instant.seconde = 25
print(afficheHeure(instant))

# <afficheHeure> étant utile, il serait bien vu de l'encapsuler dans
# la classe <Time> afin d'y avoir accès facilement et en continue
maintenant = TimeMethode()
maintenant.heure = 12
maintenant.minute = 22
maintenant.seconde = 55
print(maintenant.afficheHeure())


# On améliore encore la classe grâce à un constructeur
# On initialise la méthode et on évite ainsi des erreurs
start = Time()
print(start.afficheHeure())
# Grâce à ces paramètres d'initialisation on peut directement assigner
# des valeurs à la création
start = Time(11, 44, 33)
print(start.afficheHeure())


# Espace des noms et instances :
aa = 12
essai = Espaces()
essai.aa = 67
# On remarque donc bien que chaques variables n'interfèrent pas entre elles
essai.affiche()


# Héritage
# voir classes : # 1
geb = chien()
# On remarque donc bien que <geb> herite bien des attribut des classes parentes
# On utilise un procédé de dérivation pour réaliser celà
print(geb.carac1, geb.carac2, geb.carac3)


# Petit exercice sur les atomes
a1 = Atome(5)
a2 = Ion(3, 1)
a3 = Ion(8, -2)
a1.affiche()
a2.affiche()
a3.affiche()


# Importation et création de modules
# import formes
# ---> Importation du module créé et enregistré sous le nom de formes
f1 = formes.Rectangle(27, 12)
f2 = formes.Carre(13)
f1.mesures()
f2.mesures()
print(formes.Rectangle.__doc__)  # Affiche la documentation sur la classe
