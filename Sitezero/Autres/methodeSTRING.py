import os




"""méthodes de la classe str"""

chaine = "  NE CRIE PAS SI FORT ! EE "
print(chaine)

chaine.lower()# permet de passer en minuscule un texte sans modifier la variable
print(chaine.lower())
print(chaine) # on voit que la variable ne change pas

chaine.upper() # permet de passer en majuscule un texte sans modifier la variable
print(chaine.upper())

chaine = str() # permet d'écrire un espace vide afin de juste déclarer une variable str
print(chaine)

chaine = "  NE CRIE PAS SI FORT ! EE "

chaine.strip() # permet de retirer les espaces avant et après le texte de la variable
print(chaine.strip())

chaine.center(2) # permet de centrer un texte d'une variable(possible de définir le nombre total de caractères
print(chaine.center(30).lower())

chaine  = "mignon coquin"

chaine.capitalize() # permet d'ajouter une majuscule à la première lettre
print(chaine.capitalize())




"""méthode de formatage numéro 1"""


nom = "bois"
prenom = "jeremy"
age = 22

# permet d'intégrer des variables simplement et de les modifier avant de les "print"
print("je suis le petit {0} {1} et j'ai déja plus de {2} !!!".format(prenom.capitalize(), nom.upper(), age))





"""méthode de formatage numéro 2"""

# formatage d'une adresse
adresse = """\r
    {no_rue}, {nom_rue} {appt}\r
    {postal} {ville} ({pays})"""\
    .format(no_rue = 9, nom_rue = "allée de la misaine", appt = "appt C103", postal = 17000, ville = "LA ROCHELLE", pays = "FRANCE")
print(adresse)





"""concaténer des variables entre elles (assembler)"""

assemblage = " j'ai " + str(age) + " et je me nomme " + prenom + " " + nom # on ajoute différentes variables entre elles grâce à l'opérateur +
print(assemblage)





"""méthode pour parcourir des "str" """      

parcour = "Bonjour les enfants, je suis patafouin"
parcour[0] # recherche le premier caractère de la chaine de caractères "parcour"

print(parcour[3])
print(parcour[0])
print(parcour[8])
print(parcour[19])

len(parcour) # affiche la longueur de la chaine
print(len(parcour))


# méthode parcourant toute la chaine de la variable (jusqu'à i)
i = 0
while i < len(parcour): # si on incrémente pas on risque de voir apparaître une erreur du type : "IndexError"
    print(parcour[i])
    i += 1



"""selection de chaine de caractères dans une chaine"""

test = "hello"
print(test[0:2]) # on selectionne les 2 premiers caractères et on les affiche (print)
print(test[2:len(test)]) # on selectionne les caractères depuis le 3 ème jusqu'au dernier

# il est possible de sous-entendre des infos sans pour autant qu'il comprenne rien
print(test[:2])
print(test[2:])

test = test + test[2:] # on ajoute à la chaine de caractère de test les caractères ( 3ème à la fin)
print(test)




"""méthode de recherche"""


phrase = "leE chasseur est parti mais où ? "

print(phrase.count("e", 0, 10)) # compte le nombre de fois que le caractère voulu est utilisé (distingue maj de mini)dans l'intervalle voulue

print(phrase.replace("e", "r", 2)) # remplace un caractère par un autre pour un nombre de fois voulu (ici 2)

print(phrase.find("par", 0, 20)) # trouve et donne le numéro du caractère (début si on recherche une chaine) dans une intervalle voulue
print(phrase.find("par", 20)) # on remarque qu'il renvoi "-1" si il trouve rien


os.system("pause")



