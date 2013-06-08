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
