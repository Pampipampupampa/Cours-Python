#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""PENSE BÊTE SUR L'AIDE DISPONIBLE SUR LES MODULES ET FONCTIONS"""
"PENSE BÊTE"

###########################################
#### Importation fonction et modules : ####
###########################################


import math


###############################################################################
#### Gestion d'évènements : définition de différentes fonctions utiliées : ####
###############################################################################


###############################
#### Programme principal : ####
###############################


# Ouvrir l'aide sur le module spécifié entre parenthèses
print(help(math))


# Ouvrir l'aide sur une méthode du module spécifié entre parenthèses
print(help(math.cos))


# Permet d'accéder à la Docstring du module
print(math.__doc__)


# Permet d'accéder à la Docstring de la méthode
# On peut faire de même sur ces propres fonctions
print(math.sin.__doc__)
