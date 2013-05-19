#! /usr/bin/env python
# -*- coding:Utf8 -*-


"ENSEMBLE DE COURS SUR LE CHAPITRE : APPROFONDIR LES STRUCTURES DE DONNEES (COURS 10)"
"COURS 10"

################################################################
############# Importation fonction et modules : ################
################################################################




###################################################################################################
############# Gestion d'évènements : définition de différentes fonctions utiliées  : ##############
###################################################################################################




######################################################
############## Programme principal : #################
######################################################



# Indiçage, extraction et longueur
nom = "Damien"
print(nom[1], nom[3], nom[5]) # Extraction à partir du début de la chaine
print(nom[-1], nom[-3], nom[-5]) # Extraction à partir de la fin de la chaine
print(len(nom)) # Affiche la longueur de la chaine
print(nom[0:4]) # Extraction des caractères 1 à 4 (inclusion du premier et exclusion du dernier = les indices se trouvent donc entres les caractères)
print(nom[0:2], nom[3:6])



# Concaténation et répétition
n = 'abc' + 'def' # Concaténation
m = 'zut ! ' * 4 # Répétition
print(n, m)