import os

from Package.Table.Table import * # Appel les fonctions contenues dans le fichier Table du sous dossier Table 
# test importation de la fonction table

import Package.Table.Table2

nb = input(" table à étudier ?  ")
bn = input(" longueur de la table ?  ")

nb,bn = int(nb), int(bn)

Table(nb, bn)
Package.Table.Table2.Tablee(nb, bn)

os.system("pause")
