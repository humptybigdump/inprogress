import sys
from PyQt5 import QtCore, QtWidgets, uic

# TODO:

class MyDialog: # TODO:
    pass # TODO:


if __name__ == "__main__":
    # In Spyder kann nur eine Qt-Applikation laufen und sie werden nicht anschliessend geloescht
    if QtCore.QCoreApplication.instance() is not None:
        app = QtCore.QCoreApplication.instance()
    else:
        app = QtWidgets.QApplication(sys.argv)

    dialog = MyDialog()
    dialog.show()
    sys.exit(app.exec_())
    