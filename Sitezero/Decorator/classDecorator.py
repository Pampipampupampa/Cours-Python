#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""UTILISATION DE DÉCORATEURS POUR HABILLER UNE CLASSE"""
"SDZ : PATTERN-DECORATOR"

#########################################
### Importation fonction et modules : ###
#########################################

from collections import namedtuple

############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


# On ajoute une fonction surchargeant l'opérateur >> qui appel la fonction
# __lshift__ : On modifie la fonction pour que l'interprétation de la chaine
# de commande soit interprétée comme on le veut
# Très utile et puissant
def decorable(classe):
    classe.__lshift__ = lambda objet, fonction: fonction(objet)
    return classe


# ----- Création des Classes ----- #

@decorable
class Sandwich:
    """Classe primaire racine pour les autres"""
    def __init__(self, sauce):
        self.sauce = sauce
        self._ing = dict()

    @property
    def prix(self):
        # Multiplication du prix par la quantité pour chaques ingrédients
        return sum(el.prix * el.qte for el in self._ing.values())

    def __repr__(self):
        """Représentation de l'object"""
        return "Sandwich {0:s}".format(self.sauce)

    def __str__(self):
        """Affichage de l'object"""
        s = repr(self)
        for key, val in self._ing.items():
            s += "\n - {0} {1:<16}{2:>5.2f} €".format(val.qte, key,
                                                      val.prix * val.qte)
        s += "\n TOTAL............... {:.2f} €\n".format(self.prix)
        return s


class Kebab(Sandwich):
    """Sous classe de Sandwich construisant des kebabs"""
    def __init__(self, sauce):
        Sandwich.__init__(self, sauce)  # Ne supporte pas l'héritage multiple
        super().__init__(sauce)  # Supporte l'héritage multiple (préférable)
        self._ing['base'] = Ingredient(prixBase, 1)
        self._ing['salade'] = Ingredient(prixSalade, 1)
        self._ing['tomates'] = Ingredient(prixTomates, 1)
        self._ing['oignons'] = Ingredient(prixOignons, 1)
        self._ing['frites'] = Ingredient(prixFrites, 1)

    def __repr__(self):
        return "Kebab avec sauce {}".format(self.sauce)


class DecoratorSandwich(Sandwich):
    """Encapsule la classe maîtresse"""
    def __init__(self, sandwich):
        super().__init__(sandwich.sauce)
        self.sandwich = sandwich
        self._ing = sandwich._ing


class RetraitIngredient(DecoratorSandwich):
    """Retrait d'un ingrédient de la liste"""
    def __init__(self, sandwich, ingredient):
        super().__init__(sandwich)
        self.retrait = None
        if ingredient in self._ing:
            del self._ing[ingredient]
            self.retrait = ingredient

    def __repr__(self):
        r = repr(self.sandwich)
        if self.retrait is not None:
            r += ", sans {}".format(self.retrait)
        return r


class Supplement(DecoratorSandwich):
    """Ajout de supplément à la commande"""
    def __init__(self, sandwich, ingredient, prix):
        super().__init__(sandwich)
        # utilisation de get pour éviter un KeyError,
        # Attention cependant la nouvelle clé sera insérée quand même
        prix, qte = self._ing.get(ingredient, Ingredient(prix, 0))
        self.ajout = ingredient
        self._ing[ingredient] = Ingredient(prix, qte + 1)

    def __repr__(self):
        r = repr(self.sandwich)
        s = ", supplément {}".format(self.ajout)
        if s not in r:
            r += s
        return r


class ModViande(DecoratorSandwich):
    def __init__(self, sandwich, viande):
        super().__init__(sandwich)
        self.viande = viande
        self.dejaFait = "mod viande" in self._ing
        if not self.dejaFait:
            self._ing["mod viande"] = Ingredient(prixModViande, 1)

    def __repr__(self):
        s = " viande={0}".format(self.viande)
        r = repr(self.sandwich).split(',')
        if not self.dejaFait:
            r.append(s)
        else:
            for idx, elt in enumerate(r):
                if "viande=" in elt:
                    r[idx] = s
                    break
        return ','.join(r)


