from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QSlider
from  PyQt5.QtWidgets import QFileDialog, QPushButton, QApplication, QMainWindow, QLabel
from PyQt5.QtMultimedia import QSound, QMultimedia, QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
import numpy as np
import pyaudio
import struct
import matplotlib.pyplot as plt
import wave
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import struct
from matplotlib import pyplot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from scipy.io import wavfile
from PyQt5.QtGui import QPixmap
import simpleaudio as sa


class Second_Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 561, 241))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tableWidget1 = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.tableWidget1.setObjectName("tableWidget")
        self.tableWidget1.setColumnCount(0)
        self.tableWidget1.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget1)
        self.verticalSlider = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider.setGeometry(QtCore.QRect(0, 240, 22, 91))
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName("verticalSlider")

        #2 lines of code below sets the integer range for the slider
        self.verticalSlider.setMaximum(100)
        self.verticalSlider.setMinimum(0)

        self.verticalSlider.setTickPosition(QSlider.TicksLeft)
        #self.verticalSlider.setTickInterval(10)

        #Below is the code to manually set a value for the slider
        #self.verticalSlider.setValue(20)
        ####Commented out code above for manually setting slider value

        #self.dial = QtWidgets.QDial(self.centralwidget)
        #self.dial.setGeometry(QtCore.QRect(570, 0, 50, 64))
        #self.dial.setObjectName("dial")

        self.verticalSlider_2 = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider_2.setGeometry(QtCore.QRect(40, 240, 22, 91))
        self.verticalSlider_2.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_2.setObjectName("verticalSlider_2")
        self.verticalSlider_2.setMaximum(100)
        self.verticalSlider_2.setMinimum(0)
        self.verticalSlider_2.setTickPosition(QSlider.TicksLeft)


        self.verticalSlider_3 = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider_3.setGeometry(QtCore.QRect(90, 240, 22, 91))
        self.verticalSlider_3.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_3.setObjectName("verticalSlider_3")
        self.verticalSlider_3.setMaximum(100)
        self.verticalSlider_3.setMinimum(0)
        self.verticalSlider_3.setTickPosition(QSlider.TicksLeft)


        self.verticalSlider_4 = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider_4.setGeometry(QtCore.QRect(130, 240, 22, 91))
        self.verticalSlider_4.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_4.setObjectName("verticalSlider_4")
        self.verticalSlider_4.setMaximum(100)
        self.verticalSlider_4.setMinimum(0)
        self.verticalSlider_4.setTickPosition(QSlider.TicksLeft)


        self.verticalSlider_5 = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider_5.setGeometry(QtCore.QRect(0, 340, 22, 91))
        self.verticalSlider_5.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_5.setObjectName("verticalSlider_5")
        self.verticalSlider_5.setMaximum(100)
        self.verticalSlider_5.setMinimum(0)
        self.verticalSlider_5.setTickPosition(QSlider.TicksLeft)


        self.verticalSlider_6 = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider_6.setGeometry(QtCore.QRect(40, 340, 22, 91))
        self.verticalSlider_6.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_6.setObjectName("verticalSlider_6")
        self.verticalSlider_6.setMaximum(100)
        self.verticalSlider_6.setMinimum(0)
        self.verticalSlider_6.setTickPosition(QSlider.TicksLeft)


        self.verticalSlider_7 = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider_7.setGeometry(QtCore.QRect(90, 340, 22, 91))
        self.verticalSlider_7.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_7.setObjectName("verticalSlider_7")
        self.verticalSlider_7.setMaximum(100)
        self.verticalSlider_7.setMinimum(0)
        self.verticalSlider_7.setTickPosition(QSlider.TicksLeft)


        self.verticalSlider_8 = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider_8.setGeometry(QtCore.QRect(130, 340, 22, 91))
        self.verticalSlider_8.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_8.setObjectName("verticalSlider_8")
        self.verticalSlider_8.setMaximum(100)
        self.verticalSlider_8.setMinimum(0)
        self.verticalSlider_8.setTickPosition(QSlider.TicksLeft)


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.menuFile.addAction(self.actionSave)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionSave.setText(_translate("MainWindow", "Save"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Second_Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
