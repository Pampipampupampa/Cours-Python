#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""GESTION DE LA BASE DE DONNÉES"""
"COURS 16"

#########################################
### Importation fonction et modules : ###
#########################################


import sys
from pg8000 import DBAPI
from dicoApplication import *


############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


# ----- Création des Classes ----- #

class Enregistreur(object):
    """Gère les enregistrements"""
    def __init__(self, bd, table):
        self.bd = bd
        self.table = table
        self.descriptif = Glob.dicoT[table]  # Descriptif des champs

    def entrer(self):
        """Procédure d'entrée d'un enregistrement entier"""
        champs = "("  # Début de la chaine pour les noms de champs
        valeurs = []  # Liste contenant les valeurs correspondantes
        # Demande successive d'une valeur pour chaques champs
        for cha, type, nom, in self.descriptif:
            if type == "k":
                continue
            champs = champs + cha + ","
            val = input("Entrez le champ {:s} : ".format(nom))
            if type == "i":
                val = int(val)
            valeurs.append(val)
        balises = "(" + "%s," * len(valeurs)  # Balise de conversion
        champs = champs[:-1] + ")"    # Suppr virgule et ajout parenthèse
        balises = balises[:-1] + ")"  # Suppr virgule et ajout parenthèse
        req = "INSERT INTO {0:s} {1:s} VALUES {2:s}".\
              format(self.table, champs, balises)
        self.bd.executeReq(req, valeurs)
        ch = input("Continuer ? (o/N)")
        if ch.upper() == "O":
            return 0
        else:
            return 1


##### CLASSE PRINCIPALE #####


class GestionBD(object):
    """Mise en place et interfaçage d'une base de données PostgreSQL"""
    def __init__(self, dbName, user, passwd, host, port=5432):
        "Etablissement de la connection et crétion du curseur"
        try:
            self.baseDonn = DBAPI.connect(host=host, port=port,
                                          database=dbName, user=user,
                                          password=passwd)
        except Exception as err:
            print("La connection avec la base de données a échoué : \n" +
                  "Erreur détectée : {:s}".format(err))
            self.echec = 1
        else:
            self.cursor = self.baseDonn.cursor()
            self.echec = 0

    def creerTables(self, dicTables):
        """Création des tables décrites dans le dictionnaire <dicTables>"""
        for table in dicTables:  # Parcours des clés du dictionnaire
            req = "CREATE TABLE {0:s} (".format(table)
            pk = ""
            for val in dicTables[table]:
                nomChamp = val[0]  # Renseigne le libellé du champ
                typeVal = val[1]  # Renseigne le type de la valeur
                if typeVal == 'i':
                    typeChamp = 'INTEGER'
                elif typeVal == 'k':
                    # Champ de clé primaire
                    typeChamp = 'SERIAL'
                    pk = nomChamp
                else:
                    # <VARCHAR> est un type string avec limitation de caractère
                    # Permet de prendre moins de place
                    typeChamp = 'VARCHAR({:s})'.format(str(typeVal))
                req = req + "{0:s} {1:s}, ".format(nomChamp, typeChamp)
            if pk == '':
                req = req[:-2] + ")"  # On vire l'espace et la virgule
            else:
                req = req + "CONSTRAINT {0:s}_pk PRIMARY KEY({0:s}))".\
                            format(pk, pk)
            self.executeReq(req)

    def supprTable(self, dicTables):
        """Suppression de toutes les tables de <dicTables>"""
        for table in list(dicTables.keys()):
            req = "DROP TABLE {}".format(table)
            self.executeReq(req)
        # self.commit()  # Transfert requête dans base de données --> disque

    def executeReq(self, req, param=None):
        "Exécution de la requête <req> avec détection d'erreur"
        try:
            self.cursor.execute(req, param)
        except Exception as err:
            print("Requête SQL invalide : \n" +
                  "Erreur détectée : {:s}".format(err))
            print(err)
            return 0
        else:
            return 1

    def resultatReq(self):
        """Renvoi le résultat de la requête précédente"""
        return self.cursor.fetchall()

    def commit(self):
        if self.baseDonn:
            self.baseDonn.commit()  # Transfert --> disque

    def close(self):
        if self.baseDonn:
            self.baseDonn.close()


#############################
### Programme principal : ###
#############################

bd = GestionBD(Glob.dbName, Glob.user, Glob.passwd, Glob.host, Glob.port)
if bd.echec:
    sys.exit()

while 1:
    print("\nQue voulez-vous faire :\n" +
          "1) Créer les tables de la base de données\n" +
          "2) Supprimer les tables de la base de données ?\n" +
          "3) Entrer des compositeurs\n" +
          "4) Entrer des oeuvres\n" +
          "5) Lister les compositeurs\n" +
          "6) Lister les oeuvres\n" +
          "7) Exécuter une requête SQL quelconque\n" +
          "9) terminer ?                         Votre choix :", end=' ')
    ch = int(input())
    if ch == 1:
        # création de toutes les tables décrites dans le dictionnaire :
        bd.creerTables(Glob.dicoT)
    elif ch == 2:
        # suppression de toutes les tables décrites dans le dic. :
        bd.supprTable(Glob.dicoT)
    elif ch == 3 or ch == 4:
        # création d'un <enregistreur> de compositeurs ou d'oeuvres :
        table = {3: 'compositeurs', 4: 'oeuvres'}[ch]
        enreg = Enregistreur(bd, table)
        while 1:
            if enreg.entrer():
                break
    elif ch == 5 or ch == 6:
        # listage de tous les compositeurs, ou toutes les oeuvres :
        table = {5: 'compositeurs', 6: 'oeuvres'}[ch]
        if bd.executeReq("SELECT * FROM {}".format(table)):
            # analyser le résultat de la requête ci-dessus :
            records = bd.resultatReq()      # ce sera un tuple de tuples
            for rec in records:             # => chaque enregistrement
                for item in rec:            # => chaque champ dans l'enreg.
                    print(item, end=' ')
                print()
    elif ch == 7:
        req = input("Entrez la requête SQL : ")
        if bd.executeReq(req):
            print(bd.resultatReq())          # ce sera un tuple de tuples
    else:
        bd.commit()
        bd.close()
        break
