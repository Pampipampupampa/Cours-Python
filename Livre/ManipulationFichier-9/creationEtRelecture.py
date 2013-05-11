#! /usr/bin/env python
# -*- coding:Utf8 -*-


"PROGRAMME PERMETTANT DE LIRE OU MODIFIER UN FICHIER DU REPERTOIRE COURANT"
"EXERCICE 9.1"

################################################################
############# Importation fonction et modules : ################
################################################################



from os import chdir, getcwd



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
	while 1:
		txt = obFichier.readline()
		if txt == "":
			break
		print(amputation(txt))
	obFichier.close()



"Fonction permettant l'écriture du fichier"
def ecriture(source):
	obFichier = open(source, 'a')
	while 1:
		txt = input("Veuillez ajouter le texte pour cette ligne et finir par <Entree> (finir l'ajout par deux <Entree>) : ")
		if txt == "":
			break
		else:
			obFichier.write(txt + '\n')
	obFichier.close()




######################################################
############## Programme principal : #################
######################################################



# Définition du répertoire courant
chdir("/home/pampi/Documents/Git/Cours-Python/Livre/ManipulationFichier-9/Stockage")
rep_courant = getcwd()



# Sélection du fichier à étudié
choixFichier = input("Ecrire le nom du fichier à étudié (Pour être lu le fichier doit être dans ce dossier : " + rep_courant + " ) : ")



# Choix de l'action à réaliser
choixUtilisation = input("Ecrire <R> ou <r> pour lire ce fichier, ou alors <W> ou <w> pour le modifier : ")
while 1:
	if choixUtilisation=='W' or choixUtilisation=='w':
		ecriture(choixFichier)
		break
	if choixUtilisation=='R' or choixUtilisation=='r':
		lecture(choixFichier)
		break
	else:
		choixUtilisation = input("Ecrire <R> ou <r> pour lire ce fichier, ou <W> ou <w> pour le modifier : ")


