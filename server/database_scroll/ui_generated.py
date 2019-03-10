# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.rightVLayout = QtWidgets.QVBoxLayout()
        self.rightVLayout.setObjectName("rightVLayout")
        self.statHLayout = QtWidgets.QHBoxLayout()
        self.statHLayout.setObjectName("statHLayout")
        self.episodeStatVLayout = QtWidgets.QVBoxLayout()
        self.episodeStatVLayout.setObjectName("episodeStatVLayout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.episodeStatVLayout.addWidget(self.label_2)
        self.frameAmountLabel = QtWidgets.QLabel(self.centralwidget)
        self.frameAmountLabel.setObjectName("frameAmountLabel")
        self.episodeStatVLayout.addWidget(self.frameAmountLabel)
        self.startEpisodeLabel = QtWidgets.QLabel(self.centralwidget)
        self.startEpisodeLabel.setObjectName("startEpisodeLabel")
        self.episodeStatVLayout.addWidget(self.startEpisodeLabel)
        self.endEpisodeLabel = QtWidgets.QLabel(self.centralwidget)
        self.endEpisodeLabel.setObjectName("endEpisodeLabel")
        self.episodeStatVLayout.addWidget(self.endEpisodeLabel)
        self.lengthEpisodeLabel = QtWidgets.QLabel(self.centralwidget)
        self.lengthEpisodeLabel.setObjectName("lengthEpisodeLabel")
        self.episodeStatVLayout.addWidget(self.lengthEpisodeLabel)
        self.sensorEpisodeLabel = QtWidgets.QLabel(self.centralwidget)
        self.sensorEpisodeLabel.setObjectName("sensorEpisodeLabel")
        self.episodeStatVLayout.addWidget(self.sensorEpisodeLabel)
        self.statHLayout.addLayout(self.episodeStatVLayout)
        self.frameStatVLayout = QtWidgets.QVBoxLayout()
        self.frameStatVLayout.setObjectName("frameStatVLayout")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.frameStatVLayout.addWidget(self.label_4)
        self.minLabel = QtWidgets.QLabel(self.centralwidget)
        self.minLabel.setObjectName("minLabel")
        self.frameStatVLayout.addWidget(self.minLabel)
        self.maxLabel = QtWidgets.QLabel(self.centralwidget)
        self.maxLabel.setObjectName("maxLabel")
        self.frameStatVLayout.addWidget(self.maxLabel)
        self.avLabel = QtWidgets.QLabel(self.centralwidget)
        self.avLabel.setObjectName("avLabel")
        self.frameStatVLayout.addWidget(self.avLabel)
        self.frameTimeLabel = QtWidgets.QLabel(self.centralwidget)
        self.frameTimeLabel.setObjectName("frameTimeLabel")
        self.frameStatVLayout.addWidget(self.frameTimeLabel)
        self.statHLayout.addLayout(self.frameStatVLayout)
        self.rightVLayout.addLayout(self.statHLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.backwardMoreButton = QtWidgets.QPushButton(self.centralwidget)
        self.backwardMoreButton.setObjectName("backwardMoreButton")
        self.horizontalLayout.addWidget(self.backwardMoreButton)
        self.backwardOneButton = QtWidgets.QPushButton(self.centralwidget)
        self.backwardOneButton.setObjectName("backwardOneButton")
        self.horizontalLayout.addWidget(self.backwardOneButton)
        self.forwardOneButton = QtWidgets.QPushButton(self.centralwidget)
        self.forwardOneButton.setObjectName("forwardOneButton")
        self.horizontalLayout.addWidget(self.forwardOneButton)
        self.forwardMoreButton = QtWidgets.QPushButton(self.centralwidget)
        self.forwardMoreButton.setObjectName("forwardMoreButton")
        self.horizontalLayout.addWidget(self.forwardMoreButton)
        self.rightVLayout.addLayout(self.horizontalLayout)
        self.timeSlider = QtWidgets.QSlider(self.centralwidget)
        self.timeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.timeSlider.setObjectName("timeSlider")
        self.rightVLayout.addWidget(self.timeSlider)
        self.csvHLayout = QtWidgets.QHBoxLayout()
        self.csvHLayout.setObjectName("csvHLayout")
        self.rightVLayout.addLayout(self.csvHLayout)
        self.gridLayout.addLayout(self.rightVLayout, 0, 1, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.startLabel = QtWidgets.QLabel(self.centralwidget)
        self.startLabel.setObjectName("startLabel")
        self.verticalLayout_2.addWidget(self.startLabel)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.startTimeEdit = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.startTimeEdit.setObjectName("startTimeEdit")
        self.horizontalLayout_2.addWidget(self.startTimeEdit)
        self.ignoreStartCheckbox = QtWidgets.QCheckBox(self.centralwidget)
        self.ignoreStartCheckbox.setText("")
        self.ignoreStartCheckbox.setChecked(True)
        self.ignoreStartCheckbox.setObjectName("ignoreStartCheckbox")
        self.horizontalLayout_2.addWidget(self.ignoreStartCheckbox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.stopLabel = QtWidgets.QLabel(self.centralwidget)
        self.stopLabel.setObjectName("stopLabel")
        self.verticalLayout_2.addWidget(self.stopLabel)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.stopTimeEdit = QtWidgets.QDateTimeEdit(self.centralwidget)
        self.stopTimeEdit.setObjectName("stopTimeEdit")
        self.horizontalLayout_3.addWidget(self.stopTimeEdit)
        self.ignoreStopCheckbox = QtWidgets.QCheckBox(self.centralwidget)
        self.ignoreStopCheckbox.setText("")
        self.ignoreStopCheckbox.setChecked(True)
        self.ignoreStopCheckbox.setObjectName("ignoreStopCheckbox")
        self.horizontalLayout_3.addWidget(self.ignoreStopCheckbox)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.connectLabel = QtWidgets.QLabel(self.centralwidget)
        self.connectLabel.setToolTip("")
        self.connectLabel.setObjectName("connectLabel")
        self.verticalLayout_2.addWidget(self.connectLabel)
        self.connectTimeSpinbox = QtWidgets.QSpinBox(self.centralwidget)
        self.connectTimeSpinbox.setProperty("value", 60)
        self.connectTimeSpinbox.setObjectName("connectTimeSpinbox")
        self.verticalLayout_2.addWidget(self.connectTimeSpinbox)
        self.sliceLabel = QtWidgets.QLabel(self.centralwidget)
        self.sliceLabel.setObjectName("sliceLabel")
        self.verticalLayout_2.addWidget(self.sliceLabel)
        self.sliceTimeSpinbox = QtWidgets.QSpinBox(self.centralwidget)
        self.sliceTimeSpinbox.setObjectName("sliceTimeSpinbox")
        self.verticalLayout_2.addWidget(self.sliceTimeSpinbox)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.frameAmountSpinbox = QtWidgets.QSpinBox(self.centralwidget)
        self.frameAmountSpinbox.setMaximum(9999999)
        self.frameAmountSpinbox.setProperty("value", 1000)
        self.frameAmountSpinbox.setObjectName("frameAmountSpinbox")
        self.verticalLayout_2.addWidget(self.frameAmountSpinbox)
        self.timeList = QtWidgets.QListWidget(self.centralwidget)
        self.timeList.setMaximumSize(QtCore.QSize(120, 16777215))
        self.timeList.setObjectName("timeList")
        self.verticalLayout_2.addWidget(self.timeList)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMinimumSize(QtCore.QSize(50, 50))
        self.frame.setMaximumSize(QtCore.QSize(120, 16777215))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setObjectName("frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.sourcesVLayout = QtWidgets.QVBoxLayout()
        self.sourcesVLayout.setSpacing(0)
        self.sourcesVLayout.setObjectName("sourcesVLayout")
        self.verticalLayout_3.addLayout(self.sourcesVLayout)
        self.verticalLayout_2.addWidget(self.frame)
        self.refreshButton = QtWidgets.QPushButton(self.centralwidget)
        self.refreshButton.setMaximumSize(QtCore.QSize(120, 16777215))
        self.refreshButton.setObjectName("refreshButton")
        self.verticalLayout_2.addWidget(self.refreshButton)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.saveCSVFRAMEButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveCSVFRAMEButton.setObjectName("saveCSVFRAMEButton")
        self.verticalLayout.addWidget(self.saveCSVFRAMEButton)
        self.loadCSVButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadCSVButton.setObjectName("loadCSVButton")
        self.verticalLayout.addWidget(self.loadCSVButton)
        self.saveCSVEPISODEButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveCSVEPISODEButton.setObjectName("saveCSVEPISODEButton")
        self.verticalLayout.addWidget(self.saveCSVEPISODEButton)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_2.setObjectName("frame_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_2)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.visualizeVLayout = QtWidgets.QVBoxLayout()
        self.visualizeVLayout.setObjectName("visualizeVLayout")
        self.verticalLayout_5.addLayout(self.visualizeVLayout)
        self.verticalLayout.addWidget(self.frame_2)
        self.timeCheckBox = QtWidgets.QCheckBox(self.centralwidget)
        self.timeCheckBox.setObjectName("timeCheckBox")
        self.verticalLayout.addWidget(self.timeCheckBox)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.verticalLayout, 0, 2, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_2.setText(_translate("MainWindow", "Episode stats:"))
        self.frameAmountLabel.setText(_translate("MainWindow", "Frames: -"))
        self.startEpisodeLabel.setText(_translate("MainWindow", "Start: -"))
        self.endEpisodeLabel.setText(_translate("MainWindow", "End: -"))
        self.lengthEpisodeLabel.setText(_translate("MainWindow", "Length: -"))
        self.sensorEpisodeLabel.setText(_translate("MainWindow", "Sensors: -"))
        self.label_4.setText(_translate("MainWindow", "Frame stats:"))
        self.minLabel.setText(_translate("MainWindow", "min: -"))
        self.maxLabel.setText(_translate("MainWindow", "max: -"))
        self.avLabel.setText(_translate("MainWindow", "av: -"))
        self.frameTimeLabel.setText(_translate("MainWindow", "Fame time: -"))
        self.backwardMoreButton.setText(_translate("MainWindow", "<<<"))
        self.backwardOneButton.setText(_translate("MainWindow", "<"))
        self.forwardOneButton.setText(_translate("MainWindow", "> "))
        self.forwardMoreButton.setText(_translate("MainWindow", ">>>"))
        self.startLabel.setText(_translate("MainWindow", "Start time"))
        self.startTimeEdit.setDisplayFormat(_translate("MainWindow", "dd/MM/yyyy HH:mm:ss"))
        self.stopLabel.setText(_translate("MainWindow", "Stop time"))
        self.stopTimeEdit.setDisplayFormat(_translate("MainWindow", "dd/MM/yyyy HH:mm:ss"))
        self.connectLabel.setText(_translate("MainWindow", "Connect time (seconds)"))
        self.sliceLabel.setText(_translate("MainWindow", "Slice time (seconds)"))
        self.label.setText(_translate("MainWindow", "Frame amount"))
        self.refreshButton.setText(_translate("MainWindow", "Refresh"))
        self.saveCSVFRAMEButton.setText(_translate("MainWindow", "Save frame CSV"))
        self.loadCSVButton.setText(_translate("MainWindow", "Load CSV"))
        self.saveCSVEPISODEButton.setText(_translate("MainWindow", "Save episode CSV"))
        self.label_3.setText(_translate("MainWindow", "Visualize methods"))
        self.timeCheckBox.setText(_translate("MainWindow", "Time Mode"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

