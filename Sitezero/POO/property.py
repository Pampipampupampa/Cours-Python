#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""CLASSES ET POO"""
"CLASSES SDZ"

#########################################
### Importation fonction et modules : ###
#########################################


############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


# ----- Création des Classes ----- #


class Personne:
    """Classe définissant une personne caractérisée par :
    - son nom ;
    - son prénom ;
    - son âge ;
    - son lieu de résidence"""

    def __init__(self, nom, prenom):
        """Constructeur de notre classe"""
        self.nom = nom
        self.prenom = prenom
        self.age = 33
        self._lieuResidence = "Paris"  # Souligné _ devant le nom

    def _get_lieuResidence(self):
        """Méthode qui sera appelée quand on souhaitera accéder en lecture
        à l'attribut 'lieuResidence' """
        print("On accède à l'attribut lieuResidence !")
        return self._lieuResidence

    def _set_lieuResidence(self, nouvelle_residence):
        """Méthode appelée quand on souhaite modifier le lieu de résidence"""
        print("Attention, il semble que {} déménage à {}.".format(
              self.prenom, nouvelle_residence))
        self._lieuResidence = nouvelle_residence
    # On va dire à Python que notre attribut lieuResidence pointe vers une
    # propriété
    lieuResidence = property(_get_lieuResidence, _set_lieuResidence)

    def __repr__(self):
        """Quand on entre notre objet dans l'interpréteur"""
        return "Personne: nom({}), prénom({}), âge({})".format(
               self.nom, self.prenom, self.age)

    def __str__(self):
        """Méthode permettant d'afficher plus joliment notre objet"""
        return "{} {}, âgé de {} ans".format(
               self.prenom, self.nom, self.age)


class Protege:
    """Classe possédant une méthode particulière d'accès à ses attributs :
    Si l'attribut n'est pas trouvé, on affiche une alerte et renvoie N"""

    def __init__(self):
        """On crée quelques attributs par défaut"""
        self.a = 1
        self.b = 2
        self.c = 3

    def __getattr__(self, nom):
        """Si Python ne trouve pas l'attribut nommé nom, il appelle
        cette méthode. On affiche une alerte"""
        print("Alerte ! Il n'y a pas d'attribut {} ici !".format(nom))
        # On retourne la valeur d'un autre attribut
        return self.b

    def __setattr__(self, nom_attr, val_attr):
        """Méthode appelée quand on fait objet.nom_attr = val_attr.
        On se charge d'enregistrer l'objet"""
        # Ici on renvoie à la méthode setattr de la classe object
        object.__setattr__(self, nom_attr, val_attr+2)

    def __delattr__(self, nom_attr):
        """On ne peut supprimer d'attribut, on lève l'exception
        AttributeError"""
        raise AttributeError("Vous ne pouvez supprimer aucun attribut de cette classe")


##### CLASSE PRINCIPALE #####


#############################
### Programme principal : ###
#############################


# Les propriétés : mutateur et accesseur
if __name__ == '__main__':
    jean = Personne("Micado", "Jean")
    print(jean.nom)
    print(jean.prenom)
    print(jean.age)
    print(jean.lieuResidence)
    jean.lieuResidence = "Berlin"
    print(jean.lieuResidence)


# Les fonctions spéciales : __repr__
# On modifie les informations renseignés lors de l'affichage d'un objet
if __name__ == '__main__':
    print("\n")
    p1 = Personne("Micado", "Jean")
    print(repr(p1))


# Les fonctions spéciales : __str__
if __name__ == '__main__':
    print("\n")
    p1 = Personne("Micado", "Jean")
    print(p1)
    chaine = str(p1)
    print(chaine)


# Les fonctions spéciales : __getattr__
# Permet d'accéder à un attribut ou réaliser une action si python ne trouve pas
# l'attribut recherché
if __name__ == '__main__':
    pro = Protege()
    print(pro.a)
    print(pro.r)


# Les fonctions spéciales : __setattr__
# On modifie la méthode appelée (__setattr__) lorsque on modifie un attribut
if __name__ == '__main__':
    pro.a = 555
    print(pro.a)


# Exemples utilisant les chaines de caractères
"""
objet = MaClasse() # On crée une instance de notre classe
getattr(objet, "nom") # Semblable à objet.nom
setattr(objet, "nom", val) # = objet.nom = val ou objet.__setattr__("nom", val)
delattr(objet, "nom") # = del objet.nom ou objet.__delattr__("nom")
hasattr(objet, "nom") # Renvoie True si l'attribut "nom" existe, False sinon
"""
