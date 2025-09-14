from PyQt5 import uic, QtWidgets, QtCore
import sys


Ui_MainWindow, WindowBaseClass = uic.loadUiType("main_window.ui")
class MyDialog(WindowBaseClass, Ui_MainWindow):
    def __init__(self, parent=None):
        WindowBaseClass.__init__(self, parent)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
    
if __name__ == '__main__':
    # In Spyder kann nur eine Qt-Applikation laufen und sie werden nicht anschliessend geloescht
    if QtCore.QCoreApplication.instance() is not None:
        application = QtCore.QCoreApplication.instance()
    else:
        application = QtWidgets.QApplication(sys.argv)

    dialog = MyDialog()
    dialog.show()
    application.exec_()
