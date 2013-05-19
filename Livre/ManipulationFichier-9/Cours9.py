#! /usr/bin/env python
# -*- coding:Utf8 -*-

"ENSEMBLE DU COURS SUR LA MANIPULATION DE FICHIER (COURS 9)"
"COURS 9"

################################################################
############# Importation fonction et modules : ################
################################################################

from os import chdir, getcwd

# import os = importation de toutes les fonctions du module (risque de doublons de variables et donc d'interférence : méthode a utilisé le moins souvent possible)
# On préfèrera utilise la forme ci-dessus (from "module" import "fonction1, fonction2")

# Module spécialisé dans l'enregistrement de valeurs en conservant leur type
import pickle

###################################################################################################
############# Gestion d'évènements : définition de différentes fonctions utiliées  : ##############
###################################################################################################

"Fonction permettant de lire l'intégralité d'un fichier en transférant des portions de 50 caractères à la fois"
def copieFichier(source, destination):
	fs = open(source, 'r')
	fd = open(destination,'w')
	while 1:
		txt = fs.read(50)
		if txt == "": # Si on atteintla fin du fichier alors on stop la boucle avec l'instruction "break"
			break
		fd.write(txt)
	fs.close()
	fd.close()
	return # On obtient ainsi une copie du fichier source



"Recopie un fichier texte en ommetant les lignes commençant par #"
def filtre(source, destination):
	fs = open(source, 'r')
	fd = open(destination,'w')
	while 1:
		txt = fs.readline()
		if txt == "":
			break
		if txt[0] != '#':
			fd.write(txt)
	fs.close()
	fd.close()
	return



"Vérifie que le fichier que l'utilisateur tente d'ouvrir existe bien"
def existe(fname):
	try:
		f = open(fname, 'r')
		f.close()
		return 1
	except:
		return 0



######################################################
############## Programme principal : #################
######################################################


"Changement et vérification de la position du répertoire courant"
# On définit ici le chemin du répertoire courant (par défaut c'est le dossier contenant le fichier .py)
chdir("/home/pampi/Documents/Git/Cours-Python/Livre/ManipulationFichier-9/Stockage")

# fonction permettant de vérifier le chemin du répertoire courant ("get current working directory")
rep_courant = getcwd()

print(rep_courant)



"Ecriture séquentielle dans un fichier"
# La fonction "open" permet l'écriture dans un fichier et le mode "a" définit comment (<a> = append = ajout à la fin, <w> = write = reécriture et donc efface avant d'écrire, <r> = read = en lecture, <r+> = lecture et écriture)
obFichier = open('monFichier','w') # Variable objet-fichier
obFichier.write('Bonjour mon enfant !!!') # On ajoute du contenu dans le fichier créé (seulement des chaînes de caractères peuvent être écrites : la fonction str() permettra donc de formater en chaîne de caractères un nombre par exemple avant de l'écrire)
obFichier.write('Comment ça va ??')
obFichier.close() # Permet de fermer le fichier (opérations finies)

ouvreFichier = open('monFichier','r')

# La numéro indique combien de caractères doivent être lues à partir de la dernière lecture (ainsi dans la variable "r" on lit 20 caractères à partir du 7 ème car on a déja demandé de lire les 7 premiers)
t = ouvreFichier.read(7)
print(t)
r = ouvreFichier.read(20)
print(r)
ouvreFichier.close()



"Création d'une copie d'un fichier texte"
copieFichier('ModificationFlash.txt', 'copieModificationFlash')



"Séparation des éléments par saut de lignes"
# Rappel : Le marqueur de fin de ligne est le symbole "\n"
f = open('sautLigne', 'w')
f.write('Ligne 1\nLigne 2\nLigne 3\nLigne 4')
f.close()



"Méthode 'Readline et Readlines'"
fichier = open('sautLigne' ,'r')
ligne = fichier.readline() # On associe à la variable ligne la valeur de la première ligne du fichier "sautLigne" sous forme de chaîne de caractères
print(ligne)
print(fichier.readline())
ligne = fichier.readlines() # On associe à la varaiable ligne la valeur des lignes restantes (attention readlines != readline) sous forme de liste
print(ligne)
fichier.close()



"Création d'une copie après filtration des commentaires"
filtre('ModificationFlash.txt', 'copieFiltreModificationFlash')



"Fonctionnement du module pickle"
a, b, c = 27, 12.96, [5, 4.83, 'René']
f = open('donneesTest', 'wb') # Ouverture d'un fichier binaire en écriture

# Méthode permettant de conserver le type de l'élément à écrire dans le fichier (variable à insérer, fichier cible)
pickle.dump(a, f)
pickle.dump(b, f)
pickle.dump(c, f)
f.close()
f = open('donneesTest','rb') # Ouverture d'un fichier binaire en lecture

# Attribution des valeurs du fichier ainsi que leur type (int, string, ...)
j, k, l = pickle.load(f), pickle.load(f), pickle.load(f)

print(j, type(j))
print(k, type(k))
print(l, type(l))


"Exceptions et Vérifications"
filename = input('Entrez le nom du fichier svp : ')
i = 0
while i==0:
	if existe(filename):
		print("Ca ira cette fois")
		i = 1
	else:
		filename = input("Le fichier " + "< " + filename + " >" + " est introuvable. Veuillez entrer le nom d'un fichier existant : ")
		i = 0