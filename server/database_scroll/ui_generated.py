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
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.rightVLayout.addItem(spacerItem)
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
        self.gridLayout.addLayout(self.rightVLayout, 0, 1, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.timeList = QtWidgets.QListWidget(self.centralwidget)
        self.timeList.setMaximumSize(QtCore.QSize(120, 16777215))
        self.timeList.setObjectName("timeList")
        self.verticalLayout_2.addWidget(self.timeList)
        self.sensorList = QtWidgets.QListWidget(self.centralwidget)
        self.sensorList.setMaximumSize(QtCore.QSize(120, 16777215))
        self.sensorList.setObjectName("sensorList")
        self.verticalLayout_2.addWidget(self.sensorList)
        self.refreshButton = QtWidgets.QPushButton(self.centralwidget)
        self.refreshButton.setMaximumSize(QtCore.QSize(120, 16777215))
        self.refreshButton.setObjectName("refreshButton")
        self.verticalLayout_2.addWidget(self.refreshButton)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)
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
        self.backwardMoreButton.setText(_translate("MainWindow", "<<<"))
        self.backwardOneButton.setText(_translate("MainWindow", "<"))
        self.forwardOneButton.setText(_translate("MainWindow", ">"))
        self.forwardMoreButton.setText(_translate("MainWindow", ">>>"))
        self.refreshButton.setText(_translate("MainWindow", "Refresh"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

