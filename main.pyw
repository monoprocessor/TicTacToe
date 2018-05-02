# ! /usr/bin/env python
__author__ = 'Daniel Purcell'

import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtGui, QtWidgets
from sys import path
from os import path
from PyQt5 import QtGui, uic, QtMultimedia
from time import sleep
from logging import basicConfig, getLogger, DEBUG, INFO, CRITICAL
from pickle import dump, load
from PyQt5.QtCore import pyqtSlot, QSettings, QCoreApplication, Qt, QTimer
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox

logFileNameDefault = "tictactoe.log"

class TicTacToe(QMainWindow):
    """A game of Tic Tac Toe."""
    def __init__(self, parent = None):
        """Build a game with two dice."""

        super().__init__()
        uic.loadUi("TicTacToe.ui", self)

        self.result = "Welcome to Tic Tac Toe!"

        try:
            with open("tictactoe.pkl", 'rb') as pickledData:
                self.pickledSelfData = load(pickledData)
                self.user, self.computer, self.wins, self.losses, self.draws, self.goFirst, = self.pickledSelfData
                self.updateUI()

        except FileNotFoundError:
            self.user = 'X'
            self.computer = 'O'
            self.wins = 0
            self.losses = 0
            self.draws = 0
            self.goFirst = True

        # self.newGameButton.setEnabled(False)
        self.values = (self.user, self.computer)
        self.corners = [self.Block1, self.Block2, self.Block3, self.Block4]
        self.edges = [self.Block5, self.Block6, self.Block7, self.Block8]
        self.buttons = [self.Block1, self.Block2, self.Block3, self.Block4,
                        self.Block5, self.Block6, self.Block7, self.Block8,
                        self.Block9]
        self.used = []

        self.notes = {
            "win": QtMultimedia.QSound("ok.wav"),
            "lose": QtMultimedia.QSound("ok.wav"),
            "circle": QtMultimedia.QSound("ok.wav"),
            "cross": QtMultimedia.QSound("ok.wav")
        }

        self.Block1.clicked.connect(lambda: self.play(self.Block1, self.user))
        self.Block2.clicked.connect(lambda: self.play(self.Block2, self.user))
        self.Block3.clicked.connect(lambda: self.play(self.Block3, self.user))
        self.Block4.clicked.connect(lambda: self.play(self.Block4, self.user))
        self.Block5.clicked.connect(lambda: self.play(self.Block5, self.user))
        self.Block6.clicked.connect(lambda: self.play(self.Block6, self.user))
        self.Block7.clicked.connect(lambda: self.play(self.Block7, self.user))
        self.Block8.clicked.connect(lambda: self.play(self.Block8, self.user))
        self.Block9.clicked.connect(lambda: self.play(self.Block9, self.user))

    def computerLogic(self):
        # First check if computer can be a winner
        for button in self.buttons:
            if button.isEnabled():
                self.makeMove(button, self.computer)

        for button in self.buttons:
            if button.isEnabled():
                self.makeMove(button, self.user)


        if self.Block5.isEnabled():
            self.makeMove(self.Block5, self.computer)
            return


    def play(self, arg, value):
        if self.user == 'O':
            self.notes["circle"].play()
        else:
            self.notes["cross"].play()

        self.makeMove(arg, value)

        self.computerLogic()

    def makeMove(self, arg, value, boolean=True, append=True):
        arg.setText(value)
        if boolean:
            arg.setEnabled(False)
        if append:
            self.used.append(arg)

    def prefButtonClickedHandler(self):
        self.preferencesWindow = PreferenceWindow()
        self.preferencesWindow.show()
        self.preferencesWindow.exec_()



class PreferenceWindow(QDialog):
    """That good pref window."""
    def __init__(self):

        super().__init__()
        uic.loadUi('PreferencesWindow.ui', self)



if __name__ == "__main__":
    appSettings = QSettings()
    startingFolderName = path.dirname(path.realpath(__file__))
    if appSettings.contains('logFile'):
        logFileName = appSettings.value('logFile', type= str)
    else:
        logFileName = logFileNameDefault
        appSettings.setValue('logFile', logFileName)
        basicConfig(filename= path.join(startingFolderName, logFileName), level=INFO, format='%(asctime)s %(name)-8s %(levelName)-8s %(message)s')

    app = QApplication(sys.argv)
    tictactoeApp = TicTacToe()
    # preferencesApp = PreferenceWindow()

    tictactoeApp.show()
    # preferencesApp.show()
    sys.exit(app.exec_())



# prefButton.clicked.connect(lambda: funcion(12))

# all buttons to one event handler
# pass it a different number each time
# use lamda
