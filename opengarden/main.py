# This Python file uses the following encoding: utf-8
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.title = "OpenGarden"
        self.top = 200
        self.left = 500
        self.width = 400
        self.height = 300



        self.setGeometry(50,50,320,200)
        self.setWindowTitle("Checkbox Example")
        self.show()

        #Load the UI Page
        uic.loadUi('mainwindow.ui', self)

        self.InitWindow()





    def InitWindow(self):
        pixmap = QPixmap("home garden.jpg")





def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
        main()
