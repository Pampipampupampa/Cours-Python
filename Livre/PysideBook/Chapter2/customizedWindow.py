#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""UNE FENÊTRE CUSTOMISÉE AVEC DES ÉLÉMENTS BASIQUES"""
"COURS PYSIDE CHAPITRE 2"

#########################################
### Importation fonction et modules : ###
#########################################


import sys
from PySide.QtGui import *
from PySide.QtCore import Qt


############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


# ----- Création des Classes ----- #


##### CLASSE PRINCIPALE #####

class SampleWindow(QWidget):
    """Création de la fenêtre principale"""
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Fenêtre principale")
        self.setGeometry(300, 300, 200, 150)
        self.setMinimumHeight(100)
        self.setMinimumWidth(250)
        self.setMaximumHeight(200)
        self.setMaximumWidth(800)

    def setIcone(self):
        """Création d'un icone et ajout à la Fenêtre"""
        appIcon = QIcon('Stock/pampaR.jpg')
        self.setWindowIcon(appIcon)

    def quitApp(self):
        """Demande la confirmation à l'utilisateur"""
        userInfo = QMessageBox.question(self, 'Confirmation',
                                        'This will quit the application.\
                                        Do you want to continue?',
                                        QMessageBox.Yes | QMessageBox.No)
        if userInfo == QMessageBox.Yes:
            app.quit()
        if userInfo == QMessageBox.No:
            pass

    def setButton(self):
        """Ajout d'un boutton pour quitter"""
        button = QPushButton('Quitter ?', self)
        button.move(50, 100)
        button.clicked.connect(self.quitApp)

    def centerApp(self):
        """Permet de centrer l'application pour tous les écrans"""
        qRect = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerPoint)
        self.move(qRect.topLeft())

    def setAboutButton(self):
        """Ajout d'un boutton de renseignement sur l'application"""
        self.aboutButton = QPushButton("About", self)
        self.aboutButton.move(150, 100)
        self.aboutButton.clicked.connect(self.showAbout)

    def showAbout(self):
            """Ajout une fenêtre renseignant sur le logiciel"""
            QMessageBox.about(self.aboutButton, "About this application",
                              "Permet juste de comprendre les bases de \
                              Pyside, c'est tout !!")
            # Ajoute un about à propos de Qt
            QMessageBox.aboutQt(self.aboutButton, "test")


# ----- Création des Fonctions ----- #

#############################
### Programme principal : ###
#############################

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        window = SampleWindow()
        window.setIcone()
        window.setButton()
        window.centerApp()
        window.setAboutButton()
        window.show()
        app.exec_()
        sys.exit(0)
    except NameError:
        print("Name Error : ", sys.exc_info()[1])
    except SystemExit:
        print("Closing Window")
    except Exception:
        print("sys.exc_info()[1]")
