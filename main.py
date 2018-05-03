#! /usr/bin/env python
__author__ = 'Daniel Purcell'

import time
from PyQt5 import uic
import random, sys, logging
from pickle import load, dump
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox



class TicTacToe(QMainWindow):
    """The Ticc Tacc Toe game."""

    def __init__(self, parent = None):
        """Setting up the game."""
        logging.info("Game Initiated")
        super().__init__()
        uic.loadUi("tictactoe.ui", self)

        self.result = "Welcome to Tic Tac Toe!"

        try:
            with open("tictactoe.pkl", 'rb') as pickledData:
                self.pickledSelfData = load(pickledData)
                self.user, self.computer, self.wins, self.losses, self.draws = self.pickledSelfData
                self.updateUI()

        except:
            self.user = 'X'
            self.computer = 'O'
            self.wins = 0
            self.losses = 0
            self.draws = 0
        self.logging = True
        self.newGameButton.setEnabled(False)
        self.values = (self.user, self.computer)
        self.corners = [self.button1, self.button3, self.button7, self.button9]
        self.edges = [self.button8, self.button4, self.button6, self.button2]
        self.buttons = [self.button1, self.button2, self.button3, self.button4, self.button5, self.button6, self.button7, self.button8, self.button9]
        self.used = []

        self.settingsButton.clicked.connect(self.showSettings)

        self.button1.clicked.connect(lambda: self.play(self.button1, self.user))
        self.button2.clicked.connect(lambda: self.play(self.button2, self.user))
        self.button3.clicked.connect(lambda: self.play(self.button3, self.user))
        self.button4.clicked.connect(lambda: self.play(self.button4, self.user))
        self.button5.clicked.connect(lambda: self.play(self.button5, self.user))
        self.button6.clicked.connect(lambda: self.play(self.button6, self.user))
        self.button7.clicked.connect(lambda: self.play(self.button7, self.user))
        self.button8.clicked.connect(lambda: self.play(self.button8, self.user))
        self.button9.clicked.connect(lambda: self.play(self.button9, self.user))
        self.newGameButton.clicked.connect(self.restartGame)
        # self.restartButton.clicked.connect(self.restart)

    def closeEvent(self, event):
        quit_msg = "Would you like to save and exit?"
        reply = QMessageBox.question(self, 'Message', quit_msg, QMessageBox.Yes, QMessageBox.No)

        self.pickleInfo = [self.user, self.computer, self.wins, self.losses, self.draws]

        if reply == QMessageBox.Yes:
            event.accept()
            with open("tictactoe.pkl", 'wb') as ticPickle:
                dump(self.pickleInfo, ticPickle)
            exit()
        else:
            event.ignore()

    def changePlayer(self, arg):
        self.user = arg
        if arg == 'O':
            self.computer = "X"
        else:
            self.computer = "O"

    def showSettings(self):
        settings.show()

    def restart(self):
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.resultText = "You have restarted the game!!!!!"
        self.updateUI()
        self.rollingForLabel.setText("RESTART COMPLETE!!")

    def play(self, arg, value):


        self.makeMove(arg, value)
        status = self.checkWinner()
        if status:
            self.strikeOut(status)
            self.result = "You win!"
            self.wins += 1
            self.endGame()
            self.updateUI()
            self.newGameButton.setEnabled(True)
            return

        self.computerLogic()
        status = self.checkWinner()

        if status:
            self.strikeOut(status)
            self.result = "Good luck the next time!"
            self.losses += 1
            self.endGame()
            self.updateUI()
            self.newGameButton.setEnabled(True)
            return

        if self.checkBoard():
            self.result = "You draw!"
            self.draws += 1
            self.updateUI()
            self.endGame()
            self.newGameButton.setEnabled(True)
            return

    def restartGame(self):
        for button in self.buttons:
            button.setEnabled(True)
            button.setText("")
            temp = button.font()
            temp.setStrikeOut(False)
            temp.setBold(False)
            button.setFont(temp)
        self.used = []
        self.newGameButton.setEnabled(False)
        self.result = "Another round of Tic Tac Toe!"
        self.updateUI()

    def updateUI(self):
        self.lossesLabel.setText(str(self.losses))
        self.winsLabel.setText(str(self.wins))
        self.drawsLabel.setText(str(self.draws))
        self.resultsLabel.setText(self.result)

    def checkBoard(self):
        for button in self.buttons:
            if button.isEnabled():
                return False
        return True

    def strikeOut(self, args):
        for arg in args:
            temp = arg.font()
            temp.setStrikeOut(True)
            temp.setBold(True)
            arg.setFont(temp)

    def makeMove(self, arg, value, boolean=True, append=True):
        arg.setText(value)
        if boolean:
            arg.setEnabled(False)
        if append:
            self.used.append(arg)

    def deleteMove(self, arg):
        arg.setText("")
        arg.setEnabled(True)
        if arg in self.used:
            self.used.remove(arg)

    def endGame(self):
        for button in self.buttons:
            button.setEnabled(False)

    def computerLogic(self):
        # First check if computer can be a winner
        for button in self.buttons:
            if button.isEnabled():
                self.makeMove(button, self.computer)
                if self.checkWinner():
                    return
                else:
                    self.deleteMove(button)

        # Second check if player can be a winner
        for button in self.buttons:
            if button.isEnabled():
                self.makeMove(button, self.user)
                if self.checkWinner():
                    self.makeMove(button, self.computer)
                    return
                self.deleteMove(button)

        # Random
        random.shuffle(self.buttons)
        for button in self.buttons:
            if button.isEnabled():
                self.makeMove(button, self.computer)
                return

    def checkWinner(self):
        if self.button1.text() == self.button2.text() == self.button3.text() and self.button1.text() in self.values:
            return self.button1, self.button2, self.button3

        elif self.button4.text() == self.button5.text() == self.button6.text() and self.button4.text() in self.values:
            return self.button4, self.button5, self.button6

        elif self.button7.text() == self.button8.text() == self.button9.text() and self.button7.text() in self.values:
            return self.button7, self.button8, self.button9

        elif self.button1.text() == self.button4.text() == self.button7.text() and self.button1.text() in self.values:
            return self.button1, self.button4, self.button7

        elif self.button2.text() == self.button5.text() == self.button8.text() and self.button2.text() in self.values:
            return self.button2, self.button5, self.button8

        elif self.button3.text() == self.button6.text() == self.button9.text() and self.button3.text() in self.values:
            return self.button3, self.button6, self.button9

        elif self.button1.text() == self.button5.text() == self.button9.text() and self.button1.text() in self.values:
            return self.button1, self.button5, self.button9

        elif self.button7.text() == self.button5.text() == self.button3.text() and self.button7.text() in self.values:
            return self.button7, self.button5, self.button3
        return False

    def checkFull(self):
        for button in self.buttons:
            if button.text() == "":
                return False
        return True

class Settings(QDialog):
    def __init__(self, parent = None):
        """Change preferences"""

        super().__init__()
        uic.loadUi("settings.ui", self)
        self.xRadio.setChecked(True)

        self.oRadio.toggled.connect(lambda: game.changePlayer('O'))
        self.xRadio.toggled.connect(lambda: game.changePlayer('X'))




if __name__== "__main__":
    app = QApplication(sys.argv)
    logger = logging.basicConfig(filename='TicTacToe.log', level=logging.INFO,
                                 format='%(asctime)s %(levelname)s Ln %(lineno)d: %(message)s',
                                 datefmt='%m/%d/%Y %I:%M:%S %p')
    game = TicTacToe()
    settings = Settings()
    game.show()
    sys.exit(app.exec_())