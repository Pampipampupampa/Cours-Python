#! /usr/bin/env python
# -*- coding:Utf8 -*-


"""UN PROGRAMME D'ÉDITION DE TEXTE"""
"COURS PYSIDE CHAPITRE 3"

#########################################
### Importation fonction et modules : ###
#########################################


import sys
import time
from PySide.QtGui import *

############################################################################
### Gestion d'évènements : définition de différentes Fonctions/Classes : ###
############################################################################


# ----- Création des Classes ----- #


##### CLASSE PRINCIPALE #####

class MainWindow(QMainWindow):
    """Fenêtre principale du programme"""
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Pampi Text Editor")
        self.setGeometry(100, 100, 800, 600)
        self.centerApp()
        self.setWindowIcon(QIcon('Stock/appicon.png'))
        self.fileName = None
        self.filters = "Text files (*.txt)"

    def centerApp(self):
        """Permet de centrer l'application pour tous les écrans"""
        qRect = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerPoint)
        self.move(qRect.topLeft())

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
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAction)
        self.editMenu.addAction(self.undoAction)
        self.editMenu.addAction(self.redoAction)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.copyAction)
        self.editMenu.addAction(self.cutAction)
        self.editMenu.addAction(self.pasteAction)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.selectAllAction)
        self.formatMenu.addAction(self.fontAction)
        self.helpMenu.addAction(self.aboutAction)
        self.helpMenu.addAction(self.aboutQtAction)

    def setupToolBar(self):
        """Ajout de la barre d'outils"""
        self.mainToolBar = self.addToolBar('Main')
        self.mainToolBar.addAction(self.newAction)
        self.mainToolBar.addAction(self.openAction)
        self.mainToolBar.addAction(self.saveAction)
        self.mainToolBar.addSeparator()
        self.mainToolBar.addAction(self.copyAction)
        self.mainToolBar.addAction(self.cutAction)
        self.mainToolBar.addAction(self.pasteAction)
        self.mainToolBar.addSeparator()
        self.mainToolBar.addAction(self.undoAction)
        self.mainToolBar.addAction(self.redoAction)

    def showProgress(self):
        """Avancement de la barre de progression"""
        while self.progressBar.value() < self.progressBar.maximum():
            self.progressBar.setValue(self.progressBar.value() + 10)
            time.sleep(1 / 10)
        # self.statusBar.showMessage('Ready', 2000)
        self.statusLabel.setText('Ready !!')

    def createMenu(self):
        """Création de la barre de menu avec 3 menus"""
        self.fileMenu = self.menuBar().addMenu('&Fichier')
        self.editMenu = self.menuBar().addMenu('&Edition')
        self.formatMenu = self.menuBar().addMenu('&Format')
        self.helpMenu = self.menuBar().addMenu('&About')

    def createActions(self):
        """Création des différentes actions du menu
           '&' permet de surligner une lettre pour acès rapide Alt+lettre
           'shortcut' permet de définir le raccourci de l'action du menu
           'statusTip' permet de modifier l'affichage dans la barre de status
           'triggered' permet de définir l'action à réaliser"""
        self.newAction = QAction(QIcon('Stock/new.png'), '&New', self,
                                 shortcut=QKeySequence.New,
                                 statusTip="Créer un nouveau fichier",
                                 triggered=self.newFile)
        self.openAction = QAction(QIcon('Stock/open.png'), '&Open', self,
                                  shortcut=QKeySequence.Open,
                                  statusTip="Ouvrir un fichier existant",
                                  triggered=self.openFile)
        self.exitAction = QAction(QIcon('Stock/exit.png'), '&Exit', self,
                                  shortcut="Ctrl+Q",
                                  statusTip="Quitter l'application",
                                  triggered=self.exitFile)
        self.saveAction = QAction(QIcon('Stock/save.png'), '&Save',
                                  self, shortcut=QKeySequence.Save,
                                  statusTip="Sauvegarde le fichier sur le" +
                                            "disque",
                                  triggered=self.saveFile)
        self.copyAction = QAction(QIcon('Stock/copy.png'), 'Copy', self,
                                  shortcut="Ctrl+C",
                                  statusTip="Copier",
                                  triggered=self.textEdit.copy)
        self.pasteAction = QAction(QIcon('Stock/paste.png'), 'Paste', self,
                                   shortcut="Ctrl+V",
                                   statusTip="Coller",
                                   triggered=self.textEdit.paste)
        self.cutAction = QAction(QIcon('Stock/cut.png'), 'Cut', self,
                                 shortcut=QKeySequence.Cut,
                                 statusTip="Coupe la sélection courante",
                                 triggered=self.textEdit.cut)
        self.selectAllAction = QAction(QIcon('Stock/selectAll.png'),
                                       'Select All', self,
                                       shortcut=QKeySequence.Open,
                                       statusTip="Selection de l'emsemble" +
                                                 "du texte",
                                       triggered=self.textEdit.selectAll)
        self.redoAction = QAction(QIcon('Stock/redo.png'), 'Redo', self,
                                  shortcut=QKeySequence.Redo,
                                  statusTip="Restaure la dernière action",
                                  triggered=self.textEdit.redo)
        self.undoAction = QAction(QIcon('Stock/undo.png'), 'Undo', self,
                                  shortcut=QKeySequence.Undo,
                                  statusTip="Annule la dernière action",
                                  triggered=self.textEdit.undo)
        self.fontAction = QAction('Font', self,
                                  statusTip="Modifier la police",
                                  triggered=self.fontChange)
        self.aboutAction = QAction(QIcon('Stock/about.png'), '&About', self,
                                   statusTip="Infos à propos de l'éditeur",
                                   triggered=self.aboutHelp)
        self.aboutQtAction = QAction("About &Qt", self,
                                     statusTip="Show Qt library's AboutBox",
                                     triggered=qApp.aboutQt)

    def newFile(self):
        """Efface le contenu du widget de text"""
        self.textEdit.setText('')

    def exitFile(self):
        """Ferme le programme"""
        self.close()

    def openFile(self):
        """Ouvre un fichier dans l'éditeur"""
        self.fileName, self.filterName = QFileDialog.getOpenFileName(self)
        self.textEdit.setText(open(self.fileName).read())

    def saveFile(self):
        """Sauvegarde sur le disque dur le fichier"""
        if self.fileName is None or self.fileName == '':
            self.fileName, self.filterName = QFileDialog.getSaveFileName(self,
                                                         filter=self.filters)
        if self.fileName != '':
            with open(self.fileName, 'w') as file_:
                file_.write(self.textEdit.toPlainText())
                self.statusBar.showMessage('Fichier Sauvegardé', 3000)

    def fontChange(self):
        """Modification de style des caractères"""
        (font, valide) = QFontDialog.getFont(QFont("Anonymous Pro", 14),
                                             self)
        if valide:
            self.textEdit.setCurrentFont(font)

    def aboutHelp(self):
        """Affiche des renseignements sur le logiciel"""
        QMessageBox.about(self, "About this application",
                          "Just a simple text editor using Menu Bar")


# ----- Création des Fonctions ----- #

#############################
### Programme principal : ###
############################d#

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        mainWindow = MainWindow()
        mainWindow.setupComponent()
        mainWindow.show()
        mainWindow.showProgress()
        app.exec_()
        sys.exit(0)
    except SystemExit:
        print("Closing Window")
    except Exception:
        print(sys.exc_info()[1])
