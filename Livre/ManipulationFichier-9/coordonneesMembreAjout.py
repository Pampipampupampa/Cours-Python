#! /usr/bin/env python
# -*- coding:Utf8 -*-


"PROGRAMME AJOUTANT DES INFORMATIONS À UN FICHIER CONTENANT DES INFOS SUR LES MEMBRES D'UN CLUB OU UN AUTRE"
"EXERCICE 9.9"

################################################################
############# Importation fonction et modules : ################
################################################################


from os import chdir


###################################################################################################
############# Gestion d'évènements : définition de différentes fonctions utiliées  : ##############
###################################################################################################


def organisation(source):
	"Organize source file in list"
	i, mot = 0, ""
	infos = []
	while i < len(source):
		if source[i] == "#":
			infos.append(mot)
			mot = ""
		else:
			mot = mot + source[i]
		i += 1
	return infos


def encodage(infos):
	"Add informations to the list (birth date, sex"
	print("Veuillez renseigner les nouvelles informations ou <Enter> pour quitter")
	# afficher les informations déja écrites
	i = 0
	while i < len(infos):
		print(infos[i], end =' ')
		i = i + 1

	print() # Retour à la ligne

	# Enregistrement des nouvelles infos
	while 1:
		naissance = input("Date de naissance : ")
		sexe = input("Sexe : ")
		print(naissance, sexe)
		verif = input("C'est bon ? <Enter> si oui sinon une autre touche")
		if verif == "":
			break
	infos.append(naissance)
	infos.append(sexe)
	return infos


def enregistrer(infos):
	"Write new data with a '#' separator"
	i = 0
	while i < len(infos):
		fichierDestination.write(infos[i] + '#')
		i += 1
	fichierDestination.write('\n') # Retour à la ligne


######################################################
############## Programme principal : #################
######################################################


# Définition du répertoire courant
chdir("/home/pampi/Documents/Git/Cours-Python/Livre/ManipulationFichier-9/Stockage")


# Ajout et inscription d'informations dans le fichier
fichierSource = open('membreClub', 'r')
fichierDestination = open('membreClubAjout', 'w')
while 1:
	ligne = fichierSource.readline()
	if ligne == "" or ligne == "\n":
		break
	# Permet d'organiser sous forme de liste les éléments de la ligne
	liste = organisation(ligne)
	liste = encodage(liste)
	enregistrer(liste)

fichierDestination.close()
fichierSource.close()
