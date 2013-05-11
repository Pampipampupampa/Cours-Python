import os

"""CREATION D'UNE FONCTION AVEC MULTIPLES CRITERES"""

def tablemulti(base, deb, fin): # differents parametres
    while deb <= fin:
        print(base, "fois", deb, "est égal à", base * deb)
        deb += 1


tablemulti(8,3,7) # table de 8 à partir de 3 jusqu'à 7

print("") # permet de separer simplement les différents tests


"""TEST D'UNE FONCTION A PLUSIEURS PARAMETRES"""

t, d, f = 11, 5, 10
while t < 21:
    tablemulti(t, d, f)
    t, d, f = t + 1, d + 3, f + 5

print("")



"""VARIABLE LOCALE OU GLOBALE"""

def test():
    p = 20
    print(p,q)

p, q = 15, 38
test() # on remarque que p change de valeur 
print(p, q) # on remarque que la valeur de p n'a pas été modifiée (la varible p dans la fonction test est donc une variable locale)

# afin de passer la variable de la fonction test en variable globale il faut ajouter l'instruction suivante

def monter():
    global a # permet la modification de la variable globale et non seulement la variable locale de la fonction monter
    a = a + 1
    print(a)

a = 15
monter()
monter() # on remrque bien que la variable globale a bien été modifiée

print("")



"""MODIFICATION D'UNE FONCTIONAFIN DE SORTIR UN RESULTAT EN LISTE"""

def table(base, deb, end):
    resultat = [] # déclaration d'une liste vide
    deb
    while deb <= end:
        b = base * deb
        resultat.append(b) # on ajoute le resultat de l'operation précédente à la liste
        deb += 1 # incrémente de 1 afin d'éviter une boucle infinie
    return resultat # renvois le resultat

test = table(2, 4, 8) # associe à la variable test le resultat de la fonction
print(test)

print("")

