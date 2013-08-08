#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""HÉRITAGE DES CLASSES"""
"CLASSES SDZ"

#########################################
### Importation fonction et modules : ###
#########################################


############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


# ----- Création des Classes ----- #


class Personne:
    """Classe représentant une personne"""
    def __init__(self, nom):
        """Constructeur de notre classe"""
        self.nom = nom
        self.prenom = "Martin"

    def __str__(self):
        """Méthode appelée lors d'une conversion de l'objet en chaîne"""
        return "{0} {1}".format(self.prenom, self.nom)


class AgentSpecial(Personne):
    """Classe définissant un agent spécial.
    Elle hérite de la classe Personne"""

    def __init__(self, nom, matricule):
        """Un agent se définit par son nom et son matricule"""
        # On appelle explicitement le constructeur de Personne :
        Personne.__init__(self, nom)
        self.matricule = matricule

    def __str__(self):
        """Méthode appelée lors d'une conversion de l'objet en chaîne"""
        return "Agent {0}, matricule {1}".format(self.nom, self.matricule)


##### CLASSE PRINCIPALE #####


# ----- Création des Fonctions ----- #


#############################
### Programme principal : ###
#############################


# issubclass : vérification de  l'appartenance d'une classe à une autre
print(issubclass(AgentSpecial, Personne))
print(issubclass(Personne, AgentSpecial))

# isinstance : vérification de l'origine d'un objet par rapport à une classe
agent = AgentSpecial("Fisher", "18327-121")
print(isinstance(agent, AgentSpecial))
print(isinstance(agent, Personne))
