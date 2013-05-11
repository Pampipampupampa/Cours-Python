import os

"""création de liste"""

liste = list() # première façon de créer des listes (ici liste vide)
print(type(liste))

liste = [1, "chat", 3.5, [], 5] # seconde façon de créer des listes
print(liste)


"""accéder aux éléments d'une liste"""

print(liste[0]) # accède au premier élément de la liste

liste[2] = "ouou" # modifie la valeur du 3ème élément de la liste
print(liste)



"""ajouter des objets à une liste"""

liste.append(777) # on remarque que contrairement aux chaines ici la liste est modifée mais elle ne renvois pas de valeur
print(liste)

liste.insert(2, "ddddd") # insertion à l'indice 2
print(liste)

liste2 =[111, 4444, 888]
liste.extend(liste2) # ajout à la fin de la liste la liste2
print(liste)

liste += liste2 # on ajoute les listes
print(liste)

liste.extend([111111111111111111, 22222222])
print(liste)



"""enlever/supprimer des objets d'une liste"""

variable = "rrrrrrrrrrrhhhhh"
print(variable)

del variable

del liste[6:8] # suppression d'objet dans la liste selon son emplacement
print(liste)

liste.remove(111) # suppression d'objet dans la liste selon son nom (suppr seulement le premier ayant ce nom)
print(liste)



"""parcourir une liste"""

liste = ["a", "rho", 1, 4.5]
i = 0
while i < len(liste): # on affiche la liste tant qu'on a pas tout affiché
    print(liste[i])
    i += 1

for elt in liste: # elt prend successivement la valeur des objets dans la liste
    print(elt)

for i, elt in enumerate(liste): # affiche indice et élément de la liste correspondant
    print("indice {} on a {} ".format(i, elt))

for elt in enumerate(liste): # affiche indice, élément de la liste correspondant ainsi que sa syntaxe (ex : "" pour un str)
    print(elt)

# création d'une nouvelle liste avec ou sans anti slash (\) pour stipuler un retour à la ligne
utile = [
    [1, "a"],
    [4, "d"],
    [7, "g"],
    [26, "z"],
    ]
for nb, lettre in utile: # affichage de la liste "utile" avec un formatage voulu
    print("La lettre {} est la {}ème de l'alphabet.".format(lettre, nb))
    


""" ATTENTION AUX TUPLES, ILS NE SONT PAS MODIFIABLES """

def decomposer(num, denom): # fonction renvoyant 2 paramètres partie entière et reste de la division
    resultat = num // denom
    reste = num % denom
    return resultat, reste

print(decomposer(2, 5))
test = decomposer(2, 5)
test.insert(1, "eeee") # renvoi une erreur car on ne peut pas le modifier
print(test) 










