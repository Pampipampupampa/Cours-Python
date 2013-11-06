#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""UNE FENÊTRE CUSTOMISÉE AVEC DES ÉLÉMENTS BASIQUES"""
"COURS PYSIDE CHAPITRE 2"

#########################################
### Importation fonction et modules : ###
#########################################


import sys
import time
from PySide.QtGui import QApplication, QMainWindow, QStatusBar, QProgressBar
from PySide.QtGui import QLabel, QTextEdit, QAction, QKeySequence, QIcon
from PySide.QtGui import QMessageBox

############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


# ----- Création des Classes ----- #


##### CLASSE PRINCIPALE #####

class MainWindow(QMainWindow):
    """Fenêtre principale du programme"""
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Main Window")
        self.setGeometry(300, 250, 400, 300)
        self.setWindowIcon(QIcon('Stock/appicon.png'))

    def setupComponent(self):
        """Initialise l'ensemble des éléments de l'application"""
        self.setupStatusBar()
        self.setupZoneText()
        self.setupMenu()
        self.setupToolBar()

    def setupStatusBar(self):
        """Ajoute une barre de status"""
        self.progressBar = QProgressBar()
        self.statusLabel = QLabel('Progression ...')
        self.progressBar.setMaximum(100)
        self.progressBar.setMinimum(0)
        self.statusBar = QStatusBar()
        # # Affiche un message durant 2 sec après ouverture de l'application
        # self.statusBar.showMessage('Please Wait ...', 2000)
        self.progressBar.setValue(10)
        self.statusBar.addWidget(self.statusLabel, 1)
        self.statusBar.addWidget(self.progressBar, 2)
        self.setStatusBar(self.statusBar)

    def setupZoneText(self):
        """Ajout du widget central (zone de texte)"""
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

    def setupMenu(self):
        """Ajout de menus contextuels"""
        self.createActions()
        self.createMenu()
        self.fileMenu.addAction(self.newAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAction)
        self.editMenu.addAction(self.copyAction)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.pasteAction)
        self.helpMenu.addAction(self.aboutAction)

    def setupToolBar(self):
        """Ajout de la barre d'outils"""
        self.mainToolBar = self.addToolBar('Main')
        self.mainToolBar.addAction(self.newAction)
        self.mainToolBar.addSeparator()
        self.mainToolBar.addAction(self.copyAction)
        self.mainToolBar.addAction(self.pasteAction)

    def showProgress(self):
        """Avancement de la barre de progression"""
        while self.progressBar.value() < self.progressBar.maximum():
            self.progressBar.setValue(self.progressBar.value() + 10)
            time.sleep(1/10)
        # self.statusBar.showMessage('Ready', 2000)
        self.statusLabel.setText('Ready !!')

    def createMenu(self):
        """Création de la barre de menu avec 3 menus"""
        self.fileMenu = self.menuBar().addMenu('&Fichier')
        self.editMenu = self.menuBar().addMenu('&Edition')
        self.helpMenu = self.menuBar().addMenu('&About')

    def createActions(self):
        """Création des différentes actions du menu
           '&' permet de surligner une lettre pour acès rapide Alt+lettre
           'shortcut' permet de définir le raccourci de l'action du menu
           'statusTip' permet de modifier l'affichage dans la barre de status
           'triggered' permet de définir l'action à réaliser"""
        self.newAction = QAction('&New', self, shortcut=QKeySequence.New,
                                 statusTip="Créer un nouveau fichier",
                                 triggered=self.newFile)
        self.exitAction = QAction('&Exit', self, shortcut="Ctrl+Q",
                                  statusTip="Quitter l'application",
                                  triggered=self.exitFile)
        self.copyAction = QAction('&Copy', self, shortcut="Ctrl+C",
                                  statusTip="Copier",
                                  triggered=self.textEdit.copy)
        self.pasteAction = QAction('&Paste', self, shortcut="Ctrl+V",
                                   statusTip="Coller",
                                   triggered=self.textEdit.paste)
        self.aboutAction = QAction('&About', self,
                                   statusTip="Infos à propos de l'éditeur",
                                   triggered=self.aboutHelp)

    def newFile(self):
        """Efface le contenu du widget de text"""
        self.textEdit.setText('')

    def exitFile(self):
        """Ferme le programme"""
        self.close()

    def aboutHelp(self):
        """Affiche des renseignements sur le logiciel"""
        QMessageBox.about(self, "About this application",
                          "Just a simple text editor using Menu Bar")


# ----- Création des Fonctions ----- #

#############################
### Programme principal : ###
#############################

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        mainWindow = MainWindow()
        mainWindow.setupComponent()
        mainWindow.show()
        mainWindow.showProgress()
        app.exec_()
        sys.exit(0)
    except NameError:
        print("Name Error : ", sys.exc_info()[1])
    except SystemExit:
        print("Closing Window")
