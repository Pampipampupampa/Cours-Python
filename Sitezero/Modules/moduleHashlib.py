#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""MODULES <HASHLIB> ET <GETPASS>"""
"SITE DU ZÉRO"

#########################################
### Importation fonction et modules : ###
#########################################


import hashlib
from getpass import getpass


############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


# ----- Création des Classes ----- #


##### CLASSE PRINCIPALE #####


#############################
### Programme principal : ###
#############################


motPass = b"azerty"
motPassChiffre = hashlib.sha1(motPass).hexdigest()

verrouille = True
while verrouille:
    entre = getpass("Tapez le mot de passe : ")  # azerty
    # On encode la saisie pour avoir un type bytes
    entre = entre.encode()

    entreChiffre = hashlib.sha1(entre).hexdigest()
    if entreChiffre == motPassChiffre:
        verrouille = False
    else:
        print("Mot de passe incorrect")

print("Mot de passe accepté...")
