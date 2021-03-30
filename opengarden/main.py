# This Python file uses the following encoding: utf-8
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QDate, QTime,QDateTime,Qt
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel,QComboBox
from PyQt5.QtGui import QPixmap
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
import serial
import time
#import RPi.GPIO as GPIO
import sqlite3
from sqlite3 import Error
from PyQt5.QtWidgets import QMessageBox

relayin1=2
relayin2=3
relayin3=17
relayin4=27

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.title = "OpenGarden"
        self.showFullScreen()
        
        self.setWindowTitle("Watering System")
        self.show()


        #Load the UI Page
        uic.loadUi('mainwindow.ui', self)

        self.InitWindow()

        #self.ser = serial.Serial('/dev/ttyUSB1',9600)



    def InitWindow(self):
        pixmap = QPixmap("home garden.jpg")
        self.groupBoxWateringList.hide()
        self.tableViewStatus.hide()
        self.labelStatus.hide()

        self.btnSchedule.clicked.connect(self.openScheduleWindow)
        self.btnTestSolenoidValve.clicked.connect(self.openSolenoidValveRasp)
        self.btnTestZones.clicked.connect(self.openTestZones)

    def openSolenoidValve(self):
        print("solenoid valve")
        self.getArduinoData()
        time.sleep(1)
        self.sendDataToArduino("open\n")
        time.sleep(10)
        self.sendDataToArduino("close\n")

    def openSolenoidValveRasp(self):
        print("open solenoid valve rasp")


    def setupRasbperry(self):
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(relayin1,GPIO.OUT)
        GPIO.setup(relayin2,GPIO.OUT)

        GPIO.setup(relayin3,GPIO.OUT)
        GPIO.setup(relayin4,GPIO.OUT)

        GPIO.output(relayin1,True)
        GPIO.output(relayin2,True)
        GPIO.output(relayin3,True)
        GPIO.output(relayin4,True)

    def openSolenoidValveRasp(self):
            print("open solenoid valve rasp")
            GPIO.output(relayin1,False)
            GPIO.output(relayin2,False)

            GPIO.output(relayin3,False)
            GPIO.output(relayin4,False)
            time.sleep(120)
            print("close solenoid valve rasp")

            GPIO.output(relayin1,True)
            GPIO.output(relayin2,True)
            GPIO.output(relayin3,True)
            GPIO.output(relayin4,True)


    def starArduino(self):
        print(self.ser)

    def sendDataToArduino(self,dataToSend):
        self.ser = serial.Serial('/dev/ttyUSB1',9600)
        if(self.ser.isOpen()):
            print(dataToSend)
            print (self.ser.portstr)       # check which port was really used
            self.ser.write(dataToSend.encode())      # write a string
            self.ser.close()             # close port


    def getArduinoData(self):
        self.ser = serial.Serial('/dev/ttyUSB1',9600)
        if(self.ser.isOpen()):
            b=self.ser.readline()
            print("b" , b)
            self.ser.close();
#        b.encode('utf-8').strip()
#        string_n=b.decode()
#        string=string_n.rstrip()
#        print(string)


    def openScheduleWindow(self):
        dlg=setupDlg(self)
        dlg.exec()

    def openTestZones(self):
       dlg=setupDlgZones(self)
       dlg.exec()


class setupDlgZones():
        def __init__(self,parent=None):
            super().__init__(parent)
            uic.loadUi('testZones.ui',self)



class setupDlg(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("schedule.ui",self)

        currentDateTime = QDateTime.currentDateTime()
        currentTime=QTime.currentTime()
        self.dateTimeFrom.setDateTime(currentDateTime)
        self.dateTimeTo.setDateTime(currentDateTime)

        self.timeEditFrom.setTime(currentTime)
        self.timeEditTo.setTime(currentTime)

        print("now: "+currentDateTime.toString(Qt.ISODate))


        self.groupBoxList.hide()

        self.dateTimeFrom.dateTimeChanged.connect(lambda: changeDateTimeFrom())
        self.pushButtonSaveSchedule.clicked.connect(self.saveSchedule)

        self.loadZones()


    def loadZones(self):
        self.cmbZones.addItem("ZONE1")
        self.cmbZones.addItem("ZONE2")
        self.cmbZones.addItem("ZONE3")
        self.cmbZones.addItem("ZONE4")
        self.cmbZones.activated[str].connect(self.changeComboBox)

    def changeComboBox(self,text):

        print("changeComboBox "+text)

    def changeDateTimeFrom():
        print("date time from ",self.dateTimeFrom.dateTime())


    def getConnection(self):
        conn=None
        try:
            conn=sqlite3.connect('C://repo//openwatering.db')

        except Error as e:
            print("Couldn't get connection ")
            print(e)

        return conn

    def saveSchedule(self):
        print("save schedule")
        dateTime=QDateTime.currentDateTime()
        print("datetime string ",dateTime.toString())
        time=QTime.currentTime()
        print("time: ",time)
        print ("time to default locale ",time.toString(Qt.DefaultLocaleLongDate))

        now = QDateTime.currentDateTime()
        print("now: "+now.toString(Qt.ISODate))

        print('Universal datetime: ', now.toUTC().toString(Qt.ISODate))

        print(f'The offset from UTC is: {now.offsetFromUtc()} seconds')


        print(f"date from: {str(self.dateTimeFrom.dateTime())}")
        print(f"date to: {self.dateTimeTo.dateTime()}")
        print(f"time from: {self.timeEditFrom.time()}")
        print(f"time to: {self.timeEditTo.time()}")


        print(f'Zone {self.cmbZones.currentText()}')

        date_from=self.dateTimeFrom.dateTime().toString('yyyy-MM-dd')
        time_from =self.timeEditFrom.time().toString()

        date_to=self.dateTimeTo.dateTime().toString('yyyy-MM-dd')
        time_to =self.timeEditTo.time().toString()
        print(f'date_from formatted {date_from}')
        print(f'time_from formatted {time_from}')

        print(f'date_to formatted {date_to}')
        print(f'time_to formatted {time_to}')

        if(self.cmbZones.currentText()=='ZONE1'):
            zone_id=1
        elif (self.cmbZones.currentText()=='ZONE2'):
            zone_id=2
        elif (self.cmbZones.currentText()=='ZONE3'):
            zone_id=3
        elif (self.cmbZones.currentText()=='ZONE4'):
            zone_id=4

        watering_schedule=[(date_from +" " + time_from, date_to+" "+time_to, zone_id, 'pending')]

        conn=self.getConnection()
        c=conn.cursor()

        c.executemany("INSERT INTO watering_schedule(date_from,date_to,zone_id,status) VALUES(?,?,?,?)",watering_schedule)
        conn.commit()

        QMessageBox.about(self, "Success", "The watering was scheduled :D")

    def loadZones(self):
        self.cmbZones.addItem("ZONE1")
        self.cmbZones.addItem("ZONE2")
        self.cmbZones.addItem("ZONE3")
        self.cmbZones.addItem("ZONE4")
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
