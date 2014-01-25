#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""LEARN DECORATOR WITH SAM AND MAX"""
"""SAM AND MAX"""

########################################
#### Classes and Methods imported : ####
########################################

from functools import wraps

#####################
#### Constants : ####
#####################

#######################################
#### Classes, Methods, Functions : ####
#######################################


#
# Initiation : décorateur manuel
#
def decorator_tout_neuf(fonction):
    # Englobe la fonction originale
    def wrapper_fonction_origin():
        # Ici on ajoute ce qui doit être réalisé avant la fonction décorée
        print("Eh oui je suis juste avant la fonction")
        # Fonction décoré
        fonction()
        print("Eh oui cette fois je suis après ... Je suis partout")
        # Attention on a juste défini la fonction, on ne l'a en aucun cas appelé
    return wrapper_fonction_origin


def intouchable():
    print("Je suis Dieu, je suis la création, personne ne m'ursupe")


# Ici on décore pythoniquement la fonction
@decorator_tout_neuf
def intouchable2():
    print("Dieu est mort, pouvoir au peuple")


#
# Introspection et décorateur
#
def inutile(func):
    def wrapper():
        func()
    return wrapper


# Le décorateur va détruire les informations permettant d'accéder à la doc
# par exemple (help(fonction) ou fonction.__doc__)
@inutile
def fonction_doc():
    """Super !!!!!!!!"""
    pass


#
# Utilisation du module wraps pour lire la doc d'une fonction
#
def decorator_inutile(func):
    @wraps(func)
    def wrapper():
        # Decorateur inutile^^
        func()
    return wrapper


@decorator_inutile
def ma_fonction():
    """Super doc , super doc, mais tu peux pas la lire"""
    pass


#
# On peut ajouter des arguments aux fonctions décorées
#
def decorateur_argumente(fonc):
    def wrapper_arg(arg1, arg2):
        print("Ben oui j'ai des arguments, normal quoi",
              arg1, arg2)
        fonc(arg1, arg2)
    return wrapper_arg


@decorateur_argumente
def fonction_argumente(nom, prenom):
    print("My name is : {}, {}".format(nom, prenom))


#
# Passer des arguments au décorateur
#
def createur_de_decorateur():

    print("Je fabrique des décorateurs. Je suis éxécuté une seule fois :" +
          "à la création du décorateur 1")

    def mon_decorateur(func):

        print("Je suis un décorateur, je suis éxécuté une seule fois quand" +
              " on décore la fonction 3")

        def wrapper():
            print("Je suis le wrapper autour de la fonction décorée. 5"
                  "Je suis appelé quand on appelle la fonction décorée. "
                  "En tant que wrapper, je retourne le RESULTAT de la fonction décorée.")
            return func()

        print("En tant que décorateur, je retourne le wrapper 4")

        return wrapper

    print("En tant que créateur de décorateur, je retourne un décorateur 2")
    return mon_decorateur


def fonction_decore():
    print("Je suis un joli sapin de Noël")


# On peut maintenant tester avec des arguments
def createur_de_decorateur_avec_arguments(decorator_arg1, decorator_arg2):

    print("Je créé des décorateur et j'accepte des arguments:",
          decorator_arg1, decorator_arg2)

    def mon_decorateur(func):
        print("Je suis un décorateur, vous me passez des arguments:",
              decorator_arg1, decorator_arg2)

        # Ne pas mélanger les arguments du décorateurs et de la fonction !
        def wrapped(function_arg1, function_arg2):
            print(("Je suis le wrapper autour de la fonction décorée.\n"
                  "Je peux accéder à toutes les variables\n"
                  "\t- du décorateur: {0} {1}\n"
                  "\t- de l'appel de la fonction: {2} {3}\n"
                  "Et je les passe ensuite à la fonction décorée"
                  .format(decorator_arg1, decorator_arg2,
                          function_arg1, function_arg2)))
            return func(function_arg1, function_arg2)

        return wrapped

    return mon_decorateur


@createur_de_decorateur_avec_arguments("Leonard", "Sheldon")
def fonction_decoree_avec_arguments(function_arg1, function_arg2):
    print(("Je suis une fonctions décorée, je ne me soucie que de mes " +
           "arguments: {0} {1}".format(function_arg1, function_arg2)))


# Quelques décorateurs
def benchmark(func):
    """
    Un décorateur qui affiche le temps qu'une fonction met à s'éxécuter
    """
    import time

    def wrapper(*args, **kwargs):
        t = time.clock()
        res = func(*args, **kwargs)
        print(func.__name__, time.clock()-t)
        return res
    return wrapper


def logging(func):
    """
    Un décorateur qui log l'activité d'un script.
    (Ok, en vrai ça fait un print, mais ça pourrait logger !)
    """
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        print(func.__name__, args, kwargs)
        return res
    return wrapper


def counter(func):
    """
    Un compter qui compte et affiche le nombre de fonction qu'une fonction
    a été éxécutée
    """
    def wrapper(*args, **kwargs):
        wrapper.count = wrapper.count + 1
        res = func(*args, **kwargs)
        print("{0} a été utilisée: {1}x".format(func.__name__, wrapper.count))
        return res
    wrapper.count = 0
    return wrapper

# Exemple
@counter
@benchmark
@logging
def reverse_string(string):
    return string[::-1]


########################
#### Main Program : ####
########################

# intouchable()
# je_te_decore = decorator_tout_neuf(intouchable)
# je_te_decore()

# # On peut écraser la fonction originale qui aura ainsi la même comportement que
# # la fonction décorée
# intouchable = decorator_tout_neuf(intouchable)
# intouchable()

# intouchable2()

# # Introspection
# # La nouvelle fonction contient maintenant wrapper()
# print(fonction_doc.__doc__, help(fonction_doc))

# # Utilisation du module wraps pour lire la doc de la fonction decorée
# print(ma_fonction.__doc__ + "\n")
# print(help(ma_fonction))


# # Decorateur avec paramètres
# fonction_argumente("Jeremy", "Bois")

# Argument au décorateur
# nouveau_decorateur = createur_de_decorateur()
# print("pause")
# fonction_decore = nouveau_decorateur(fonction_decore)
# print("pause")
# fonction_decore()
# print("pause")
# fonction_decore = createur_de_decorateur()(fonction_decore)()

# On teste avec les arguments
# fonction_decoree_avec_arguments("Marabou", "Bouclier")

# Ordre des décorateurs et décorateurs utiles
# print(reverse_string("Karine alla en Irak"))
# print(reverse_string("Sa nana snob porte de trop bons ananas"))


