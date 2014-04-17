#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""LES DÉCORATEURS"""
"CLASSES SDZ"

#########################################
### Importation fonction et modules : ###
#########################################


import time


############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


# ----- Création des Classes ----- #


##### CLASSE PRINCIPALE #####


# ----- Création des Fonctions ----- #


def mon_decorateur(fonction):
    """Notre décorateur : il va afficher un message avant l'appel de la
    fonction définie"""

    def fonctionModifiee():
        """Fonction que l'on va renvoyer. Il s'agit en fait d'une version
        un peu modifiée de notre fonction originellement définie. On se
        contente d'afficher un avertissement avant d'exécuter notre fonction
        originellement définie"""

        print("Attention ! On appelle {0}".format(fonction))
        return fonction()
    return fonctionModifiee


@mon_decorateur
def salut():
    print("Salut !")


"""Pour gérer le temps, on importe le module time
On va utiliser surtout la fonction time() de ce module qui renvoie le nombre
de secondes écoulées depuis le premier janvier 1970 (habituellement).
On va s'en servir pour calculer le temps mis par notre fonction pour
s'exécuter"""


def mesureTemps(nbSec):
    """Contrôle le temps mis par une fonction pour s'exécuter.
    Si le temps d'exécution est supérieur à nbSec, on affiche une alerte"""

    def decorateur(fonctionUtilise):
        """Notre décorateur. C'est lui qui est appelé directement LORS
        DE LA DEFINITION de notre fonction (fonctionUtilise)"""

        def fonctionModif(*parametresNonNommes, **parametresNommes):
            """Fonction renvoyée par notre décorateur. Elle se charge
            de calculer le temps mis par la fonction à s'exécuter
            Elle accepte aucun ou plusieurs paramètres nommés ou non"""

            tpsAvant = time.time()  # Avant d'exécuter la fonction
            # On exécute la fonction
            valeurRenvoye = fonctionUtilise(*parametresNonNommes,
                                            **parametresNommes)
            tpsApres = time.time()
            tpsExecution = tpsApres - tpsAvant
            if tpsExecution >= nbSec:
                print("La fonction {0} a mis {1} pour s'exécuter".format(
                      fonctionUtilise, tpsExecution))
            return valeurRenvoye
        return fonctionModif
    return decorateur


@mesureTemps(4)
def attendre():
    input("Appuyez sur Entrée...")


def singleton(classe_definie):
    instances = {}  # Dictionnaire de nos instances singletons

    def getInstance():
        if classe_definie not in instances:
            # On crée notre premier objet de classe_definie
            instances[classe_definie] = classe_definie()
        return instances[classe_definie]
    return getInstance


@singleton
class Test:
    pass


def controleurType(*a_args, **a_kwargs):
    """On attend en paramètres du décorateur les types souhaités. On accepte
    une liste de paramètres indéterminés, étant donné que notre fonction
    définie pourra être appelée avec un nombre variable de paramètres et que
    chacun doit être contrôlé"""

    def decorateur(fonction_a_executer):
        """Notre décorateur. Il doit renvoyer fonction_modifiee"""
        def fonction_modifiee(*args, **kwargs):
            """Notre fonction modifiée. Elle se charge de contrôler
            les types qu'on lui passe en paramètres"""

            # La liste des paramètres attendus (a_args) doit être de même
            # Longueur que celle reçue (args)
            if len(a_args) != len(args):
                raise TypeError("le nombre d'arguments attendu n'est pas égal "
                                "au nombre reçu")
            # On parcourt la liste des arguments reçus et non nommés
            for i, arg in enumerate(args):
                if a_args[i] is not type(args[i]):
                    raise TypeError("l'argument {0} n'est pas du type "
                                    "{1}".format(i, a_args[i]))

            # On parcourt à présent la liste des paramètres reçus et nommés
            for cle in kwargs:
                if cle not in a_kwargs:
                    raise TypeError("l'argument {0} n'a aucun type "
                                    "précisé".format(repr(cle)))
                if a_kwargs[cle] is not type(kwargs[cle]):
                    raise TypeError("l'argument {0} n'est pas de type"
                                    "{1}".format(repr(cle), a_kwargs[cle]))
            return fonction_a_executer(*args, **kwargs)
        return fonction_modifiee
    return decorateur


@controleurType(int, int)
def intervalle(base_inf, base_sup):
    print("Intervalle de {0} à {1}".format(base_inf, base_sup))


#############################
### Programme principal : ###
#############################

salut()
attendre()


# Il est possible de chainer les décorateurs ou bien de les appliquer à des
# classes de façon assez intuitive
# @decorateur1
# @decorateur2
# class Test:
#     pass

a = Test()
b = Test()
print(a is b)


intervalle(1, 8)
intervalle(1, 8.8)
