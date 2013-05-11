#! /usr/bin/env python
# -*- coding:Utf8 -*-


"PROGRAMME PERMETTANT DE MODIFIER UN FICHIER EN AJOUTANT DES TRIPLES ESPACES"
"PROGRAMME DU LIVRE AJOUTANT CERTAINES METHODES DE <OPEN>"
################################################################
############# Importation fonction et modules : ################
################################################################



from os import chdir



###################################################################################################
############# Gestion d'évènements : définition de différentes fonctions utiliées  : ##############
###################################################################################################



def triplerEspaces(ch):
    "fonction qui triple les espaces entre mots dans la chaîne ch"
    i, nouv = 0, ""
    while i < len(ch):
        if ch[i] == " ":
            nouv = nouv + "   "
        else:
            nouv = nouv + ch[i]
        i = i +1    
    return nouv



######################################################
############## Programme principal : #################
######################################################



# Définition du répertoire courant
chdir("/home/pampi/Documents/Git/Cours-Python/Livre/ManipulationFichier-9/Stockage")


# Demande le nom du dossier
NomF = 'espaceTriple2'


# Creation de la copie
fichier = open(NomF, 'r+')              # 'r+' = mode read/write
lignes = fichier.readlines()            # lire toutes les lignes
n=0
while n < len(lignes):
    lignes[n] = triplerEspaces(lignes[n])
    n =n+1
    

# Remplacement de l'ancien fichier
fichier.seek(0)                         # retour au début du fichier
fichier.writelines(lignes)              # réenregistrement du fichier
fichier.close()


