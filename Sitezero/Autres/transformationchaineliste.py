import os

"""chaines en liste"""

chaine = "bonjour les enfants"
chaine.split(" ") # permet de séparer les caractère de la chaine afin de créer une liste
print(chaine.split(" ")) # ici " " représente le séparateur : premiere découpe jusqu'au premier espace, ect, ...



"""liste en chaine"""

liste = ["bonjour", "les", "enfants"]
print(" ".join(liste)) # on indique au début le séparateur contrairement à split


"""exemple pratique"""

def flottant(nbr): # permet de réduire le nombre de chiffre après la virgule
    if type(nbr) is not float:
        raise TypeError(" On demande un flottant ")
        raise NameError(" On demande un nombre ")
    nbr = str(nbr)
    entier, flottant = nbr.split(".")
    return ",".join([entier, flottant[:3]])

print(flottant(2.77777777777777))



"""appel de paramètres"""

# le "*" capture les paramètres en tuple
def appel(nom, *parametre): # fonction affichant un nombre infini de paramètre ou 0 selon (rôle du *) et ayant un paramètre obligatoire (nom)
    print("{} a obtenu : {} ".format(nom, parametre))

appel(1)
appel(4)
appel("autruche", 4.555, 4, [4])



"""appel de paramètre nommés et conversion de tuples""" # Pas fonctionnel

def afficher(*parametre, sep = " ", fin = "\n"):
    # sep permet de choisir le séparateur entre les chaines (ici un espace)
    # fin permet de définir ce qui se passe une fois fini (ici retour à la ligne)
    
    parametre = list(parametre) # on transforme le tuple en liste afin de le modifier
    
    for i, parametre in enumerate(parametre): # on transforme la liste en chaine de caractère
        parametre[i] = str(parametre)
    chaine = sep.join(parametre) # on ajoute un espace (sep) entre chaques chaines 
    chaine += fin # on ajoute un retour ligne à la fin
    return print(chaine, end = "")

afficher(liste)




"""transformer liste en paramètre de fonction"""
liste = [1, 7, 16, 55]
print(*liste) # le "*" décompose plusieurs paramètres avant de les envoyer


