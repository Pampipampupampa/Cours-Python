#! /usr/bin/env python
# -*- coding:Utf8 -*-


"DÉCOUPAGE ET RÉASSEMBLAGE D'UNE CHAINE DE CARACTÈRES"
"EXERCICE 10.2"

################################################################
############# Importation fonction et modules : ################
################################################################




###################################################################################################
############# Gestion d'évènements : définition de différentes fonctions utiliées  : ##############
###################################################################################################



def reAssemblage(chaine):
	"Découpe une chaine de caractères 5 par 5 et les regroupes dans une liste"
	liste = []
	i, deb, fn = 0, -5, 0 # On décale les indices de base de 5 afin de pouvoir obtenir tout les éléments (voir plus bas)
	while fn < len(chaine):
		deb, fn = fn, fn + 5 # Incrémenter avant la vérification afin de récupérer les derniers caractères si la chaine n'est pas un multiple de 5
		if fn > len(chaine):
			fn = len(chaine)
		liste.append(chaine[deb:fn])
		i += 1
	return liste



def reAssemblageCorrection(chaine):
	"Variante de la fonction reAssemblage : correction livre"
	liste = []
	i, deb, fn = 0, 0, 5
	while deb < len(chaine):
		if fn > len(chaine):
			fn = len(chaine)
		liste.append(chaine[deb:fn])
		i += 1
		deb, fn = fn, fn + 5 
	return liste



def inverse(chaine):
	"Réaffecte les éléments de la liste dans une chaine de caractère et les inverses"
	ch = ""
	i = len(chaine)
	while i > 0:
		i -= 1 # Correspond au dernier élément de la liste
		ch = ch + chaine[i]
	return ch

	

######################################################
############## Programme principal : #################
######################################################


chaine = "Je suis bon, bien bon, jeune tortue des montagnes"



# Réalise la première transformation en affichant les caractères dans une liste
liste = reAssemblage(chaine)
print(reAssemblage.__doc__) # Permet d'afficher la docliste d'une fonction (ou d'une classe)
print(liste)



# Réalise la seconde et dernière étape : le passage à l'inverse (5 par 5)
chaineInverse = inverse(liste)
print(inverse.__doc__) # Permet d'afficher la docliste d'une fonction (ou d'une classe)
print(chaineInverse)



# Correction du livre
liste = reAssemblageCorrection(chaine)
chaineInverse = inverse(liste)
print(liste)
print(chaineInverse)