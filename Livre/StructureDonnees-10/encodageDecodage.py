#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""PROGRAMMES RÉALISANT DES ENCODAGES DÉCODAGES AFIN DE MANIPULER LES CARACTÈRES ET LES NORMES"""
"EXERCICE 10.14 ET 10.15 ET 10.16 ET 10.17"

###########################################
#### Importation fonction et modules : ####
###########################################


###############################################################################
#### Gestion d'évènements : définition de différentes fonctions utiliées : ####
###############################################################################


def paroursASCII(deb, fin=91):
	"""Affiche les caractères correspondants au code ASCII (deb = début, fin = fin)"""
	alpha = ""
	while deb < fin:
		alpha += chr(deb)
		deb += 1
	return alpha


def minVersMaj(chaine):
	"""Converti en majuscules la phrase <chaine>"""
	chaineMaj = ""
	for car in chaine:
		code = ord(car)  # Variable récupérant le code de chaques caractères
		# Minuscules ordinaires
		if code > 96 and code < 123:
			code = code - 32
		# Minuscules accentuées (249 = signe divisé)
		elif code > 223 and code < 249:
			code = code - 32
		# Minuscules accentuées (249 = signe divisé)
		elif code > 249 and code < 255:
			code = code - 32
		else:
			code = code
		chaineMaj = chaineMaj + chr(code)
	return chaineMaj


###############################
#### Programme principal : ####
###############################


# Exercice 10.14
if __name__ == '__main__':
	maj = paroursASCII(65)
	min = paroursASCII(97, 123)
	print("Code ASCII alphabet MAJ : ", maj, "\nCode ASCII alphabet MIN : ", min)


# Exercice 10.15
if __name__ == '__main__':
	code = paroursASCII(128, 256)
	print("Ensemble des code ASCII de 128 à 256\n", code)
	code = paroursASCII(192, 256)
	print("Ensemble des code ASCII de 192 à 256\n", code)
	code = paroursASCII(224, 256)
	print("Ensemble des code ASCII de 224 à 256\n", code)


# Exercice 10.16
if __name__ == '__main__':
	phrase = "Les lutins sont des hermaphrodïtes de pâques  ö "
	transforme = minVersMaj(phrase)
	print(transforme)
