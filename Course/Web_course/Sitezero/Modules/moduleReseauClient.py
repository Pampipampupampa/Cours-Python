#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""MODULES <SOCKET> coté client"""
"SITE DU ZÉRO"

#########################################
### Importation fonction et modules : ###
#########################################


import socket


############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


# ----- Création des Classes ----- #


##### CLASSE PRINCIPALE #####


#############################
### Programme principal : ###
#############################


hote = "localhost"
port = 12800

# Construction du client
connexionServeur = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexionServeur.connect((hote, port))
print("Connexion établie avec le serveur sur le port {}".format(port))

msgAenvoyer = b""
while msgAenvoyer != b"fin":
    msgAenvoyer = input("> ")
    # Peut planter si vous tapez des caractères spéciaux
    msgAenvoyer = msgAenvoyer.encode()
    # On envoie le message
    connexionServeur.send(msgAenvoyer)
    msgrecu = connexionServeur.recv(1024)
    print(msgrecu.decode())  # Là encore, peut planter s'il y a des accents

print("Fermeture de la connexion")
connexionServeur.close()
