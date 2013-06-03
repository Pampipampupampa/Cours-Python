#! /usr/bin/env python
# -*- coding:Utf8 -*-


"PROGRAMME RECHERCHANT L'INDICE DU CARACTÈRE RECHERCHÉ ET COMPTANT LE NOMBRE D'OCCURENCES"
"EXERCICE 10.3 et 10.4 et 10.5"

################################################################
############# Importation fonction et modules : ################
################################################################




###################################################################################################
############# Gestion d'évènements : définition de différentes fonctions utiliées  : ##############
###################################################################################################



def trouve(chaine, caractere, debut = 0): # De base on recherche depuis le premier caractère
	"Recherche l'indice correspondant au caractère recherché"
	erreur = "Impossible de trouver le caractère dans la chaine"
	while debut < len(chaine):
		if chaine[debut] == caractere:
			return debut # La fonction a trouvé le caractère et renvoi son indice
		debut += 1
	return erreur # La fonction n'a rien trouvé



def compte(chaine, caractere, debut = 0):
	"Recherche et compte le nombre d'occurence d'un caractère dans une chaine"
	compteur = 0
	while debut < len(chaine):
		if chaine[debut] == caractere:
			compteur += 1
		debut += 1
	return compteur


######################################################
############## Programme principal : #################
######################################################



# Bout de code utile pour faire des test de fonctions. 
# Le code à l'intérieur du if ne sera exécuté que seulement si on appelle l'élément (classe, fonction, ...) depuis le fichier contenant le module
# Ainsi si on importe ce module depuis un autre fichier ce qui se trouve dessous ne sera pas exécuté
if __name__ == '__main__': 
	print(trouve("La souris verte ?", 'z'))
	print(trouve("La souris verte ?", 'e'))
	print(trouve("La souris verte ?", 'e', 13))
	print(compte("La souris verterr ?", 'r', 1))


