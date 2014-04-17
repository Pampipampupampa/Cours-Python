#! /usr/bin/env python
# -*- coding:Utf8 -*-


"PROGRAMME RECHERCHANT LA PHRASE LA PLUS LONGUE ET L'AFFICHE"
"EXERCICE 9.2"

################################################################
############# Importation fonction et modules : ################
################################################################

from os import chdir


###################################################################################################
############# Gestion d'évènements : définition de différentes fonctions utiliées  : ##############
###################################################################################################



"Fonction permettant à l'utilisateur de rentrer autant d'éléments qu'il veut par ligne dans le fichier texte"
def amputation(chaine):
	i = 0
	new = "" # chaine vide
	while i < len(chaine)-1: # Permet de faire sauter le caractère <Retour à la ligne (\n)>
		new = new + chaine[i]
		i =i + 1
	return new



"Fonction permettant la lecture du fichier"
def lecture(source):
	obFichier = open(source, 'r')
	max = ""
	while 1:
		txt = obFichier.readline()
		if txt == "":
			break
		if len(max) < len(amputation(txt)):
			max = amputation(txt)
		else:
			max = max	
	obFichier.close()
	print(max)




######################################################
############## Programme principal : #################
######################################################



# Définition du répertoire courant
chdir("/home/pampi/Documents/Git/Cours-Python/Livre/ManipulationFichier-9/Stockage")



# Lit le fichier
lecture('test')


