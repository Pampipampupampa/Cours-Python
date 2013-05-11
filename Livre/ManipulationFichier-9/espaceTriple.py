#! /usr/bin/env python
# -*- coding:Utf8 -*-


"PROGRAMME PERMETTANT DE MODIFIER UN FICHIER EN AJOUTANT DES TRIPLE ESPACES"

################################################################
############# Importation fonction et modules : ################
################################################################


from os import chdir


###################################################################################################
############# Gestion d'évènements : définition de différentes fonctions utiliées  : ##############
###################################################################################################


"Fonction permettant de lire l'intégralité d'un fichier et de modifier les espaces"
def ecritureTriple(source, destination):
	fs = open(source, 'r')
	fd = open(destination,'w')
	while 1:
		txt = fs.read(1)
		if txt == "": # Si on atteintla fin du fichier alors on stop la boucle avec l'instruction "break"
			break
		if txt == " ":
			txt = txt*3
		fd.write(txt)
	fs.close()
	fd.close()
	return # On obtient ainsi une copie du fichier source avec des triple espaces

######################################################
############## Programme principal : #################
######################################################


# Définition du répertoire courant
chdir("/home/pampi/Documents/Git/Cours-Python/Livre/ManipulationFichier-9/Stockage")

# Création de la copie avec espace en triple
ecritureTriple('espaceSimple', 'espaceTriple')
