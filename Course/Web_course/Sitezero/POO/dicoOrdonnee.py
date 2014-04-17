#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""CRÉATION D'UN DICTIONNAIRE ORDONNÉE"""
"CLASSES SDZ"

#########################################
### Importation fonction et modules : ###
#########################################


############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


# ----- Création des Classes ----- #


##### CLASSE PRINCIPALE #####


class DicoOrdonnee(object):
    """Fonctionne de façon similaire aux dictionnaires de bases mais les informations sont triées à l'intérieur"""
    def __init__(self, defaut={}, **donnees):
        # Ces attributs ne doivent pas être accesible de l'extérieur
        self._cles = []     # Liste contenant l'ensemble des clés
        self._valeurs = []  # Liste contenant les valeurs correspondantes
        if type(defaut) not in (dict, DicoOrdonnee):
            raise TypeError("Un dictionnaire est demandé (ordonnée ou non)")
        # Récupération des donnes d'entrées
        for cles in defaut:
            self[cles] = defaut[cles]
        for cles in donnees:
            self[cles] = donnees[cles]

    def __repr__(self):
        """Surcharge modifiant l'affichage de l'objet"""
        representation = "{"  # Premier caractère affiché
        flag = True  # Permet de sauter l'ajout de la première virgule
        for cle, val in self.items():
            if not flag:
                representation += ", "  # Séparateur de couples clés/valeurs
            else:
                flag = False  # On veut maintenant ajouter une virgule
            representation += repr(cle) + ": " + repr(val)
        representation += "}"
        return representation

    def __str__(self):
        """On renvoit à l'attribut __repr__ afin d'afficher comme on le
        souhaite l'ensemble des couples clés/valeurs"""
        return repr(self)

    def __iter__(self):
        """Méthode de parcours de l'objet. On renvoie l'itérateur des clés"""
        return iter(self._cles)

    def items(self):
        """Renvoie un générateur contenant les couples (cles, valeurs)"""
        for i, cle in enumerate(self._cles):
            valeur = self._valeurs[i]
            yield (cle, valeur)

    def keys(self):
        """Cette méthode renvoie la liste des clés"""
        return self._cles

    def values(self):
        """Cette méthode renvoie la liste des valeurs"""
        return self._valeurs

    def __len__(self):
        """Renvoie la taille du dictionnaire"""
        return len(self._cles)

    def __contains__(self, cle):
        """Renvoie True si la clé est dans la liste des clés, False sinon"""
        return cle in self._cles

    def __getitem__(self, cle):
        """Renvoie la valeur correspondant à la clé si elle existe, lève
        une exception KeyError sinon"""

        if cle not in self._cles:
            raise KeyError(
                "La clé {0} ne se trouve pas dans le dictionnaire".format(cle))
        else:
            indice = self._cles.index(cle)
            return self._valeurs[indice]

    def __setitem__(self, cle, valeur):
        """Méthode spéciale appelée quand on cherche à modifier une clé
        présente dans le dictionnaire. Si la clé n'est pas présente,
        on l'ajoute à la fin du dictionnaire"""

        if cle in self._cles:
            indice = self._cles.index(cle)
            self._valeurs[indice] = valeur
        else:
            self._cles.append(cle)
            self._valeurs.append(valeur)

    def __delitem__(self, cle):
        """Méthode appelée quand on souhaite supprimer une clé"""
        if cle not in self._cles:
            raise KeyError(
                "La clé {0} ne se trouve pas dans le dictionnaire".format(
                cle))
        else:
            indice = self._cles.index(cle)
            del self._cles[indice]
            del self._valeurs[indice]

    def __add__(self, autre_objet):
        """On renvoie un nouveau dictionnaire contenant les deux
        dictionnaires mis bout à bout (d'abord self puis autre_objet)"""

        if type(autre_objet) is not type(self):
            raise TypeError(
                "Impossible de concaténer {0} et {1}".format(
                type(self), type(autre_objet)))
        else:
            nouveau = DicoOrdonnee()

            # On commence par copier self dans le dictionnaire
            for cle, valeur in self.items():
                nouveau[cle] = valeur

            # On copie ensuite autre_objet
            for cle, valeur in autre_objet.items():
                nouveau[cle] = valeur
            return nouveau

    def sort(self):
        """Méthode permettant de trier le dictionnaire en fonction des clés"""
        # On trie les clés
        cles_triees = sorted(self._cles)
        # On crée une liste de valeurs, encore vide
        valeurs = []
        # On parcourt ensuite la liste des clés triées
        for cle in cles_triees:
            valeur = self[cle]
            valeurs.append(valeur)
        # Enfin, on met à jour notre liste de clés et de valeurs
        self._cles = cles_triees
        self._valeurs = valeurs

    # def reverse(self):
    #     """Inversion du dictionnaire"""
    #     # On crée deux listes vides qui contiendront le nouvel ordre des clés
    #     # et valeurs
    #     cles = []
    #     valeurs = []
    #     for cle, valeur in self.items():
    #         # On ajoute les clés et valeurs au début de la liste
    #         cles.insert(0, cle)
    #         valeurs.insert(0, valeur)
    #     # On met ensuite à jour nos listes
    #     self._cles = cles
    #     self._valeurs = valeurs

    def reverse(self):
        """Inversion du dictionnaire par slicing"""
        self._cles = self._cles[::-1]
        self._valeurs = self._valeurs[::-1]

# ----- Création des Fonctions ----- #


#############################
### Programme principal : ###
#############################


if __name__ == '__main__':
    fruits = DicoOrdonnee()
    print(fruits)
    fruits["pomme"] = 52
    fruits["poire"] = 34
    fruits["prune"] = 128
    fruits["melon"] = 15
    print(fruits)
    fruits.sort()
    print(fruits)
    legumes = DicoOrdonnee(carotte=26, haricot=48, tomates=55)
    legumes.sort()
    print(legumes)
    print(len(legumes))
    legumes.reverse()
    fruits = fruits + legumes
    print(fruits)

    del fruits['haricot']
    print('haricot' in fruits)
    print(legumes['haricot'])
    for cle in legumes:
        print(cle)

    print(legumes.keys())
    print(legumes.values())
    for nom, qtt in legumes.items():
        print("{0} ({1})".format(nom, qtt))
