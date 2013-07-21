#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""GESTION DE LA BASE DE DONNÉES DE L'EXERCICE 16.1"""
"COURS 16"

#########################################
### Importation fonction et modules : ###
#########################################


import sqlite3


############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


# ----- Création des Classes ----- #


##### CLASSE PRINCIPALE #####


# ----- Création des Fonctions ----- #


#############################
### Programme principal : ###
#############################

baseDonnee = sqlite3.connect("BaseDonnees/musiqueClass.sq3")
cur = baseDonnee.cursor()
while 1:
    print("Entrer une requête SQL ou <Enter> pour quitter")
    req = input()
    if req == "":
        break
    try:
        cur.execute(req)
    except:
        print("--- Erreur : Requête invalide ---")
    else:
        for elem in cur:
            print(elem)
    print()

choix = input("<O> ou <o> pour confirmer l'enregistrement")
if choix[0] == "O" or choix[0] == "o":  # Test de la première lettre
    cur.commit()
else:
    baseDonnee.close()
