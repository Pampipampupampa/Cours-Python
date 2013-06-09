#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""ENSEMBLE DE COURS SUR LE CHAPITRE : APPROFONDIR LES STRUCTURES DE DONNEES"""
"COURS 10 PART 2"

###########################################
#### Importation fonction et modules : ####
###########################################

###############################################################################
#### Gestion d'évènements : définition de différentes fonctions utiliées : ####
###############################################################################

###############################
#### Programme principal : ####
###############################


"""                                      """
"""Le point sur les chaines de caractères"""
"""                                      """

# Les chaînes sont des objets
# Possible de définir l'intervalle pour ces méthode dans la plupart
# des cas afin d'affiner son utilisation

print(dir("string"))  # Permet d'obtenir les méthodes associé à ce type d'objet
chaine = "cet exemple montre, la grandeur de Rome et anto  "

# Transforme en liste une chaine en choississant le séparateur
print(chaine.split(" "))

# Transforme en chaine une liste en choississant le séparateur
liste = chaine.split()
print(" ".join(liste))

# Recherche un mot et renvoi l'indice du premier caractère
mot = "Rome"
print(chaine.find(mot))

# Compte l'occurence d'un mot (sous chaine) dans une chaine
print(chaine.count("an"))

# Conversion en minuscule d'une chaine
print(chaine.lower())

# Conversion en majuscule d'une chaine
print(chaine.upper())

# Conversion du premier caractère de chaque mot en majuscule
print(chaine.title())

# Conversion du premier caractère de la chaine en majuscule
print(chaine.capitalize())

# Inverse la case d'une chaine de caractères
print(chaine.swapcase())

# Enlève les espaces en début et fin de chaine
print(chaine.strip())

# Remplacer un caractère par un autre
print(chaine.replace(" ", "*"))

# Recherche et renvoit l'indice de la première occurence du caractère
print(chaine.index("Rome"))

# Fonctions intégrées
print(float(3))  # Transforme en nombre flottant
print(int(3.3))  # Transforme en nombre entier
print(str(3))  # Transforme en chaine de caractères

# Formatage des chaines de caractères
coul = "verte"
temp = 18
# Sans indications les variables sont inscrites dans l'ordre donné
ch = "La couleur est {}, et la température est de {} °C"
print(ch.format(coul, temp))
# Si on assigne des chiffres alors le premier argument sera appliqué à 0, etc
ch = "La couleur est {0}, et la température est de {1} °C et pourtant on a \
toujours la couleur {0} et la température aux alentours de {1}"
print(ch.format(coul, temp))
# Définir un format différent pour l'affichage
# Possible d' ajouter le nombre max à afficher, la forme (exemple notation scientifique), le nombre max après la virgule et surement plus
ch = "La couleur est {0}, et la température est de {1:6.4f} °C et pourtant on a toujours la couleur {0} et la température aux alentours de {1:2.2e} ou en binaire {1:b}"
print(ch.format(coul, temp))


"""                       """
"""Le point sur les listes"""
"""                       """

# Accès un élément d'une liste dans une liste
liste = ["chocolat", "lettre", ['chat', 'souris', 'autruche'], 3]
print(liste)
liste[2][1] = "nouveau"  # On remplace le second élément de la liste dans la liste
print(liste)


# Méthodes principales sur les listes (il est souvent possible en plus de
# définir l'intervalle d'action)

# Trier la liste
liste = [2, 7, 1, 88, 3.9, 3.1, 6]
print(liste.sort())

# Ajouter un élément
liste.append(44)
print(liste)

# Inverser l'ordre
liste.reverse()
print(liste)

# Retrouver l'index d'un élément
print(liste.index(7))

# Effacer un élément de la liste (seulement la première itération)
liste.remove(88)
print(liste)


# Les instructions sur les listes
del liste[3]  # efface un élément à partir de l'index contrairement à remove
print(liste)
del liste[1:4]
print(liste)


# Slicing avancé


# Ajout d'élément dans une liste
mots = ["jambon", "fromage", "souris", "gruyère", "banane"]
mots[2:2] = ["miel", "saucisse"]  # Insertion des éléments à la 3ème place
print(mots)


# Suppression d'éléments
mots[2:5] = []  # supprime les éléments 3, 4 et 5 de la liste
print(mots)


# Remplacement d'éléments
mots[2:3] = ["ihihih"]  # Remplace le 3ème élément de la liste
print(mots)
mots[1:] = ["bambi", "choucroute"]  # Remplace l'ensemble des éléments après le premier
print(mots)


# Fonction range (comporte 3 arguments ; les négatifs sont autorisés)
print(list(range(10)))  # Convertir en liste une séquence de nombre


# Parcours de liste
prov = ["La", "raison", "du", "plus", "fort", "est", "toujours", "la", "meilleure"]
for mot in prov:
	print(mot, end=' ')


# Parcours de liste avec range
for n in range(3, 12, 3):
	print(n, n+1, n**2)


# Parcours de liste avec len et range afin d'obtenir chaques éléments et leurs indices
fable = ["Maître", "Corbeau", "sur", "un", "arbre", "perché"]
for n in range(len(fable)):
	print(n, fable[n])


# Particularité des variables dynamiques
divers = [3, 3.4, "chat", ["souris", 3, "EE"]]
for elem in divers:
	print(elem, type(elem))


# Opérations sur les listes


# L'addition
liste1 = divers
liste2 = fable
listeFinale = liste1 + liste2
print(listeFinale)


# La multiplication
listeFinale = liste1 * 3
print(listeFinale)


# Test d'appartenance
v = "chat"
if v in listeFinale:
	print("Ben oui !!")
if "souris" in listeFinale[3]:
	print("Ben oui ENCORE!!")


# L'affectation ne crée pas de copie indépendante mais elle renvoie vers la même liste
fable = ["Maître", "Corbeau", "sur", "un", "arbre", "perché"]
# Une simple affectation ne fait que attribuer à la une autre variable la liste en mémoire
copieFausse = fable
print(fable)
copieFausse[1] = "ttttt"
print(fable)  # On voit bien que les 2 variable sont liées
# C'est ce qu'on appelle un <ALIAS> !!!
# Pour faire une vraie copie on peut par exemple utilisé une fonction qui va ajouter à une liste les élément de la première (.append(x))

# Améliorer la syntaxe
couleurs = [noir, coco, marron, jaune, violet, bleue,
 			vert, turquoise, rouge, orange, cacao]
