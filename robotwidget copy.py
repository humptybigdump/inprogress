from PyQt5 import QtCore, QtGui, QtWidgets


class RobotWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)   
        # generate mouse move events (see below)
        #self.setMouseTracking(True)
        
        
    # event handler
    def mousePressEvent(self, event):
        print("Mouse pressed:", event.button(), event.pos())
        
    
    def mouseReleaseEvent(self, event):
        print("Mouse released:", event.button(), event.pos())
        
        if event.button() == QtCore.Qt.LeftButton:
            print(" -> left button")
        elif  event.button() == QtCore.Qt.RightButton:
            print(" -> right button")
        
        
    def mouseMoveEvent(self, event):
        print("Mouse moved:", event.pos())
        
        if event.buttons() & QtCore.Qt.LeftButton and event.buttons() & QtCore.Qt.RightButton:
            print(" -> left and right button down")
        
    
    def paintEvent(self, event):
        super().paintEvent(event) # let base class paint itself
        
        painter = QtGui.QPainter(self)
        painter.setRenderHints(QtGui.QPainter.Antialiasing) # smooth painting
        
        # draw a circle
        painter.setPen(QtCore.Qt.NoPen) # no boundary
        circle_brush = QtGui.QBrush(QtCore.Qt.red)
        painter.setBrush(circle_brush)
        
        # placement and size relative to window size
        M = [self.width() / 4, self.height() / 4]
        r = min(self.width(), self.height()) / 4
        rect = QtCore.QRectF(M[0]-r, M[1]-r, 2*r, 2*r)
        
        painter.drawEllipse(rect)
        
        
        # draw some lines
        line_pen = QtGui.QPen(QtCore.Qt.black)
        line_pen.setCapStyle(QtCore.Qt.RoundCap) # nice line endings
        line_pen.setWidth(1)
        painter.setPen(line_pen)
        
        # use QPainters coordinate transform (optional)
        painter.translate(3 * self.width() / 4, 3 * self.height() / 4)
        painter.rotate(180)
        painter.scale(self.width() / 80, self.height() / 80)
        
        ll, ul = (-10, -10), (-10, 10)
        lr, ur = (10, -10), (10, 10)
        top = (0, 20)
        niko = [ll, ul, top, ur, ul, lr, ll, ur, lr]
        
        for p, q in zip(niko[:-1], niko[1:]):
            painter.drawLine(*p, *q)


if __name__ == "__main__":
    import sys
    # In Spyder kann nur eine Qt-Applikation laufen und sie werden nicht anschliessend geloescht
    if QtCore.QCoreApplication.instance() is not None:
        app = QtCore.QCoreApplication.instance()
    else:
        app = QtWidgets.QApplication(sys.argv)

    rob = RobotWidget()
    rob.resize(800, 600)
    rob.show()
    sys.exit(app.exec_())

    
