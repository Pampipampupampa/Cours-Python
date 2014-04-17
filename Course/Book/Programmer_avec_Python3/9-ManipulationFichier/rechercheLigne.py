#! /usr/bin/env python
# -*- coding:Utf8 -*-


"PROGRAMME RECHERCHANT DES INFORMATIONS DANS UN FICHIER ET RETOURNE LA LIGNE CORESPONDANTE"
"EXERCICE 9.10"

################################################################
############# Importation fonction et modules : ################
################################################################



from os import chdir



###################################################################################################
############# Gestion d'évènements : définition de différentes fonctions utiliées  : ##############
###################################################################################################



# Définition du répertoire courant
chdir("/home/pampi/Documents/Git/Cours-Python/Livre/ManipulationFichier-9/Stockage")



def rechercheCodePostal(source):
	"Recherche dans le fichier une portion de texte"
	i, flag, champs = 0, 0, 0 # Champs sert à choisir la position de l'élément recherché
	chaine = ""
	while i < len(source):
		if source[i] == "#":
			champs += 1
			if champs == 3:
				flag = 1
			elif champs == 4:
				break
		elif flag == 1:
			chaine = chaine + source[i]
		i += 1
	return chaine



######################################################
############## Programme principal : #################
######################################################



fichierSource = open('membreClubAjout', 'r')
recherche = input("Code Postal à rechercher ? ")
while 1:
	ligne = fichierSource.readline()
	if ligne == "": # Fin du fichier et recherche infructueuse
		break
	if rechercheCodePostal(ligne) == recherche: # Recherche trouvée
		print(ligne)

fichierSource.close()
