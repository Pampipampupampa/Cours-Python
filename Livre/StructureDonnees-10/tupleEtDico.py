#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""PROGRAMMES SUR LES BASES DE L'UTILISATION DES DICTIONNAIRES ET DES TUPLES"""
"EXERCICE 10.45 ET 10.46"

###########################################
#### Importation fonction et modules : ####
###########################################


###############################################################################
#### Gestion d'évènements : définition de différentes fonctions utiliées : ####
###############################################################################


def inverse(annuaire):
    """Construit un nouveau dictionnaire en inversant clé \
       et valeur de l'entrée"""
    dicoInverse = {}
    for cle in annuaire:
        element = annuaire[cle]
        dicoInverse[element] = cle
    return dicoInverse


def consultation():
    """Permet de parcourir le dictionnaire"""
    while 1:
        nom = input("Veuillez définir le nom de la personne : ")
        if nom == "":
            break
        if nom in annuaire:
            element = annuaire[nom]
            age, taille = element[0], element[1]
            print("Nom : {} ---- Âge : {} ans ---- Taille : {2:2f} mètres".
                  format(nom, age, taille))
        else:
            print("*** Ce nom n'est pas présent !!! ***")


def remplissage():
    """Permet d'ajouter une entrée au dictionnaire"""
    while 1:
        nom = input("Veuillez définir le nom de la personne : ")
        if nom == "":
            break
        age = input("Veuillez définir l'age de {} : ".format(nom))
        taille = input("Veuillez définir la taille de {} (en m)(mettre un <.> pour la virgule) : ".format(nom))
        flag = input("{} ayant {} ans, et mesurant {} m;\
                     C'est bon? (oui ou O ou o confirme) :".
                     format(nom, age, taille))
        if flag == "oui" or flag == "oui" or flag == "o" or flag == "O":
            annuaire[nom] = (int(age), float(taille))


###############################
#### Programme principal : ####
###############################


# Exercice 10.45 : Création d'une mini base de données
annuaire = {}
while 1:
    choix = input("Action voulue : (R)emplir ou (C)onsulter ou (Q)uitter : ")
    if choix.upper() == "Q":  # Passe en majuscule afin d'accepter le "q"
        break
    if choix.upper() == "C":
        consultation()
    elif choix.upper() == "R":
        remplissage()


# Exercice 10.46 : Inverse valeurs et clés dans un dictionnaire
dictionnaire = {"pommes": 430, "bananes": 312, "oranges": 274, "poires": 137}
print(dictionnaire)
print(inverse(dictionnaire))
