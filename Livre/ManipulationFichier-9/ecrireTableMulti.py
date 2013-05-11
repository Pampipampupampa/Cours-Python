#! /usr/bin/env python
# -*- coding:Utf8 -*-


"PROGRAMME GÉNÉRANT UN FICHIER AVEC LES TABLES DE MULTIPLICATION DE 2 À 30 (20 POUR CHAQUE)"

################################################################
############# Importation fonction et modules : ################
################################################################



from os import chdir



###################################################################################################
############# Gestion d'évènements : définition de différentes fonctions utiliées  : ##############
###################################################################################################



def tableFichier(debut, fin, max=20):
	i = 0
	opFichier = open('table', 'w')
	while debut <= fin:
		while i < max:
			# Ecrit la table dans le fichier au fur et à mesure
			opFichier.write(str(debut) + '*' + str(i+1) + '=' + str((i+1)*debut) + '\n')
			i += 1
		debut += 1
		i = 0
		opFichier.write('\n')
	opFichier.close()



######################################################
############## Programme principal : #################
######################################################



# Définition du répertoire courant
chdir("/home/pampi/Documents/Git/Cours-Python/Livre/ManipulationFichier-9/Stockage")



# Ecriture dans le fichier
tableFichier(2, 30)