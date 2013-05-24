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



# Utilisation d'une boucle while pour parcourir une chaine à proscrire
nom = "Nadia Bois"
index = 0
while index < len(nom):
	print(nom[index] + '**', end = ' ')
	index += 1
print(end = '\n') # Seulement pour revenir à la ligne avant d'éffectuer le code suivant



# On préfèrera la forme suivante moins lourde autant en ligne qu'en rendement
nom = "Nadia Bois"
for car in nom:
	print(car + '&', end = ' ')
print(end = '\n') # Seulement pour revenir à la ligne avant d'éffectuer le code suivant



# Autre avantage : il a bon goût de conserver le typage des éléments
divers = ['lézard', 3, 3.22, [5, 'Jean']]
for element in divers:
	print(element, type(element))



# Utilisation de l'instruction <in> seule (sans <for>)
car = "e"
voyelles = "aeiouyAEIOUYàâÀÂéèêëÊËÉÈùÙîïÎÏ"
if car in voyelles:
	print(car, " est une voyelle.")



# Utilisation de l'instruction <in> pour les listes
n = 5
liste = [1, 2, 3, 4, 5, 6]
if n in liste:
	print(n, " est dans la liste")


#Evaluation des différentes erreurs possibles sur le slicing
mot = "Je suis un gros chat et donc j'aime les canards ?"
print(mot[-22:-112]) # Aucunes erreurs mais n'affiche rien
print(mot[22:111]) # Aucunes erreurs mais n'affiche rien
print([mot['e']]) # TypeError: string indices must be integers
print(mot[1111]) # IndexError: string index out of range
