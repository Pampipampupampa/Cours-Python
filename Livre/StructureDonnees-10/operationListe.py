#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""PROGRAMME RÉALISANT DES OPÉRATIONS SUR LES LISTES"""
"EXERCICE 10.36 ET 10.37 ET 10.38 ET 10.39 ET 10.40 ET 10.41 ET 10.42 ET 10.43 ET 10.44"

###########################################
#### Importation fonction et modules : ####
###########################################


from random import random, randrange


###############################################################################
#### Gestion d'évènements : définition de différentes fonctions utiliées : ####
###############################################################################


def alternanceListe(list1, list2):
	i = 1
	for elem in list1:
		list2[i:i] = [elem]  # Attention faut une liste !!!
		i += 2
	return list2

def alternanceListeCour(list1, list2):
	i, n = 1, 0
	while n > len(list1):
		list2[i:i] = [list1[n]]  # Attention faut une liste !!!
		i += 2
		n += 1
	return list2


def listeAleatoire(nombre):
	s = []
	for elem in range(nombre):
		s.append(random())
	return s


def imprimeListe(element):
	for elem in element:
		print(elem)


def verifAleatoire(test=1000, fraction=4):
	compteur = [0] * fraction
	nbrAleatoire = listeAleatoire(test)
	for nbr in nbrAleatoire:
			index = int(nbr * fraction)
			compteur[index] = compteur[index] + 1
	for compte in compteur:
		print(compte, end=' ')
	print()


def carteHazardeuse1():
	carte = [["trèfle", "carreau", "pique", "coeur"], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "valet", "dame", "roi", "as"]]
	val2 = carte[0][randrange(0, len(carte[0]))]
	val1 = carte[1][randrange(0, len(carte[1]))]
	print("{} de {}".format(val1, val2))


def carteHazardeuse2():
	carteListe = [["trèfle", "carreau", "pique", "coeur"], [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "valet", "dame", "roi", "as"]]
	carte = []
	for couleur in carteListe[0]:
		for num in carteListe[1]:
			carte.append("{} de {}".format(num, couleur))
	carte = carte[randrange(0, len(carte))]
	return carte


###############################
#### Programme principal : ####
###############################


# Exercice 10.36 : Addition alternée d'éléments de listes
if __name__ == '__main__':
	t1 = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	t2 = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
	print(alternanceListe(t1, t2))
	print(alternanceListeCour(t1, t2))


# Exercice 10.37 et 10.38 et 10.39 : Création d'une copie d'une liste
if __name__ == '__main__':
	# Exercie 10.38
	aa = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	bb = []
	for element in aa:
		bb.append(element)
	# Vérification de l'indépendance
	del aa[1]
	aa[0] = 3
	# Exercie 10.37
	print(bb, aa)
	aa = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	bb = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	i = 0
	for ele in aa:
		bb[i] = ele  # Ne demande pas forcement une liste
		i += 1
	del aa[1]
	aa[0] = 3
	print(bb, aa)
	# Exercie 10.39
	aa = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
	bb = []
	bb = aa[0:]
	del aa[1]
	aa[0] = 3
	print(bb, aa)


# Exercice 10.40 : Etablie la liste des nombres premiers
if __name__ == '__main__':
	liste = [1] * 1000
	# On débute la liste à partir de 2
	for elem in range(2, 1000):
		# Met à zéro les éléments suivant dans la liste
		# si c'est un multiple de <elem>
		for j in range(elem*2, 1000, elem):
			liste[j] = 0
	for elem in range(1, 1000):  # On enlève le 0
		if liste[elem]:
			print(elem, end=' ')  # Affiche le résultat


# Exercice 10.41 et 10.42 : Génère une liste de nombre aléatoire et les affiche en colonne
if __name__ == '__main__':
	print(listeAleatoire(3))
	print(imprimeListe(listeAleatoire(3)))


# Exercice 10.43 : Vérification de l'éfficacité de la fonction générant des nombres aléatoires
if __name__ == '__main__':
	verifAleatoire(10000, 10)


# Exercice 10.44 : Tire une carte au hazard dans un jeu de 52 cartes
if __name__ == '__main__':
	carteHazardeuse1()
	print(carteHazardeuse2())
