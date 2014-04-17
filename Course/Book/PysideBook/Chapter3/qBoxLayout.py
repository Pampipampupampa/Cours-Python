#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""UNE FENÊTRE CUSTOMISÉE AVEC DES ÉLÉMENTS BASIQUES"""
"COURS PYSIDE CHAPITRE 2"

#########################################
### Importation fonction et modules : ###
#########################################


import sys
from PySide.QtGui import (QApplication, QWidget, QPushButton, QHBoxLayout,
                          QVBoxLayout, QGridLayout, QFormLayout, QLabel,
                          QLineEdit)


############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


# ----- Création des Classes ----- #


##### CLASSE PRINCIPALE #####


class MainWindow(QWidget):
    """Main window class"""
    def __init__(self):
        QWidget.__init__(self)
        self.setGeometry(300, 250, 400, 300)

    def setlayoutH(self):
        """Présentation de QHBoxLayout"""
        self.setWindowTitle("Horizontal Layout")
        horizontalLayout = QHBoxLayout(self)
        boutton1 = QPushButton("I'm first", self)
        boutton2 = QPushButton("I'm second", self)
        boutton3 = QPushButton("I'm third", self)
        boutton4 = QPushButton("I'm fourth", self)
        horizontalLayout.addWidget(boutton1)
        horizontalLayout.addSpacing(44)
        horizontalLayout.addWidget(boutton2)
        horizontalLayout.addSpacing(44)
        horizontalLayout.addWidget(boutton3)
        horizontalLayout.addSpacing(44)
        horizontalLayout.addWidget(boutton4)
        self.setLayout(horizontalLayout)

    def setlayoutV(self):
        """Présentation de QVBoxLayout"""
        self.setWindowTitle("Vertical Layout")
        verticalLayout = QVBoxLayout(self)
        boutton1 = QPushButton("I'm first", self)
        boutton2 = QPushButton("I'm second", self)
        boutton3 = QPushButton("I'm third", self)
        boutton4 = QPushButton("I'm fourth", self)
        verticalLayout.addWidget(boutton1)
        verticalLayout.addWidget(boutton2)
        verticalLayout.addStretch()
        verticalLayout.addWidget(boutton3)
        verticalLayout.addWidget(boutton4)
        self.setLayout(verticalLayout)

    def setlayoutGrid(self):
        """Présentation du QGridLayout"""
        self.setWindowTitle("Grid Layout")
        gridLayout = QGridLayout(self)
        boutton1 = QPushButton("I'm first", self)
        boutton2 = QPushButton("I'm second", self)
        boutton3 = QPushButton("I'm third", self)
        boutton4 = QPushButton("I'm fourth", self)
        boutton5 = QPushButton("I'm fifth", self)
        # Positionnement en grille : ligne puis colonne
        gridLayout.addWidget(boutton1, 0, 0)
        gridLayout.addWidget(boutton2, 0, 2)
        gridLayout.addWidget(boutton3, 1, 0)
        gridLayout.addWidget(boutton4, 2, 0)
        gridLayout.addWidget(boutton5, 2, 1)
        self.setLayout(gridLayout)

    def setLayoutForm(self):
        """Présentation du QFormLayout"""
        self.setWindowTitle("Form Layout")
        formLayout = QFormLayout(self)
        labelUser = QLabel("Username")
        txtUser = QLineEdit()
        labelPass = QLabel("Password")
        txtPass = QLineEdit()
        formLayout.addRow(labelUser, txtUser)
        formLayout.addRow(labelPass, txtPass)
        self.setLayout(formLayout)

# ----- Création des Fonctions ----- #

#############################
### Programme principal : ###
#############################

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        mainWindow1 = MainWindow()
        mainWindow1.setlayoutV()
        mainWindow1.show()
        mainWindow2 = MainWindow()
        mainWindow2.setlayoutH()
        mainWindow2.show()
        mainWindow3 = MainWindow()
        mainWindow3.setlayoutGrid()
        mainWindow3.show()
        mainWindow4 = MainWindow()
        mainWindow4.setLayoutForm()
        mainWindow4.show()
        app.exec_()
        sys.exit(0)
    except NameError:
        print("Name Error : ", sys.exc_info()[1])
    except SystemExit:
        print("Closing Window")
