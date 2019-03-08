from PyQt5 import QtWidgets
import sys
from ui_generated import Ui_MainWindow
from main import MyUI


app = QtWidgets.QApplication(sys.argv)
MainWindow = MyUI()
ui = Ui_MainWindow()

ui.setupUi(MainWindow)
MainWindow.confirmUI(ui)
MainWindow.add_source('csv', file_name='csv/frame1.csv')
MainWindow.show()
sys.exit(app.exec_())

