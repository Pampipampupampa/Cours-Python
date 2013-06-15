#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""APPRENTISSAGE DES TUPLES ET DES DICTIONNAIRES"""
"COURS 10 PART 3"

###########################################
#### Importation fonction et modules : ####
###########################################


###############################################################################
#### Gestion d'évènements : définition de différentes fonctions utiliées : ####
###############################################################################


###############################
#### Programme principal : ####
###############################


"""                       """
"""Le point sur les TUPLES"""
"""                       """


# Création d'un tuple : les parenthèses ne sont pas obligatoires mais
# permettent une meilleure lisibilité
tup = ("a", "b", "c", "d", "e")
print(tup, len(tup))


# Contrairement aux listes les éléments ne sont pas modifiable (comme les
# chaines de caractères), cependant le reste des actions restent possibles
tup = ("André",) + tup[1:]
# On remarque que l'addition est valable en respectant une syntaxe
# très precise
print(tup, len(tup))
for e in tup:
    print(e, end=':')
print()
# Les tuples sont moins gourmants en mémoire que les listes et représentent
# donc un choix plus judicieux dans ces cas là (l'interpréteur les traites
# aussi plus rapidement)


"""                              """
"""Le point sur les DICTIONNAIRES"""
"""                              """


# Ce type de données n'est pas contrairement aux autres des séquences
dico = {}
dico["computer"] = "ordinateur"
dico["mouse"] = "souris"
dico["keyboard"] = "clavier"
print(dico)
print(dico["mouse"])
# On remarque donc 2 choses :
# Les éléments ne sont pas rangés dans un ordre défini
# On peut ajouter un élément simplement en ajoutant  une paire clé/valeur
dico["cat"] = "chat"
print(dico)


inventaire = {"pommes": 430, "bananes": 312, "oranges": 274, "poires": 137}
print(inventaire, len(inventaire))
# Supprimer un élément du dictionnaire utilise la même fonction que pour
# les listes
del inventaire["pommes"]
print(inventaire, len(inventaire))


# Test d'appartenance
if "pommes" in inventaire:  # Non présent
    print("c'est gagné")
else:
    print("c'est perdu")
if "430" in inventaire:  # Seul l'élément de droite est vérifié
    print("c'est gagné")
else:
    print("c'est perdu")
if "bananes" in inventaire:  # Présent
    print("c'est gagné")
else:
    print("c'est perdu")


# Les dicos sont des objets
print(dico.keys())  # Affiche l'ensemble des clés du dictionnaire
print(dico.values())  # Affiche l'ensemble des valeurs du dictionnaire
print(dico.items())  # Affiche chaque couple sous forme d'un tuple

# Création d'une vraie copie du dictionnaire
# En effet comme pour les listes une simple affectation crée seulement un alias
magasin = inventaire.copy()
del inventaire["bananes"]
print(magasin, inventaire)

# On parcourt les <clé> du dictionnaire et dicotionnaire[] renvoit la <valeur>
# qui correspond à la <clé>
for elem in dico.keys():
    print("clé : {} ---- valeur : {}".format(elem, dico[elem]))


# Transformation en liste ou en tuple
a = list(dico.keys())
b = tuple(dico.keys())
print(a, b)


# Parcours du dictionnaire
# Attention on affecte successivement à la variable de parcours les clés et
# non des valeurs
# L'ordre de parcours est imprévisible


# Méthode générique non recommandée
for cle in inventaire:
    print(cle, inventaire[cle])


# Méthode recommandée : utilisation de double variable dans le parcours
# On a ainsi chaques élément du tuple crée
for cle, valeur in inventaire.items():
    print(cle, valeur)


# Variabilité des clés
arb = {(1, 2): "Peuplier", (3, 4): "Platane", (6, 5): "Palmier",
       (5, 1): "Cycas", (7, 3): "Sapin"}
print(arb, arb[6, 5])


# Prévoir les erreurs pouvant survenir grâce à la méthode get
print(arb.get((1, 2), "rien"), arb.get((2, 1), "rien"))
# L'utilisation de la méthode get en plus permet d'éviter d'obtenir une erreur
# si on cherche à avoir une clé qui n'existe pas


# Attention les dictionnaires ne sont pas des séquences
""" print(arb[1:3]) renvoi une <TypeError: unhashable type>"""
