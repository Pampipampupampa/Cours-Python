#! /usr/bin/env python
# -*- coding:Utf8 -*-


"PROGRAMME PERMETTANT DE COMPARER 2 FICHIERS ET D'AVERTIR DÈS QU'UNE DIFFÉRENCE SURVIENT"
"EXERCICE 9.6"

################################################################
############# Importation fonction et modules : ################
################################################################


from os import chdir


###################################################################################################
############# Gestion d'évènements : définition de différentes fonctions utiliées  : ##############
###################################################################################################




######################################################
############## Programme principal : #################
######################################################



# Définition du répertoire courant
chdir("/home/pampi/Documents/Git/Cours-Python/Livre/ManipulationFichier-9/Stockage")



# Comparaison des 2 fichiers entre eux
fb = open('base', 'r')
fc = open('basecopie', 'r')

caractere, flag = 0, 0 # Le flag change une fois qu'une différence est trouvée
while 1:
	fichier1 = fb.read(1)
	fichier2 = fc.read(1)
	if fichier1 == "" or fichier2 == "":
		break
	if fichier2 != fichier1:
		flag = 1
		break
	caractere += 1


fb.close()
fc.close()



# Affichage du résultat
print("Ces 2 fichiers", end = ' ')
if flag == 1:
	print("sont identiques jusqu'au caractère : ", caractere, " (", fichier1, " != ", fichier2, ") ")
else:
	print("sont strictement identiques")