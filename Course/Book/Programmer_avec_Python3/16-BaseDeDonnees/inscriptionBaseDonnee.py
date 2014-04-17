#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""PERMET D'ENREGISTRER UN ENSEMBLE D'ÉLÉMENT DANS UNE BASE DE DONNÉES"""
"EXERCICE 16.1"

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

connex = sqlite3.connect("BaseDonnees/musiqueClass.sq3")
cur = connex.cursor()

# Création des différentes tables avec vérification de leur existence
# en amont grâce à l'instruction <try>
try:
    req = "CREATE TABLE compositeurs (compositeur TEXT, anneeNaissance\
                                       INTEGER, anneeMort INTEGER)"
    cur.execute(req)
    req = "CREATE TABLE oeuvres (compositeur TEXT, titre TEXT, duree INTEGER,\
                                interprete TEXT)"
    cur.execute(req)
except:
    pass  # Les tables existent déja

# Enregistrement de la table <compositeurs>
print("Début de l'enregistrement des compositeurs : ")
while 1:
    nom = input("Veuillez rentrer le nom du compositeur: ")
    if nom == "":
        break  # Champs vide permettant de finir la saisie
    naissance = input("Année de naissance : ")
    mort = input("Année de mort : ")
    req = "INSERT INTO compositeurs (compositeur, anneeNaissance, anneeMort) \
           VALUES (?, ?, ?)"
    cur.execute(req, (nom, naissance, mort))

# Vérification des éléments
print("Ensemble des éléments de la table compositeurs: ")
cur.execute("SELECT * FROM compositeurs")
for elem in cur:
    print(elem)

# Enregistrement de la table <oeuvre>
print("Début de l'enregistrement des oeuvres : ")
while 1:
    nom = input("Renseignez l'artiste : ")
    if nom == "":
        break
    titre = input("Renseignez le nom du morceaux : ")
    duree = input("Renseignez la durée : ")
    interprete = input("Renseignez l'interprête : '")
    req = "INSERT INTO oeuvres (compositeur, titre, duree, interprete) \
        VALUES (?, ?, ?, ?)"
    cur.execute(req, (nom, titre, duree, interprete))

# Vérification des éléments
print("Ensemble des éléments de la table oeuvres: ")
cur.execute("SELECT * FROM oeuvres")
for elem in cur:
    print(elem)

connex.commit()
connex.close()
