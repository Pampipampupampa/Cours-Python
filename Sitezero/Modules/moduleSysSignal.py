#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""MODULES <SYS> ET <SIGNAL>"""
"SITE DU ZÉRO"

#########################################
### Importation fonction et modules : ###
#########################################


import sys
import signal

############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


# ----- Création des Classes ----- #


##### CLASSE PRINCIPALE #####


# ----- Création des Fonctions ----- #


def fermeProgramme(signal, frame):
    """Fonction appelée quand vient l'heure de fermer notre programme"""
    print("C'est l'heure de la fermeture !")
    sys.exit(0)


#############################
### Programme principal : ###
#############################


# Utilisation d'arguments et de paramètres
# Long et cour
"""

import getopt

try:
    # On récupère sous un tuple les informations
    opts, args = getopt.getopt(sys.argv[1:], "ho:v", ["help", "output="])
except getopt.GetoptError as err:
    # Affiche l'aide et quitte le programme
    print(err)  # Va afficher l'erreur en anglais
    usage()  # Fonction à écrire rappelant la syntaxe de la commande
    sys.exit(2)

output = None
verbose = False
for o, a in opts:
    if o == "-v":
        # On place l'option 'verbose' à True
        verbose = True
    elif o in ("-h", "--help"):
        # On affiche l'aide
        usage()
        sys.exit()
    elif o in ("-o", "--output"):
        output = a
    else:
        print("Option {} inconnue".format(o))
        sys.exit(2)

"""


# Utiliation de sys.argv afin modifier l'ouverture du script avec des
# paramètres qui influeront sur le script
if len(sys.argv) < 2:  # On accepte un nombre max de paramètres
    print("Précisez une action en paramètre")
    sys.exit(1)

action = sys.argv[1]

if action == "start":
    print("On démarre l'opération")
elif action == "stop":
    print("On arrête l'opération")
elif action == "restart":
    print("On redémarre l'opération")
elif action == "status":
    print("On affiche l'état (démarré ou arrêté ?) de l'opération")
else:
    print("Je ne connais pas cette action")


# Utilisation de la fonction signal
signal.signal(signal.SIGINT, fermeProgramme)
print("Le programme va boucler...")
while True:
    continue
