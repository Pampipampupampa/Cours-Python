#! /usr/bin/env python
# -*- coding:Utf8 -*-

"PROGRAMME TRANSFORMANT LES NOMBRES À VIRGULES EN NOMBRE ENTIER ARRONDI"
"EXERCICE 9.5"

################################################################
############# Importation fonction et modules : ################
################################################################



from os import chdir



###################################################################################################
############# Gestion d'évènements : définition de différentes fonctions utiliées  : ##############
###################################################################################################



def versInteger(ligne):
	nombreFloat = float(ligne)
	nombreEntier = int(nombreFloat + 0.5)
	return str(nombreEntier)



######################################################
############## Programme principal : #################
######################################################



# Définition du répertoire courant
chdir("/home/pampi/Documents/Git/Cours-Python/Livre/ManipulationFichier-9/Stockage")



# Lecture et écriture après transformation
fs = open('nombreFloat', 'r')
fd = open('nombreInteger', 'w')


while 1:
	ligneSource = fs.readline()
	if ligneSource == "" or ligneSource == '\n':
		break
	ligneSource = versInteger(ligneSource)
	fd.write(ligneSource + '\n')

fs.close()
fd.close()