# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'NewUI-3.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from  PyQt5.QtWidgets import QFileDialog, QPushButton, QApplication, QMainWindow, QLabel
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


list = []
track_array = np.empty([20, 20])
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 593)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QtCore.QSize(1080, 1920))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Waveform_Tools = QtWidgets.QTableWidget(self.centralwidget)
        self.Waveform_Tools.setGeometry(QtCore.QRect(0, 0, 131, 271))
        self.Waveform_Tools.setObjectName("Waveform_Tools")
        self.Waveform_Tools.setColumnCount(1)
        self.Waveform_Tools.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.Waveform_Tools.setHorizontalHeaderItem(0, item)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(130, 0, 531, 271))
        self.tableWidget.setObjectName("Waveform-Viewer-Pane")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()

        #Horizontal Layout
        #self.horizontalLayout = QtWidgets.QHBoxLayout(self.tableWidget)
        #self.horizontalLayout.setObjectName("horizontal layout")

        #Create Canvas
        #self.figure = plt.figure()
        #self.canvas = FigureCanvasQTAgg(self.figure)
        ###End Canvas

        #Add Canvas
        #self.horizontalLayout.addWidget(self.canvas)
        #End Horizontal Layout

        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(0, 0, 801, 451))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.widget = QtWidgets.QWidget(self.gridLayoutWidget)
        self.widget.setMaximumSize(QtCore.QSize(1080, 16777215))
        self.widget.setObjectName("widget")
        self.Music_Player_Background = QtWidgets.QWidget(self.widget)
        self.Music_Player_Background.setGeometry(QtCore.QRect(-1, 269, 661, 51))
        self.Music_Player_Background.setObjectName("Music_Player_Background")
        self.Background_Wallpaper = QtWidgets.QLabel(self.Music_Player_Background)
        self.Background_Wallpaper.setGeometry(QtCore.QRect(0, -260, 801, 311))
        self.Background_Wallpaper.setText("")
        self.Background_Wallpaper.setPixmap(QtGui.QPixmap("../../Downloads/plain-black-background.jpg"))
        self.Background_Wallpaper.setObjectName("Background_Wallpaper")
        self.Play_button = QtWidgets.QPushButton(self.Music_Player_Background)
        self.Play_button.setGeometry(QtCore.QRect(10, 20, 50, 32))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../../Downloads/play-button-round-icon.webp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Play_button.setIcon(icon)
        self.Play_button.setObjectName("Play_button")
        self.Pause_button = QtWidgets.QPushButton(self.Music_Player_Background)
        self.Pause_button.setGeometry(QtCore.QRect(70, 20, 50, 32))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../../Downloads/pause-button-icon.webp"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Pause_button.setIcon(icon1)
        self.Pause_button.setObjectName("Pause_button")
        self.Stop_button = QtWidgets.QPushButton(self.Music_Player_Background)
        self.Stop_button.setGeometry(QtCore.QRect(130, 20, 50, 32))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../../Downloads/stop-button-round-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Stop_button.setIcon(icon2)
        self.Stop_button.setObjectName("Stop_button")
        self.Overall_volume = QtWidgets.QSlider(self.Music_Player_Background)
        self.Overall_volume.setGeometry(QtCore.QRect(490, 20, 160, 25))
        self.Overall_volume.setOrientation(QtCore.Qt.Horizontal)
        self.Overall_volume.setObjectName("Overall_volume")
        self.Loop_button = QtWidgets.QPushButton(self.Music_Player_Background)
        self.Loop_button.setGeometry(QtCore.QRect(190, 20, 50, 32))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("../../Downloads/loop.1024x1004.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Loop_button.setIcon(icon3)
        self.Loop_button.setObjectName("Loop_button")
        self.Fast_Forward_button = QtWidgets.QPushButton(self.Music_Player_Background)
        self.Fast_Forward_button.setGeometry(QtCore.QRect(310, 20, 50, 32))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("../../Downloads/Black-Fast-Forward-Button-PNG-Free-Image.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Fast_Forward_button.setIcon(icon4)
        self.Fast_Forward_button.setObjectName("Fast_Forward_button")
        self.Rewind_button = QtWidgets.QPushButton(self.Music_Player_Background)
        self.Rewind_button.setGeometry(QtCore.QRect(250, 20, 50, 32))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("../../Downloads/Black-Rewind-Button-PNG-Free-Image.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Rewind_button.setIcon(icon5)
        self.Rewind_button.setIconSize(QtCore.QSize(30, 23))
        self.Rewind_button.setObjectName("Rewind_button")
        self.gridLayout.addWidget(self.widget, 0, 0, 2, 1)
        self.gridLayoutWidget.raise_()
        self.tableWidget.raise_()
        self.Waveform_Tools.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 24))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSave_file = QtWidgets.QMenu(self.menuFile)
        self.menuSave_file.setObjectName("menuSave_file")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen.triggered.connect(self.clicker)
        self.actionSave_as = QtWidgets.QAction(MainWindow)
        self.actionSave_as.setObjectName("actionSave_as")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.menuSave_file.addAction(self.actionSave_as)
        self.menuSave_file.addAction(self.actionSave)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.menuSave_file.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.Waveform_Tools.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "File Name"))
        item = self.tableWidget.horizontalHeaderItem(0)
        #item.setText(_translate("MainWindow", "New Column"))
        #item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Audio Track Waveform"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuSave_file.setTitle(_translate("MainWindow", "Save file"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.actionOpen.setText(_translate("MainWindow", "Open.."))
        self.actionSave_as.setText(_translate("MainWindow", "Save as"))
        self.actionSave.setText(_translate("MainWindow", "Save"))

    def clicker(self):
        #self.figure.clear()
        fname = QFileDialog.getOpenFileNames(None, "Open File", "", "Wav Files (*.wav)")
        print(fname)

        row = 0

        if fname:
            fname = fname[0]
            self.Waveform_Tools.setRowCount(len(fname))
            self.tableWidget.setRowCount((len(fname)))
            #print(fname)


            #print(len(fname))

            for n in fname[0:]:
                list.append([n])



                Fs, data = wavfile.read(n)
                print(n)
                print(len(data.shape))

                #Read Channel data

                if len(data.shape) == 1:
                    mono_channel = data
                elif len(data.shape) == 2:
                    mono_channel = data[:,0]
                    stereo_channel = data[:,1]

                #Number of sample points
                N = mono_channel.size

                #Sampling interval
                Ts = 1/Fs

                #Timing scale
                t = np.arange(N)*Ts

                #Plotting
                plt.figure(figsize=[12,4])



                if len(data.shape) == 2:
                    plt.subplot(2,1,1) #2 rows, 1 column, first section
                    plt.plot(t, mono_channel)

                    plt.subplot(2, 1, 2)  # 2 rows, 1 column, second section
                    plt.plot(t, stereo_channel)
                    plt.savefig(str(n) + '.png')
                    pic = QtGui.QPixmap(str(n) + '.png')
                    #self.tableWidget.setItemDelegate(0, pic)

                    plt.show()
                    #self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(plt.show()))
                    #self.tableWidget.setItem(n,0, fig)
                    #show = plt.show()
                    #self.figure = plt.show()

                elif len(data.shape) == 1:
                    plt.subplot(1, 1, 1)  # 2 rows, 1 column, first section
                    plt.plot(t, mono_channel)
                    plt.savefig(str(n) + '.png')
                    pic = QtGui.QPixmap(str(n) + '.png')
                    #self.tableWidget.setItemDelegate(0, pic)


                    plt.show()
                    #self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(plt.show()))
                    #show = plt.show()
                    #self.figure = plt.show()
                    #fig = plt.gcf()
                    #self.tableWidget.setItem(n, 0, fig)





                self.Waveform_Tools.setItem(row, 0, QtWidgets.QTableWidgetItem(str(n)))
                row += 1






               #split_words =  re.split(pattern=r"[\"\"\'\']", '', string_of_list)
                #print(list)
                #print(type(list))

                #for i in list:
                    #Fs, data = wavfile.read(n)




        #print(track_array)

                #Fs, data = wavfile.read(str(fname).strip('"[]"'))

            #track_array = np.array(list[0:])
            #print(track_array)
            #res = fname[-1:1]
            #print(type(res))
            #print(res)
            #for i in fname[0:]:
             #   Fs, data = wavfile.read(fname)


        #res = str(fname).strip('[]')
        #print(res[1])

            #for i in res[0:]:
             #   Fs, data = wavfile.read(res)

            #print(data)
        #print(Fs)

            #for i in list[0:]:
                #self.tableView.setItem(row, 0, QtWidgets.QTableWidgetItem(str(list[0:])))
                #row += 1


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())