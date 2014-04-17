#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""DERRIÈRE LA BOUCLE FOR : ITÉRATEURS ET GÉNÉRATEURS"""
"CLASSES SDZ"

#########################################
### Importation fonction et modules : ###
#########################################


############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


# ----- Création des Classes ----- #


class RevStr(str):
    """Classe reprenant les méthodes et attributs des chaînes construites
    depuis 'str'. On se contente de définir une méthode de parcours
    différente : au lieu de parcourir la chaîne de la première à la dernière
    lettre, on la parcourt de la dernière à la première.

    Les autres méthodes, y compris le constructeur, n'ont pas besoin
    d'être redéfinies"""

    def __iter__(self):
        """Cette méthode renvoie un itérateur parcourant la chaîne
        dans le sens inverse de celui de 'str'"""
        return self  # On renvoie l'itérateur créé pour l'occasion

    def __init__(self, chaine_a_parcourir):
        """On se positionne à la fin de la chaîne"""
        self.chaine_a_parcourir = chaine_a_parcourir
        self.position = len(chaine_a_parcourir)

    def __next__(self):
        """Cette méthode doit renvoyer l'élément suivant dans le parcours,
        ou lever l'exception 'StopIteration' si le parcours est fini"""
        if self.position == 0:  # Fin du parcours
            raise StopIteration
        self.position -= 1  # On décrémente la position
        return self.chaine_a_parcourir[self.position]


##### CLASSE PRINCIPALE #####


# ----- Création des Fonctions ----- #


def generateur():
    """Notre premier générateur. Il va simplement renvoyer 1, 2 et 3"""
    yield 1
    yield 2
    yield 3


def intervalle(deb, fini):
    """Générateur parcourant la série des entiers entre deb et fini.
    Notre générateur doit pouvoir "sauter" une certaine plage de nombres
    en fonction d'une valeur qu'on lui donne pendant le parcours. La
    valeur qu'on lui passe est la nouvelle valeur de deb."""
    if deb > fini:
        while deb > fini:
            deb -= 1
            yield deb
    elif deb < fini:
        while deb < fini:
            deb += 1
            valeurRecue = (yield deb)  # On accepte une information
            if valeurRecue is not None:  # Générateur a reçu quelque chose
                deb = valeurRecue
    else:
        yield "Très drôle le rigolo !!!"


def intervalle1(borne_inf, borne_sup):
    """Générateur parcourant la série des entiers entre borne_inf et borne_sup.
    Notre générateur doit pouvoir "sauter" une certaine plage de nombres
    en fonction d'une valeur qu'on lui donne pendant le parcours. La
    valeur qu'on lui passe est la nouvelle valeur de borne_inf.
    Note: borne_inf doit être inférieure à borne_sup"""
    borne_inf += 1
    while borne_inf < borne_sup:
        valeur_recue = (yield borne_inf)
        if valeur_recue is not None:  # Notre générateur a reçu quelque chose
            borne_inf = valeur_recue
        borne_inf += 1


#############################
### Programme principal : ###
#############################


if __name__ == '__main__':
    # Utilisation de la surcharge pour modifier le comportement de la boucle
    maChaine = RevStr("Bonjour")
    print(maChaine)
    for lettre in maChaine:
        print(lettre)


if __name__ == '__main__':
    # Initiation aux générateurs
    print(generateur)
    print(generateur())
    iterateur = iter(generateur())
    print(next(iterateur))
    print(next(iterateur))
    print(next(iterateur))

    # Même chose que juste au-dessus :
    for nombre in generateur():  # Attention on exécute la fonction
        print(nombre)


if __name__ == '__main__':
    # Création d'un générateur avec pramètres
    for nombre in intervalle(13, 10):
        print(nombre)
    # Stoppper un générateur lors de l'itération
    generateur = intervalle(5, 20)  # Besoin de stocker dans une variable
    for nombre in generateur:
        if nombre > 17:
            generateur.close()  # Interruption de la boucle
        print(nombre, end=" ")
    print("\n")


if __name__ == '__main__':
    generateur2 = intervalle(10, 25)
    for nombre in generateur2:
        if nombre == 15:  # On saute à 20 (petit décalage de 1)
            generateur2.send(19)  # Envoi de la nouvelle valeur de deb
        print(nombre, end=" ")
