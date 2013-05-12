#! /usr/bin/env python
# -*- coding:Utf8 -*-


"PROGRAMME CRÉANT UN FICHIER EN ALTERNANT UNE LIGNE DE L'UN PUIS DE L'AUTRE"
"EXERCICE 9.7"

################################################################
############# Importation fonction et modules : ################
################################################################



from os import chdir



###################################################################################################
############# Gestion d'évènements : définition de différentes fonctions utiliées  : ##############
###################################################################################################



"Demande à l'utilisateur les informations  à ajoutées"
def ajout():
	while 1:
		nom = input("nom ou <Enter> pour terminer : ")
		if nom == "":
			return [] # Correspond à la fin de l'enregistrement
		prenom = input("prenom : ")
		adresse = input("adresse : ")
		code = input("code postal : ")
		local = input("Localité : ")
		tel = input("numéro de téléphone : ")
		print(nom, prenom, adresse, code, local, tel)
		verif = input("Si les informations vous conviennent presse <Enter> sinon une autre touche")
		if verif == "":
			break
	return [nom, prenom, adresse, code, local, tel]



"Ecrit et formate le fichier"
def enregistrement(listeAjout):
	i = 0
	while i < len(listeAjout):
		opFichier.write(listeAjout[i] + ' ## ')
		i += 1
	opFichier.write('\n') # Permet de séparer par un saut de ligne les différents membres



######################################################
############## Programme principal : #################
######################################################



# Définition du répertoire courant
chdir("/home/pampi/Documents/Git/Cours-Python/Livre/ManipulationFichier-9/Stockage")



# Ajout et inscription d'informations dans le fichier
opFichier = open('membreClub', 'a')

while 1:
	infos = ajout()
	if infos == []:
		break
	enregistrement(infos)

opFichier.close()