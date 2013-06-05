#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""ENSEMBLE DE COURS SUR LE CHAPITRE : APPROFONDIR LES STRUCTURES DE DONNEES"""
"COURS 10"

###########################################
#### Importation fonction et modules : ####
###########################################


from os import chdir

###############################################################################
#### Gestion d'évènements : définition de différentes fonctions utiliées : ####
###############################################################################

###############################
#### Programme principal : ####
###############################


# Indiçage, extraction et longueur
nom = "Damien"
print(nom[1], nom[3], nom[5])  # Extraction à partir du début de la chaine
print(nom[-1], nom[-3], nom[-5])  # Extraction à partir de la fin de la chaine
print(len(nom))  # Affiche la longueur de la chaine
print(nom[0:4])  # Extraction des caractères 1 à 4 (inclusion du premier et exclusion du dernier = les indices se trouvent donc entres les caractères)
print(nom[0:2], nom[3:6])


# Concaténation et répétition
n = 'abc' + 'def'  # Concaténation
m = 'zut ! ' * 4  # Répétition
print(n, m)


# Utilisation d'une boucle while pour parcourir une chaine à proscrire
nom = "Nadia Bois"
index = 0
while index < len(nom):
	print(nom[index] + '**', end=' ')
	index += 1
print(end='\n')  # Seulement pour revenir à la ligne avant d'éffectuer le code suivant


# On préfèrera la forme suivante moins lourde autant en ligne qu'en rendement
nom = "Nadia Bois"
for car in nom:
	print(car + '&', end=' ')
print(end='\n')  # Seulement pour revenir à la ligne avant d'éffectuer le code suivant


# Autre avantage : il a bon goût de conserver le typage des éléments
divers = ['lézard', 3, 3.22, [5, 'Jean']]
for element in divers:
	print(element, type(element))


# Utilisation de l'instruction <in> seule (sans <for>)
car = "e"
voyelles = "aeiouyAEIOUYàâÀÂéèêëÊËÉÈùÙîïÎÏ"
if car in voyelles:
	print(car, " est une voyelle.")


# Utilisation de l'instruction <in> pour les listes
n = 5
liste = [1, 2, 3, 4, 5, 6]
if n in liste:
	print(n, " est dans la liste")


# Les chaînes de sont pas modifiables mais on peut les composer entres elles
salut = "Bonjour les enfants"
salut = 'b' + salut[1:]  # On modifie la première lettre de la chaine en créant une autre chaine
print(salut)


# On peut trier avec certaines limites les chaines
# Attention il ne faut pas mélanger maj avec minuscule ou accentuation sinon
# À cause de la norme ASCII qui attribut un nombre à chaque caractère le trie
# sera éronné
while True:
	mot = input("Entrez un truc : ")
	if mot == "":
		break
	if mot < "limonade":
		place = "précède"
	elif mot > "limonade":
		place = "suit"
	else:
		place = "se confond avec"
	print("Le mot " + mot + " " + place +
	      " le mot limonade dans l'ordre alphabétique")


# Séquences d'octects : le type bytes
chaine = "Amélie et Eugène\n"
of = open("Sources/text1.txt", 'w')
of.write(chaine)
of.close()
of = open("Sources/text1.txt", 'rb')  # Ouverture en mode binaire
octet = of.read()
of.close()
print(type(octet))  # On a bien récupérer une variable <bytes> et non <string>
print(octet)  # On affuche la chaîne en bytes (mélange ASCII, hexadécimal, valeurs numériques)
for oct in octet:  # On affiche l'ensemble des valeurs en octet
	print(oct, end=' ')
print("en octet " + str(len(octet)) + " en caractères  " + str(len(chaine)))

# On ne peut pas enregistrer une chaine d'octects dans un fichier texte il faut utiliser <wb>
of = open("Sources/text1.txt", 'ab')  # Ouverture en mode binaire
of.write(octet)
# Définir une variable de type <bytes> : var = b'chaîne écrite en ASCII'


# Méthode permettant de convertir en string une variable en bytes
chCar = octet.decode("utf8")
print(chCar, type(octet), type(chCar))


# Méthode permettant l'encodage d'une variable en bytes suivant des normes différentes
chaine = "Bonne fête de Noël"
octectUtf8 = chaine.encode("Utf-8")
octectLatin1 = chaine.encode("Latin-1")
print(octectUtf8, octectLatin1)


# Assurer l'encodage d'un fichier texte dans un code voulu
chaine = "Amélie et Eugène\n"
of = open("Sources/text1.txt", "w", encoding="Latin-1")
of.write(chaine)
of.close()
of = open("Sources/text1.txt", 'rb')  # Ouverture en mode binaire
octet = of.read()
of.close()
print(octet)
# Attention comme l'encodage n'est plus celui de base réalisé par python il faut lui dire quel encodage il doit utiliser pour l'ouvrir
of = open("Sources/text1.txt", 'r', encoding="Latin-1")  # Ouverture en mode texte avec précision de l'encodage utilisé
chLue = of.read()
of.close()
print(chLue)
# of = open("Sources/text1.txt", 'r')  # Ouverture en mode texte
# chLue = of.read()  # Il ne peut pas l'ouvrir car il ne peut décoder le code correctement
# of.close()
# print(chLue)


# Accéder aux identifiants des caractères
print(ord("A"))  # Renvoi l'identifiant numérique du caractère dans les parenthèses
print(chr(65))  # Réalise l'inverse de <ord> et renvoi le caractère correspondant

# Écrire l'alphabet grec grâce aux identifiants des caractères
s = ""
i = 945  # L'identifiant de la première lettre de cet alphabet
while i < 999:
	s += chr(i)
	i += 1
print("Ensemble de l'alphabet grec : ", s)


#Evaluation des différentes erreurs possibles sur le slicing
mot = "Je suis un gros chat et donc j'aime les canards ?"
print(mot[-22:-112])  # Aucunes erreurs mais n'affiche rien
print(mot[22:111])  # Aucunes erreurs mais n'affiche rien
print([mot['e']])  # TypeError: string indices must be integers
print(mot[1111])  # IndexError: string index out of range
