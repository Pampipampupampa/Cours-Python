#! /usr/bin/env python
# -*- coding:Utf8 -*-


"PROGRAMMES D'INITIATION À L'INSTRUCTION FOR ... IN ..."
"EXERCICE 10.6 et 10.7 et 10.8"

################################################################
############# Importation fonction et modules : ################
################################################################




###################################################################################################
############# Gestion d'évènements : définition de différentes fonctions utiliées  : ##############
###################################################################################################



def compte(chaine, serie):
	"""compte le nombre de d'occurence des caractères contenues dans serie"""
	for car in serie:
		n = compteCar(chaine, car)
		print("Caractère : " + car + " = " + str(n))



def compteCar(chaine, car):
	"""Comptage des occurences et renvois l'information à la fonction compte"""
	if len(chaine) == 0:
		return 0
	i = 0
	for uu in chaine:
		if uu == car:
			i += 1
	return i
	


######################################################
############## Programme principal : #################
######################################################



# Utilisation de l'instruction <for> pour écrire différents noms
prefixe = "JKLMNOP"
suffixe = "ack"
for car in prefixe:
	print(car + suffixe)



# Utilisation de <for> pour compter le nombre de mots dans une phrase 
phrase = "Je suis la phrase, combien de mot me compose ?"
i = 0
for car in phrase:
	if car == " ":
		i += 1
print(i + 1) # On ajoute 1 car il n'y a pas d'espace à la fin d'une phrase



# Utilisation de <for> pour compter l'occurence d'une lettre dans une phrase
i = 0
for car in phrase:
	if car == 'e' or car == 'é' or car == 'è' or car == 'ê' or car == 'ë':
		i += 1
print("Il y a donc " + str(i) + " fois l'apparition du e.")



# Utilisation de <for> pour compter l'occurence d'un groupe de lettre
if __name__ == '__main__':
	print(phrase)
	compte(phrase, "éeèêë")