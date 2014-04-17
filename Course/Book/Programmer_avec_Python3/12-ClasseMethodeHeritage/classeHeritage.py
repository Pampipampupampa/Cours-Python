#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""PROGRAMME AUTOUR DE L'UTILISATION DES CLASSES"""
"EXERCICE 12.5 ET 12.6 ET 12.7 ET 12.8"

###########################################
#### Importation fonction et modules : ####
###########################################

from math import pi
from random import randrange
from premiereClasses import CompteBancaire

###############################################################################
#### Gestion d'évènements : définition de différentes Fonctions/Classes : #####
###############################################################################


############# Création des Classes #############


class Cercle(object):
    """Définition de cercle à partir du rayon"""
    def __init__(self, rayon=3):
        self.rayon = rayon

    def surface(self):
        """Renvoie l'air du cercle"""
        return pi * self.rayon**2


class Cylindre(Cercle):
    """Définition de cylindres héritants de la classe <Cercle>"""
    def __init__(self, rayon, hauteur):
        Cercle.__init__(self, rayon)
        self.hauteur = hauteur

    def volume(self):
        return self.surface() * self.hauteur


class Cone(Cylindre):
    """Définition de cônes héritant de la classe cylindre"""
    def __init__(self, rayon, hauteur):
        Cylindre.__init__(self, rayon, hauteur)

    def volume(self):
        return Cylindre.volume(self) / 3  # Polymorphisme


class JeuDeCartes(object):
    """Simulation d'un jeu de 52 cartes"""
    # Valeur des cartes
    valeur = [2, 3, 4, 5, 6, 7, 8, 9, 10, "valet", "dame", "roi", "as"]
    # Couleur de la carte
    couleur = ["Pique", "Trèfle", "Carreau", "Coeur"]

    def __init__(self):
        """Construction du jeu de carte"""
        self.carte = []  # Liste vide à remplir
        for coul in range(4):
            for val in range(13):
                self.carte.append((val, coul))

    def nomCarte(self, c):
        """Renvoie le nom de la carte (<c> doit être un tuple !!!)"""
        print("{} de {}"
              .format(self.valeur[c[0]], self.couleur[c[1]]))

    def battre(self):
        """Mélange les cartes"""
        longueur = len(self.carte)
        for i in range(longueur):
            al1, al2 = randrange(longueur), randrange(longueur)
            self.carte[al1], self.carte[al2] = self.carte[al2], self.carte[al1]

    def tirer(self):
        """Retire une carte du jeu"""
        nombre = len(self.carte)
        if nombre > 0:
            carte = self.carte[0]
            del(self.carte[0])
            return carte
        else:
            return None


class CompteEpargne(CompteBancaire):
    """Création de compte bancaire avec interêts"""
    def __init__(self, client, solde, taux=0.3):
        CompteBancaire.__init__(self, client, solde)
        self.taux = taux

    def modifierTaux(self, taux):
        """Modification du taux des intérêts"""
        self.taux = taux

    def capitalisation(self, mois):
        """Ajout des intérêts au compte épargne"""
        for i in range(mois):
            self.solde = self.solde + self.solde*self.taux/100
        return "Capitalisation sur {} mois au taux de {} %"\
               .format(mois, self.taux)


############# Création des Fonctions #############


###############################
#### Programme principal : ####
###############################


# Exercice 12.5 et 12.6: Classes d'éléments circulaires
cyl = Cylindre(5, 7)
print(cyl.surface())  # Surface cylindre
print(cyl.volume())   # Volume cylindre
co = Cone(5, 7)
print(co.volume())    # Volume cone


# Exercice 12.7 : Classe de jeu de cartes (lire, mélanger, retirer)
if __name__ == '__main__':
    jeux = JeuDeCartes()
    jeux.nomCarte((1, 2))  # Attention la méthode demande un tuple
    for n in range(53):
        c = jeux.tirer()
        if c is None:
            print('Plus de cartes')
        else:
            jeux.nomCarte(c)


# Exercice 12.8 : Simulation d'un jeu de bataille
jeuA = JeuDeCartes()
jeuB = JeuDeCartes()
jeuA.battre()
jeuB.battre()
comptA = 0
comptB = 0
for carte in range(53):
    cA = jeuA.tirer()
    cB = jeuB.tirer()
    if cA is None or cB is None:
        print("Score :\n" +
              "Joueur A = {} -------- Joueur B = {} ".format(comptA, comptB))
    elif cA[0] > cB[0]:
        comptA += 1
    elif cB[0] > cA[0]:
        comptB += 1

# Exercice 12.9 : Importation de module et héritage
# On importe la classe <Comptebancaire>
# comme un module (fichier <premiereClasses>)
# On ajoute ensuite une classe enfant
compte = CompteEpargne("Jeremy", 950,)
compte.capitalisation(12)
compte.modifierTaux(.5)
compte.capitalisation(12)
compte.affiche()
