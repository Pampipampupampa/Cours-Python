# ! /usr/bin/env python
#  -*- coding:Utf8 -*-


"""CRÉATION D'UNE FENÊTRE AVEC <PYSIDE>"""
"DEVELOPPEZ.COM"

#########################################
### Importation fonction et modules : ###
#########################################


# Import minimum obligatoire pour réaliser une application graphique en PySide.
import sys
from PySide.QtGui import *
from PySide.QtCore import *


############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


#  ----- Création des Classes ----- #


# # # # #  CLASSE PRINCIPALE # # # # #


# Création de la classe Frame issue de QWidget.
# Toute application graphique doit contenir au moins une telle classe.
class Frame(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        # Redimensionnement de la fenêtre principale.
        self.resize(600, 500)

        # Application de la police d'écriture Verdana à la fenêtre mais aussi à tous les widgets enfants.
        # À noter que nous aurions aussi pu choisir la taille et la mise en forme (gras, italique...)
        self.setFont(QFont("Verdana"))

        # Titre de la fenêtre
        self.setWindowTitle("Présentation PySide... Présentation des widgets de base")

        # Utilisation d'une icône pour la fenêtre si celui est présent dans le répertoire courant...
        # sinon on passe.
        try:
            self.setWindowIcon(Icon("icon.jpg"))
        except:
            pass

        ####################
        # Création du bouton
        ####################
        self.quit_0 = QPushButton("Quitter", self)

        # Positionnement et dimensionnement du bouton de la forme (x,y,h,l)
        self.quit_0.setGeometry(490, 450, 100, 30)

        # Création d'une connexion entre le widget QPushButton, le signal clicked et le slot quit.
        self.quit_0.clicked.connect(quit)
        # En PyQt cette ligne se serait écrite :
        # self.connect(self.quit_0, QtCore.SIGNAL("clicked()"),QtGui.qApp, QtCore.SLOT("quit()"))

        # Connection à une fonction particulière
        self.btn_0 = QPushButton("Fermer avec confirmation", self)
        self.btn_0.clicked.connect(self.close)
        self.btn_0.move(0, 120)

        # Connexion à une fonction
        self.btn_z = QPushButton("Action 1", self)
        self.btn_z.clicked.connect(self.action1)
        self.btn_z.move(0, 320)

        #####################
        # Création d'un label
        #####################
        self.label = QLabel("<font color=red size=40>Hello World</font>", self)
        self.label.show()

        #Et de récupérer celle-ci
        print(self.label.text())

        #Il est possible de modifier la valeur du QLabel
        self.label.setText(" Nouveau texte ")

        #Et de récupérer celle-ci
        print(self.label.text())

        #À noter que setText() et text() fonctionne pour une grande majorité de widgets Qt.

        ##############################
        # Création d'une zone editable
        ##############################
        self.zoneEdit = QTextEdit("texte de départ", self)
        self.zoneEdit.setGeometry(0, 50, 100, 50)

        ###############################
        # Création d'une ligne éditable
        ###############################
        self.lineedit = QLineEdit("Ceci est un LineEdit", self)
        self.lineedit.move(0, 25)

    #Création d'un slot personnalisé
    def action1(self):
        print(" Activation slot action1 ")
            # À noter que quit est un slot prédéfini et qu'il permet de quitter l'application proprement.
            # Slot est un terme propre à Qt. Certains sont prédéfinis, d'autres seront créés directement par vous.
            # Dans ce cas-là, il s'agira ni plus ni moins que des fonctions que vous avez rencontrées dans votre
            # apprentissage de Python.

    def closeEvent(self, event):
        """Modifier aussi l'action de la croix de fermeture"""
        msg = QMessageBox.question(self, "Info", "Voulez vous vraiment quitter l'application?", QMessageBox.Yes, QMessageBox.No)
        if msg == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

#  ----- Création des Fonctions ----- #


#############################
### Programme principal : ###
#############################


# Les quatre lignes ci-dessous sont impératives pour lancer l'application.
app = QApplication(sys.argv)
#  Ajoute une frame et la montre
frame = Frame()
frame.show()
sys.exit(app.exec_())
