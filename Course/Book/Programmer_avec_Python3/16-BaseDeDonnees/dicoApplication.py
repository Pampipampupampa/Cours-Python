#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""REGROUPE L'ENSEMBLE DES VARIABLES PSEUDO GLOBALES"""
"COURS 16"

#########################################
### Importation fonction et modules : ###
#########################################


############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


# ----- Création des Classes ----- #


##### CLASSE PRINCIPALE #####


class Glob(object):
    """Espace de noms pour les variables et fonctions pseudo-globales"""
    dbName = "discotheque"
    user = "pampi"
    passwd = "Smoothcriminal0"
    host = "127.0.0.1"  # Adresse du serveur
    port = 5432
    # Structure de la base de données. Dictionnaire des tables et champs
    dicoT = {"compositeurs": [('id_comp', "k", "clé primaire"),
                              ('nom', 25, "nom"),
                              ('prenom', 25, "prenom"),
                              ('anneeNaissance', "i", "année de naissance"),
                              ('anneeMort', "i", "année de mort")],
             "oeuvres": [('id_oeuv', "k", "clé primaire"),
                         ('id_comp', "i", "clé compositeur"),
                         ('titre', 50, "titre de l'oeuvre"),
                         ('duree', "i", "durée (en minutes)"),
                         ('interprete', 30, "interprète principal")]}


# ----- Création des Fonctions ----- #


#############################
### Programme principal : ###
#############################
