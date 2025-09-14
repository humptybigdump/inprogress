import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic


Ui_MainWindow, WindowBaseClass = uic.loadUiType("main_window.ui")

class MyDialog(WindowBaseClass, Ui_MainWindow):
    def __init__(self, parent=None):
        WindowBaseClass.__init__(self, parent)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        self.resize(1100, 700)
        self.updateRobot()
        
    def get_arm_sliders(self):
        return [getattr(self, "horizontalSliderArmSize{}".format(i)) for i in range(5)]
        
    def get_arm_color(self):
        item = self.listWidgetArmColors.currentItem()
        if item:
            return item.foreground().color()
        else:
            return QtCore.Qt.black

    def updateRobot(self):
        lengths = [S.value() for S in self.get_arm_sliders()]
        self.widgetRobot.set_arm_lengths(lengths)
        # TODO:

    def resetRobot(self):
        self.widgetRobot.reset_position()
        for S in self.get_arm_sliders():
            S.setValue(90)
        # TODO:


if __name__ == "__main__":    
    # In Spyder kann nur eine Qt-Applikation laufen und sie werden nicht anschliessend geloescht
    if QtCore.QCoreApplication.instance() is not None:
        app = QtCore.QCoreApplication.instance()
    else:
        app = QtWidgets.QApplication(sys.argv)

    dialog = MyDialog()
    dialog.show()
    sys.exit(app.exec_())
    
