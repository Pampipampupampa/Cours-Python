#! /usr/bin/env python
# -*- coding:Utf8 -*-


"PROGRAMMES UTILISANT L'INSTRUCTION IN ET FOR ... IN ..."
"EXERCICE 10.9 ET 10.10 ET 10.11"

################################################################
############# Importation fonction et modules : ################
################################################################




###################################################################################################
############# Gestion d'évènements : définition de différentes fonctions utiliées  : ##############
###################################################################################################


def estUnChiffre(car):
	"""Vérifie chaques caractères d'une chaine et renvoi vrai si c'est un chiffre"""
	if car in '123456789':
		return 'true'
	else:
		return 'false'



######################################################
############## Programme principal : #################
######################################################


if __name__ == '__main__':
	chaine1 = "Bonjour les 3 chats du village, je me nomme Bambi 1er ; roi des 23 forêts sombres"
	print("La chaine testée est : " + chaine1)
	for car in chaine1:
		print(car, estUnChiffre(car), end = " : ")
