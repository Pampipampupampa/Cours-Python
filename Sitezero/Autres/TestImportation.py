import os

from ModuleTable import *
# test importation de la fonction table

nb = input(" table à étudier ?  ")
bn = input(" longueur de la table ?  ")

nb,bn = int(nb), int(bn)
table(nb, bn)

os.system("pause")
