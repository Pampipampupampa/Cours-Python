#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""PROGRAMMES UTILISANT L'INSTRUCTION IN ET FOR ... IN ..."""
"EXERCICE 10.9 ET 10.10 ET 10.11 ET 10.12 ET 10.13 ET 10.18 ET 10.19"

###########################################
#### Importation fonction et modules : ####
###########################################


###############################################################################
#### Gestion d'évènements : définition de différentes fonctions utiliées : ####
###############################################################################

def estUnChiffre(car):
	"""Vérifie chaques caractères d'une chaine et renvoi vrai si c'est un chiffre"""
	if car in '123456789':
		return 'true'
	else:
		return 'false'


def estUneMaj(car):
	"""Vérifie chaques caractères d'une chaine et renvoi vrai si c'est une majuscule"""
	if car in 'AZERTYUIOPQSDFGHJKLMWXCVBNÉÈÇÀÙÂÄÎÏÔÖÛÜËÊ':
		return 'true'
	else:
		return 'false'


def versListe(car):
	"""Création d'une liste des mots d'une phrase"""
	li, mot = [], ""
	for caractere in car:  # Parcourt de la phrase et ajout des mot à la liste  <li>
		if caractere == " ":
			li.append(mot)
			mot = ""
		else:
			mot = mot + caractere
	# Vérifie que le dernier mot est pris en compte (si vide mot est faux)
	if mot:
		li.append(mot)
	return li


def extractionMotMaj(car):
	"""Création d'une liste contenant tout les mot qui commencent par une majuscule"""
	liste, mot = [], ""
	for caractere in car:
		if caractere == " ":
			if estUneMaj(mot[0]):
				liste.append(mot)
			mot = ""
		else:
			mot = mot + caractere
	if mot and estUneMaj(mot[0]):
		liste.append(mot)
	return liste


def compteMaj(car):
	"""Vérifie chaques caractères d'une chaine et compte les majuscules"""
	compteur = 0
	for caractere in car:
		if estUneMaj(caractere) == 'true':
			compteur += 1
	return compteur

###############################
#### Programme principal : ####
###############################


# Exercice 10.9
if __name__ == '__main__':
	chaine1 = "Bonjour les 3 chats du village, je me nomme Bambi 1er ; roi des 23 forêts sombres"
	print("La chaine testée est : " + chaine1)
	for car in chaine1:
		print(car, estUnChiffre(car), end=' : ')


# Exercice 10.10 (équivalent 10.18)
if __name__ == '__main__':
	print("La chaine testée est : " + chaine1)
	for car in chaine1:
		print(car, estUneMaj(car), end=' : ')


# Exercice 10.11
if __name__ == '__main__':
	chaine2 = "Je suis le grand roi Agamendon"
	futurListe = versListe(chaine2)
	for mot in futurListe:  # Affiche chaque élément de la liste avec séparation
		print(mot + "--", end=' ')
	for mot in futurListe[1]:  # Affiche chaque élément d'un élément de la liste (ici le 2nd)
		print(mot + "--", end=' ')


# Exercice 10.12
if __name__ == '__main__':
	futurListe = extractionMotMaj("Bonjour les enfants de Dieu Martin Pêcheur Àéris")
	for mot in futurListe:  # Affiche chaque élément de la liste avec séparation
		print(mot + "--", end=' ')


# Exercice 10.13 (équivalent 10.19)
if __name__ == '__main__':
	print("Il y a dans ce texte : " + str(compteMaj("Bon je suis dans les \
	      abysses de ce monde")) + " majuscules")
