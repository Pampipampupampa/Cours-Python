#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""PROGRAMME AUTOUR DE L'UTILISATION DES CLASSES"""
"EXERCICE 12.1 ET 12.2 ET 12.3 ET 12.4"

###########################################
#### Importation fonction et modules : ####
###########################################


###############################################################################
#### Gestion d'évènements : définition de différentes Fonctions/Classes : #####
###############################################################################


############# Création des Classes #############


class Domino(object):
    """Définition d'un couple de valeurs sur un domino"""
    def __init__(self, valA=0, valB=0):
        self.faceB = valB
        self.faceA = valA

    def affichePoint(self):
        """Affiche la valeur des 2 faces du domino"""
        print("Face A : {} ----- Face B : {}".format(self.faceA, self.faceB))

    def valeur(self):
        """Ajoute les 2 faces du domino"""
        return self.faceA + self.faceB


class CompteBancaire(object):
    """Gestion de compte bancaire"""
    def __init__(self, client="Dupont", solde=1000):
        self.client = client
        self.solde = solde

    def affiche(self):
        """Obtenir les informations du compte"""
        print("Client : {0} ------ Solde : {1}"
              .format(self.client, self.solde))

    def depot(self, montant):
        """Dépôt d'argent sur le compte"""
        self.solde = self.solde + montant

    def retrait(self, montant):
        """Retrait d'argent du compte"""
        self.solde = self.solde - montant


class Voiture(object):
    """Création de voitures personalisés"""
    def __init__(self, marque="Ford", couleur="vert"):
        self.marque = marque
        self.couleur = couleur
        self.vitesse = 0
        self.pilote = "personne"

    def choixConducteur(self, pilote):
        """Choix du pilote"""
        self.pilote = pilote

    def acceleration(self, taux, duree):
        """Accélère ou ralenti la voiture"""
        if self.pilote != "personne":
            self.vitesse = self.vitesse + taux * duree
            if self.vitesse < 0:
                self.vitesse = 0
        else:
            print("Veuillez en premier lieu définir un nom pour votre pilote")

    def afficheTout(self):
        print("Caractéristiques de la voiture :\n" +
              "Marque = {0}\n".format(self.marque) +
              "Couleur = {0}\n".format(self.couleur) +
              "Pilote = {0}\n".format(self.pilote) +
              "Vitesse = {0} m/s\n".format(self.vitesse))


class Satellite(object):
    """Etude orbitale de satellites"""
    def __init__(self, nom, masse=100, vitesse=0):
        self.nom = nom
        self.masse = masse
        self.vitesse = vitesse

    def afficheVitesse(self):
        """Renvoie les caractéristiques du satellite"""
        print("Nom du satellite : {} ------ Vitesse : {} m/s"
              .format(self.nom, self.vitesse))

    def impulsion(self, force, temps):
        """Modification de la vitesse du satellite"""
        self.vitesse = self.vitesse + (force * temps)/self.masse

    def energie(self):
        """Renvoie la valeur de l'énergie cinétique du satellite"""
        cinetique = (self.masse * self.vitesse**2)/2
        return cinetique


############# Création des Fonctions #############


###############################
#### Programme principal : ####
###############################


# Exercice 12.1 : Réalisation d'une classe avec 2 méthodes
d1 = Domino(3, 4)
d2 = Domino(1, 1)
print(d1.affichePoint(), d1.valeur() + d2.valeur())
# Test Livre :
listeDominos = []
for i in range(7):
    listeDominos.append(Domino(6, i))
vt = 0
for i in range(7):
    listeDominos[i].affichePoint()
    vt = vt + listeDominos[i].valeur()
print("valeur totale des points", vt)
print(listeDominos[3], listeDominos[4])


# Exercice 12.2 : Création d'une classe pour la gestion de comptes bancaires
compte1 = CompteBancaire("Jeremy", 2000)
compte1.affiche()
compte1.retrait(1000)
compte1.affiche()
compte1.depot(500)
compte1.affiche()


# Exercice 12.3 : Constructeur sur les voitures avec restrictions
vehicule1 = Voiture("Mitsubushi", "rouge")
vehicule1.choixConducteur("Nadia")
vehicule1.acceleration(13, 20)
vehicule1.afficheTout()


# Exercice 12.4 : Constructeur sur les satellites
sat = Satellite(nom="Bambi2")
sat.afficheVitesse()
print(sat.energie())
sat.impulsion(800, 20)
print(sat.energie(), sat.afficheVitesse())
