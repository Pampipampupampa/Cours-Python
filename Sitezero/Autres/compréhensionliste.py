import os

"""compréhension de liste"""

listebase = [0, 1, 4, 6]
print([nb ** 2 for nb in listebase]) # on remplace dans la liste chaque chaine par chaine * chaine

print([nb for nb in listebase if nb % 2 == 0]) # on récupère donc que les valeurs paires

# exemple
retire = 8 # quantité retiré chaques semaines
fruitstock = [3, 44, 6, 9] # 3 poires, ...
print([nbfruit - retire for nbfruit in fruitstock if nbfruit > retire]) # si nombre fruit > fruit acheté(retire) alors on soustrait et on affiche



"""exemple plus réaliste permettant  de classer par quantité les différents fruits"""

# solution 1 avec methode sorted (possible de passer sur 1 ligne)

inventaire = [
    ("pommes", 22),
    ("melons", 4),
    ("poires", 18),
    ("fraises", 76),
    ("prunes", 51),
    ]
inventaire_inverse = [(qtt, nom) for (nom, qtt) in inventaire] # permet d'inverser nom et quantité afin de pouvoir trier correctement la quantité
print(inventaire_inverse)

inventaire = [(nom, qtt) for (qtt, nom) in sorted(inventaire_inverse, reverse = True)] # True permet de ranger en ordre décroissant en partant du haut
print(inventaire)


# solution 2 avec sort ( pas trouver comment passer sur une ligne)
inventaire = [
    ("pommes", 22),
    ("melons", 4),
    ("poires", 18),
    ("fraises", 76),
    ("prunes", 51),
    ]

inventaire_inverse = [(qtt, nom) for (nom, qtt) in inventaire]
inventaire_inverse.sort(reverse = True)
inventaire = [(nom, qtt) for (qtt, nom) in inventaire_inverse]
print(inventaire)
