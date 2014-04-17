#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""MODULES <SOCKET> coté serveur"""
"SITE DU ZÉRO"

#########################################
### Importation fonction et modules : ###
#########################################


import socket
import select


############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


# ----- Création des Classes ----- #


##### CLASSE PRINCIPALE #####


#############################
### Programme principal : ###
#############################

# # Serveur minimaliste
# hote = ''
# port = 12800  # Port d'écoute du serveur

# # Construction du serveur
# connexionPrincipale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connexionPrincipale.bind((hote, port))
# connexionPrincipale.listen(5)  # Nombre max de demandes avant acceptation
# print("Le serveur écoute à présent sur le port {}".format(port))

# # La méthode accept renvoie un tuple
# connexionAvecClient, infoConnexion = connexionPrincipale.accept()

# # Les informations doivent être envoyés en binaire
# msgRecu = b""
# while msgRecu != b"fin":
#     msgRecu = connexionAvecClient.recv(1024)
#     # L'instruction ci-dessous peut lever une exception si le message
#     # Réceptionné comporte des accents
#     print(msgRecu.decode())
#     connexionAvecClient.send(b"5 / 5")

# print("Fermeture de la connexion")
# connexionAvecClient.close()
# connexionPrincipale.close()


# Serveur standard
hote = ''
port = 12800

# Construction du serveur
connexionPrincipale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connexionPrincipale.bind((hote, port))
connexionPrincipale.listen(5)
print("Le serveur écoute à présent sur le port {}".format(port))

serveurLance = True
clientsConnectes = []  # Liste des clients connectés
while serveurLance:
    # On va vérifier que de nouveaux clients ne demandent pas à se connecter
    # Pour cela, on écoute la connexionPrincipale en lecture
    # On attend maximum 50ms
    connexionsDemandees, wlist, xlist = select.select([connexionPrincipale],
                                                      [], [], 0.05)
    # Reception des nouveaux clients et ajout à la liste
    for connexion in connexionsDemandees:
        connexionAvecClient, infos_connexion = connexion.accept()
        # On ajoute le socket connecté à la liste des clients
        clientsConnectes.append(connexionAvecClient)

    # Maintenant, on écoute la liste des clients connectés
    # Les clients renvoyés par select sont ceux devant être lus (recv)
    # On attend là encore 50ms maximum
    # On enferme l'appel à select.select dans un bloc try
    # En effet, si la liste de clients connectés est vide, une exception
    # Peut être levée
    clientAlire = []
    try:
        clientAlire, wlist, xlist = select.select(clientsConnectes,
                                                  [], [], 0.05)
    except select.error:
        pass
    else:
        # On parcourt la liste des clients à lire
        for client in clientAlire:
            # Client est de type socket
            msgRecu = client.recv(1024)
            # Peut planter si le message contient des caractères spéciaux
            msgRecu = msgRecu.decode()
            print("Reçu {}".format(msgRecu))
            client.send(b"5 / 5")
            if msgRecu == "fin":
                serveurLance = False

print("Fermeture des connexions")
for client in clientsConnectes:
    client.close()

connexionPrincipale.close()
