#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""PROGRAMMES AUTOUR DE LA NOTION D'OBJET DES LISTES"""
"EXERCICE 10.27 ET 10.28 ET 10.29 ET 10.30 ET 10.31 ET 10.32 ET 10.33"
"EXERCICE 10.34 ET 10.35 NON RÉALISÉS"

###########################################
#### Importation fonction et modules : ####
###########################################


from math import sin, pi


###############################################################################
#### Gestion d'évènements : définition de différentes fonctions utiliées : ####
###############################################################################


def carreEtCube(deb=20, fin=40):
	"""Renvoi la liste des cubes et des carrés d'une intervalle"""
	carre = []
	cube = []
	while deb < fin:
		valCarre = deb**2
		carre.append(valCarre)
		valCube = deb**3
		cube.append(valCube)
		deb += 1
	return "La liste des carré est : " + str(carre) + "\nLa liste des cubes est : " + str(cube)


def sinusIntervalle(deb=0, fin=90):
	"""Renvoi la liste des sinus d'une intervalle par pas de 5"""
	liste = []
	while deb <= fin:
		ang = deb*2*pi/360
		sinus = sin(ang)
		print("Le sinus de " + str(deb) + "° est : " + str(sinus))
		liste.append(sinus)
		deb += 5
	return liste


def tableMulti(table=1, nombre=10):
	"""Renvoi n termes de la table de multiplication par m"""
	i = 1
	liste = []
	while i <= nombre:
		table = table * i
		liste.append(table)
		i += 1
	return liste


def tableMultiLivre(m, n):
	"""Renvoi n termes de la table de multiplication par m"""
	ch = ""
	for i in range(n):
		v = m * (i+1)
		# Formatage d'une variable à 4 caractères en forme décimale
		# ch = ch + "%4d" % (v)         = ancien formatage
		ch = ch + "{0:4d}".format(v)  # = nouveau formatage
	return ch


###############################
#### Programme principal : ####
###############################


# Exercice 10.27 : Renvoyer la liste des carrés et des cubes d'une intervalle
if __name__ == '__main__':
	print(carreEtCube(20, 40))


# Exercice 10.28 : Renvoi une liste des sinus de l'intervalle choisie
if __name__ == '__main__':
	print(sinusIntervalle(0, 90))


# Exercice 10.29 : Renvoyer la table de multiplication en liste ou chaine
if __name__ == '__main__':
	nombre = [2, 3, 5, 7, 9, 11, 13, 15, 17, 19]
	for n in nombre:
		print(tableMulti(n, 15))
	for n in nombre:
		print(tableMultiLivre(n, 15))


# Exercice 10.30 : Affiche le nombre de caractères de chaques éléments
if __name__ == '__main__':
	liste = ['Jean-Michel', 'Marc', 'Vanessa', 'Anne', 'Maximilien', 'Alexandre-Benoît', 'Louise']
	for n in liste:
		print("%s : %s caractères" % (n, len(n)))
	for n in liste:
		print(("{1} : {0} caractères").format(len(n), n))

# Exercice 10.31 : Trie une liste d'éléments et vire les doublons
if __name__ == '__main__':
	listeDeb = [9, 12, 44, 12, 9, 87, 87, 98, 0.98, 0.7, 0.98, 46]
	listFin = []
	for nb in listeDeb:
		# On ajoute l'élément à la liste finale seulement
		# si il n'y est pas déja, sinon on ajoute rien
		if nb not in listFin:
			listFin.append(nb)
	listFin.sort()
	print(("La liste initiale est : {}\nLa liste triée est : {}").format(listeDeb, listFin))


# Exercice 10.32 : Recherche le mot le plus long d'une phrase
# Voir cours SiteDuZero


# Exercice 10.33 : Permet d'afficher l'enembledes jours de l'année
if __name__ == '__main__':
	# Liste permettant le parcours des mois
	mois = [[31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31], ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin", "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]]
	jour = ["Dimanche", "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi"]
	jourAnnee, jourMois, jourSemaine, el = 0, 0, 0, 0
	while jourAnnee < 365:
		jourAnnee, jourMois = jourAnnee + 1, jourMois + 1
		jourSemaine = (jourAnnee+3) % 7  # Permet de commencer par Jeudi
		# Changement de mois :
		if jourMois > mois[0][el]:
			# On remet à 0 le jour et on change de mois
			jourMois, el = 1, el + 1
		print(jour[jourSemaine], jourMois, mois[1][el])
