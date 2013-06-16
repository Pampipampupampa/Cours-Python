#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""PROGRAMMES SUR LES BASES DE L'UTILISATION DES DICTIONNAIRES ET DES TUPLES"""
"EXERCICE 10.45 ET 10.46 ET 10.47 ET 10.48 ET 10.49"

###########################################
#### Importation fonction et modules : ####
###########################################


from os import chdir


###############################################################################
#### Gestion d'évènements : définition de différentes fonctions utiliées : ####
###############################################################################


def inverse(annuaire):
    """Construit un nouveau dictionnaire en inversant clé \
       et valeur de l'entrée"""
    dicoInverse = {}
    for cle in annuaire:
        element = annuaire[cle]
        dicoInverse[element] = cle
    return dicoInverse


def consultation():
    """Permet de parcourir le dictionnaire"""
    while 1:
        nom = input("Veuillez définir le nom de la personne : ")
        if nom == "":
            break
        if nom in annuaire:
            element = annuaire[nom]
            age, taille = element[0], element[1]
            print("Nom : {} ---- Âge : {} ans ---- Taille : {} mètres".
                  format(nom, age, taille))
        else:
            print("*** Ce nom n'est pas présent !!! ***")


def remplissage():
    """Permet d'ajouter une entrée au dictionnaire"""
    while 1:
        nom = input("Veuillez définir le nom de la personne : ")
        if nom == "":
            break
        age = int(input("Veuillez définir l'age de {} : ".format(nom)))

        taille = float(input("Veuillez définir la taille de {} (en m)(mettre un <.> pour la virgule) : ".format(nom)))

        flag = input("{0} à {1} ans, mesure {2}m\n ".format(nom, age, taille) +
                     "C'est bon? :").lower()

        if flag == "oui" or flag == "yes" or flag == "o" or flag == "y":
            annuaire[nom] = (age, taille)


def enregistrement():
    """Formate et enregistre dans un fichier l'annuaire"""
    fichier = input("Nom du fichier <Cible> : ")
    fc = open(fichier, 'w', encoding="Utf-8")
    fc.write("Mini base de données\n")
    for cle, valeur in list(annuaire.items()):
        fc.write("{0}@{1}#{2}\n".format(cle, valeur[0], valeur[1]))
    fc.close()


def lecture():
    """Ouvre et transmet dans l'annuaire les informations du fichier"""
    fichier = input("Nom du fichier <Source> : ")
    # On verifie que le fichier existe et qu'il est bien encodé
    try:
        fs = open(fichier, 'r', encoding="Utf-8")
    except:
        print("Le fichier n'existe pas, veuillez choisir un fichier existant")
        return
    # On lit la première ligne pour vérifier si on est dans le bon fichier
    ligne1 = fs.readline()
    if ligne1 != "Mini base de données\n":
        print("Le fichier source n'est pas le bon fichier")
        return
    # Si le fichier existe et si c'est le bon fichier alors on récupère
    # les données et on les ajoutes à l'annuaire
    while 1:
        ligne = fs.readline()  # Lecture seconde ligne et suivantes
        if ligne == "":
            break
        enregistrement = ligne.split("@")  # On sépare clé et valeur associée
        cle = enregistrement[0]
        valeur = enregistrement[1][:-1]  # On enlève le "\n" (fin de ligne)
        donnees = valeur.split("#")  # On sépare les valeurs
        age, taille = int(donnees[0]), float(donnees[1])
        annuaire[cle] = (age, taille)
    fs.close()


def sortir():
    """Met fin au programme"""
    print("Fin du programme, merci de votre visite")
    return 1


def autre():
    """Renvoi un message précisant l'action à faire en cas d'erreur"""
    print("Veuillez choisir entre les options suivantes\n" +
          "R, L, Q, C, E")


###############################
#### Programme principal : ####
###############################


# Définition du répertoire courant
chdir("/home/pampi/Documents/Git/Cours-Python/Livre/StructureDonnees-10/" +
      "Sources")


###############################################################################


# Exercice 10.45, 10.50, 10.51 : Création d'une mini base de données
annuaire = {}
ensembleFonction = {"I": lecture, "R": remplissage, "Q": sortir,
                    "C": consultation, "S": enregistrement}
while 1:
    choix = input("Action voulue :\n" +
                  "(C)onsulter la base de données\n" +
                  "(R)emplir la base de donnée\n" +
                  "(I)mporter une base de donnée\n" +
                  "(S)auvegarder dans un fichier la base de donnée\n" +
                  "(Q)uitter l'application\n").upper()
    # () permet de convertir en fonction la chaine récupérée
    if ensembleFonction.get(choix, autre)():  # Retourne la demande de choix
        break


###############################################################################


# Exercice 10.46 : Inverse valeurs et clés dans un dictionnaire
dictionnaire = {"pommes": 430, "bananes": 312, "oranges": 274, "poires": 137}
print(dictionnaire)
print(inverse(dictionnaire))


# Exercice 10.47 : Compte l'occurence des lettres dans un texte
fs = open("texteOccurence", 'r', encoding="Utf-8")
dico1 = {}
while 1:
    texte = fs.readline()
    if texte == "":
        break
    for car in texte:
        car = car.lower()
        dico1[car] = dico1.get(car, 0) + 1
print(dico1)
fs.close()


# Exercice 10.48 : Compte le nombre d'occurence d'un mot
fs = open("texteOccurence", 'r', encoding="Utf-8")
dico2 = {}
# Variable contenant les caractères normaux
normal = "azertyuiopqsdfghjklmwxcvbnéèçàùëêâäîïôöûü"
# On initialise une chaine à construire
chaine = ""
texte = fs.read()  # On ajoute tout le texte du fichier à la variable
fs.close()

# On construit la chaine de caractère en remplaçant tous les caractères
# spéciaux par des espaces
for car in texte:
    car = car.lower()  # Evite de différencier les majuscules des minuscules
    if car in normal:
        chaine = chaine + car  # Ajout élément
    else:
        chaine = chaine + " "  # Remplace élément
liste = chaine.split()  # On sépare les mots qu'on ajoute à une liste

# Ajout dans le dico des mots
for mot in liste:
    dico2[mot] = dico2.get(mot, 0) + 1

# Trie des mots et affichage
liste = list(dico2.items())
liste.sort()
print(liste)


# Exercice 10.49 :
fs = open("texteOccurence", 'r', encoding="Utf-8")
dico3 = {}

# Variable contenant les caractères normaux
normal = "azertyuiopqsdfghjklmwxcvbnéèçàùëêâäîïôöûü"

# On initialise une chaine à construire
chaine = ""
mot = ""

# Création du compteur et de l'indice du 1er caractère du mot
compteur, flag = 0, -1

# On ajoute tout le texte du fichier à la variable
texte = fs.read()
fs.close()

# On construit la chaine de caractère en remplaçant tous les caractères
# spéciaux par des espaces
for car in texte:
    car = car.lower()  # Evite de différencier les majuscules des minuscules
    if car in normal:
        mot = mot + car  # Ajout caractère au mot
        if flag < 0:
            flag = compteur
    else:
        if mot != "":
            if mot in dico3:
                dico3[mot].append(flag)
            else:
                dico3[mot] = [flag]
            # On réinitialise le flag et le mot et on recommence
            mot, flag = "", -1
    compteur += 1
# Affichage
liste = list(dico3.items())
liste.sort()
for cle, valeur in liste:
    print(cle, ' : ', valeur)
