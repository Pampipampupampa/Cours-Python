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




######################################################
############## Programme principal : #################
######################################################



# Définition du répertoire courant
chdir("/home/pampi/Documents/Git/Cours-Python/Livre/ManipulationFichier-9/Stockage")



# Détermination des 3 fichiers à utiliser
fichA = input("Nom du premier fichier : ")
fichB = input("Nom du second fichier : ")
fichC = input("Nom du fichier destinataire : ")
fiA = open(fichA, 'r')
fiB = open(fichB, 'r')
fiC = open(fichC, 'w')



# Alternance de l'écriture sur le fichier <fichC>
while 1:
    ligneA = fiA.readline()    
    ligneB = fiB.readline()
    if ligneA =="" and ligneB =="":
        break               # On est arrivé à la fin des 2 fichiers
    if ligneA != "":
        fiC.write(ligneA)
    if ligneB != "":    
        fiC.write(ligneB)



# Fermeture et enregistrement des fichiers
fiA.close()
fiB.close()
fiC.close()