class ModPain(DecoratorSandwich):
    def __init__(self, sandwich, pain):
        super().__init__(sandwich)
        self.pain = pain
        self.dejaFait = "mod pain" in self._ing
        if not self.dejaFait:
            self._ing["mod pain"] = Ingredient(prixModPain, 1)

    def __repr__(self):
        s = " pain={0}".format(self.pain)
        r = repr(self.sandwich).split(',')
        if not self.dejaFait:
            r.append(s)
        else:
            for idx, elt in enumerate(r):
                if "pain=" in elt:
                    r[idx] = s
                    break
        return ','.join(r)


class Cheeseburger(Sandwich):
    def __init__(self, sauce):
        super().__init__(sauce)
        self._ing['base'] = Ingredient(prixBase, 1)
        self._ing['steak'] = Ingredient(prixSteak, 1)
        self._ing['salade'] = Ingredient(prixSalade, 1)
        self._ing['tomates'] = Ingredient(prixTomates, 1)
        self._ing['oignons'] = Ingredient(prixOignons, 1)
        self._ing['fromage'] = Ingredient(prixFromage, 2)
        self._ing['cornichons'] = Ingredient(prixCornichons, 1)

    def __repr__(self):
        return "Cheeseburger sauce {0}".format(self.sauce)


# ----- Création des Fonctions ----- #

def sansOignons(sandwich):
    return RetraitIngredient(sandwich, 'oignons')


def sansFrites(sandwich):
    return RetraitIngredient(sandwich, 'frites')


def sansSalade(sandwich):
    return RetraitIngredient(sandwich, 'salade')


def sansTomates(sandwich):
    return RetraitIngredient(sandwich, 'tomates')


def suppFromage(sandwich):
    return Supplement(sandwich, 'fromage', prixFromage)


def suppOignons(sandwich):
    return Supplement(sandwich, 'oignons', prixOignons)


def modPoulet(sandwich):
    return ModViande(sandwich, 'poulet')


def modDinde(sandwich):
    return ModViande(sandwich, 'dinde')


def modPita(sandwich):
    return ModPain(sandwich, 'pita')


#############################
### Programme principal : ###
#############################

# Prix des ingrédients
prixBase = 3.8
prixSalade = 0.2
prixTomates = 0.2
prixOignons = 0.3
prixFrites = 0.5
prixFromage = 0.5
prixModViande = 0.2
prixModPain = 0.2
prixSteak = 0.5
prixCornichons = 0.1

# Création du patron pour le remplissage du dictionnaire
Ingredient = namedtuple('Ingredient', 'prix qte')

if __name__ == '__main__':
    # Test Classe maitre
    print(Kebab("piment"))
    # Test Decorateur retrait
    a = Kebab("harissa")
    print(a)
    a = RetraitIngredient(a, "oignons")
    print(a)
    a = sansFrites(sansOignons(sansTomates(Kebab("ketchup"))))
    print(a)
    # Test Decorateur ajout
    a = suppFromage(suppOignons(suppFromage(Kebab("ketchup"))))
    print(a)
    # Test Modulation ingrédient par Décorateur
    a = modDinde(modPita(Kebab("ketchup")))
    print(a)
    # Test ensemble des classes
    a = sansOignons(suppFromage(modPoulet(modPita(Kebab("mayo/harissa")))))
    print(a)

# Avec cette méthode il est possible d'ajouter autant d'ingrédient que l'on
# veut sans toucher aux classes : pratique et propre !!

# On peut aussi dériver de la classe Sandwich un autre type de sandwich
# Voir le Cheeseburger
    a = sansOignons(Cheeseburger('ketchup/mayo'))
    print(a)

# Vérification de la surcharge d'opérateur avec un décorateur statique
    a = Cheeseburger('ketchup/mayo') << sansOignons << suppFromage
    print(a)
