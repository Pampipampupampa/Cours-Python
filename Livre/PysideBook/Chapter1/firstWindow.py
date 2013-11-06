#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""UNE PREMIÈRE FENÊTRE TOUTE SIMPLE"""
"COURS PYSIDE CHAPITRE 1"

#########################################
### Importation fonction et modules : ###
#########################################


import sys
from PySide.QtGui import QApplication, QLabel
from PySide.QtCore import Qt



############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


# ----- Création des Classes ----- #


##### CLASSE PRINCIPALE #####


# ----- Création des Fonctions ----- #

#############################
### Programme principal : ###
#############################

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Ajout d'un label et paramétrage de celui-ci
    appLabel = QLabel()
    appLabel.setText("Une petite fenêtre \n Hello World !!!!")
    appLabel.setWindowTitle("Best application ever")
    appLabel.setAlignment(Qt.AlignCenter)
    appLabel.setGeometry(300, 300, 250, 175)
    appLabel.show()
    app.exec_()
    sys.exit()
