# This Python file uses the following encoding: utf-8
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel,QComboBox
from PyQt5.QtGui import QPixmap
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
import serial
import time


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

        self.ser = serial.Serial('/dev/ttyUSB0',9600)

        self.btnTestSolenoidValve.clicked.connect(self.openSolenoidValve)


    def openSolenoidValve(self):
        print("solenoid valve")
        self.getArduinoData()
        self.sendDataToArduino("open")
        time.sleep(3000)
        self.sendDataToArduino("close")


    def InitWindow(self):
        pixmap = QPixmap("home garden.jpg")
        self.btnSchedule.clicked.connect(self.openScheduleWindow)



    def starArduino(self):
        print(self.ser)


    def sendDataToArduino(self,dataToSend):
        print(dataToSend)
        print (self.ser.portstr)       # check which port was really used
        self.ser.write(dataToSend.encode())      # write a string
        #self.ser.close()             # close port


    def getArduinoData(self):
        b=self.ser.readline()
        print("b" , b)
#        b.encode('utf-8').strip()
#        string_n=b.decode()
#        string=string_n.rstrip()
#        print(string)


    def openScheduleWindow(self):
        dlg=setupDlg(self)
        dlg.exec()


class setupDlg(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("schedule.ui",self)


    def loadZones(self):
        self.cmbZones.addItem("ZONE1")
        self.cmbZones.addItem("ZONE2")
        self.cmbZones.addItem("ZONE3")
        self.cmbZones.activated[str].connect(self.changeComboBox)

    def changeComboBox(self,text):
        print("changeComboBox "+text)



def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
        main()
