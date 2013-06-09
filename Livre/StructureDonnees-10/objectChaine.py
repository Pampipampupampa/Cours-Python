#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""PROGRAMMES AUTOUR DES CHAINES DE CARACTÈRES"""
"EXERCICE 10.21 ET 10.22 ET 10.23 ET 10.24 ET 10.25 ET 10.26"

###########################################
#### Importation fonction et modules : ####
###########################################


from math import pi


###############################################################################
#### Gestion d'évènements : définition de différentes fonctions utiliées : ####
###############################################################################

def caracSphere(diam):
	"""Renvoi les caractéristiques de la sphère à partir de son diamètre"""
	diam = float(diam)
	r = diam/2
	section = pi*r**2
	aire = 4*pi*r**2
	volume = 4/3*pi*r**3
	chaine = "Une sphère ayant un diamètre de {0:4.2f} [m] possède un rayon de {1:4.2f} [m], une section de section de {2:6.2f} [m2], une aire de {3:6.3f} [m2], et un volume de {4:6.3f} [m3]".format(diam, r, section, aire, volume)
	return chaine


def arrondie(nombre):
	"""Renvoi une chaine contenant les nombres arrondies à .0 ou .5"""
	entier = int(nombre)
	flottant = nombre - entier
	if flottant < 0.25:
		flottant = 0
	elif flottant < 0.75:
		flottant = 0.5
	else:
		flottant = 1
	arrondi = entier + flottant
	return arrondi


###############################
#### Programme principal : ####
###############################


# Exercice 10.21 : Ajoute une majuscule à chaque mot du texte
if __name__ == '__main__':
	# fichier ouvert devant être encodé en Latin1
	fichierSource = open("Sources/latin", 'r', encoding="Latin-1")
	# Fichier cible encodé en UTF-8
	fichierCible = open("Sources/Utf8", 'w', encoding="Utf-8")
	while 1:
		li = fichierSource.readline()
		if li == "":
			break
		fichierCible.write(li.title())
	fichierSource.close()
	fichierCible.close()


# Exercice 10.22 : Remplace " " par "_*_" et ouverture en binaire
if __name__ == '__main__':
	fichierSource = open("Sources/latin", 'rb')
	fichierCible = open("Sources/Utf8bin", 'wb')
	while 1:
		li = fichierSource.readline()
		if li == b"":  # C'est une variable binaire donc il faut la comparer avec  une chaine de même type
			break
		ch = li.decode("Latin-1")
		ch = ch.replace(" ", "_*_")
		li = ch.encode("Utf-8")
		fichierCible.write(li)
	fichierSource.close()
	fichierCible.close()


# Exercice 10.23 : Indique le nombre de mots dans le texte
if __name__ == '__main__':
	# fichier ouvert devant être encodé en Latin1
	fichierSource = open("Sources/latin", 'r', encoding="Latin-1")
	compteur = 0
	while 1:
		chaine = fichierSource.readline()
		if chaine == "":
			break
		liste = chaine.split(" ")
		compteur = compteur + len(liste)  # On ajoute chaques nouveaux mots
	fichierSource.close()
	resultat = "Il y a donc {:6.3f} mots dans ce texte"
	print(resultat.format(compteur))


# Exercice 10.24 : Fusion de ligne de texte qui ne commencent pas pas une maj
if __name__ == '__main__':
	# fichier ouvert devant être encodé en Latin1
	fichierSource = open("Sources/latin", 'r', encoding="Latin-1")
	# Fichier cible encodé en UTF-8
	fichierCible = open("Sources/fusionLigne", 'w', encoding="Utf-8")
	chaine1 = fichierSource.readline()
	while 1:
		chaine2 = fichierSource.readline()
		if not chaine2:
			break
		if chaine2[0] in "AZERTYUIOPQSDFGHJKLMWXCVBNÙÉÈÇÀÊÂÔÛÄÏ":
			fichierCible.write(chaine1)
			chaine1 = chaine2
		else:
			chaine1 = chaine1[:-1] + " " + chaine2
	fichierCible.write(chaine1)
	fichierSource.close()
	fichierCible.close()


# Exercie 10.25 : Création d'un fichier contenant les caractéristiques des sphères dont les diamètres sont contenus dans le fichier source
if __name__ == '__main__':
	fichierSource = open("Sources/sphere", 'r', encoding="Utf-8")
	fichierCible = open("Sources/sphereTraite", 'w', encoding="Utf-8")
	while 1:
		diam = fichierSource.readline()
		if diam == "" or diam == "\n":
			break
		fichierCible.write(caracSphere(diam) + "\n")
	fichierCible.close()
	fichierSource.close()


# Exercice 10.26 : Arrondie à .5 près d'un nombre
if __name__ == '__main__':
	fichierSource = open("Sources/nombre", 'r', encoding="Utf-8")
	fichierCible = open("Sources/nombreTraite", 'w', encoding="Utf-8")
	while 1:
		nombre = fichierSource.readline()
		if nombre == "" or nombre == "\n":
			break
		fichierCible.write(str(arrondie(float(nombre))) + "\n")
	fichierCible.close()
	fichierSource.close()
