from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import kinematic_chain


class RobotWidget(QtWidgets.QWidget):
    residualUpdated = QtCore.pyqtSignal(str) # define signal for residual update

    def __init__(self, parent=None):
        super().__init__(parent)
        
        # define relative robot base position
        self.factorX, self.factorY = 0.2, 0.5
        
        N = 5
        arm_elements = (
            [kinematic_chain.ArmElement(90, angle=0, angle_range=(-np.pi/2, np.pi/2))] + 
            [kinematic_chain.ArmElement(90, angle=0) for i in range(N-1)]
            )
        self.chain = kinematic_chain.KinematicChain(arm_elements)
        
        # visual styling
        self._arm_draw_width = 4
        self._arm_draw_color = QtCore.Qt.black
        self._draw_joint_circles = True
        
    def set_relative_home_pos(self, x, y):
        self.factorX, self.factorY = x / self.width(), y / self.height()     
        
    def get_absolute_home_pos(self):
        return np.array([self.width() * self.factorX, 
                         self.height() * self.factorY])
   

    # event handler
    def mousePressEvent(self, event):
        # TODO:
        pass
        
    def mouseMoveEvent(self, event):
        # TODO:
        pass
    
    def paintEvent(self, event):
        super().paintEvent(event) # let base class paint itself
        
        home_pos = self.get_absolute_home_pos()
        
        # calculate joint positions
        positions = [p + home_pos for p in self.chain.get_joint_positions()]
        
        painter = QtGui.QPainter(self)
        painter.setRenderHints(QtGui.QPainter.Antialiasing) # smooth painting
        
        # draw joint circles
        if self._draw_joint_circles:
            r = 20
            painter.setBrush(QtGui.QColor(192, 192, 192))
 
            acc_angle = 0
            for p, angle_range, angle in zip(positions[:-1], self.chain.get_angle_ranges(), self.chain.get_angles()):
                # convert angles from radians to degrees
                angle_start, angle_stop = angle_range * (180 / np.pi)

                # drawPie: full circle equals 5760 (16 * 360)
                start_angle = (angle_start - acc_angle) * 16
                span_angle = (angle_stop - angle_start) * 16
                painter.drawPie(int(p[0]-r), int(p[1]-r), 2*r, 2*r, int(start_angle), int(span_angle))

                acc_angle += angle * (180 / np.pi)
        
        # arm pen
        line_pen = QtGui.QPen(self._arm_draw_color)
        line_pen.setCapStyle(QtCore.Qt.RoundCap) # nice line endings
        line_pen.setWidth(self._arm_draw_width)
        painter.setPen(line_pen)
        
        # draw arm segments
        for start, end in zip(positions[:-1], positions[1:]):
            painter.drawLine(int(start[0]),int(start[1]), int(end[0]),int(end[1]))

        # draw head
        last_segment = (positions[-1] - positions[-2])
        last_segment /= np.linalg.norm(last_segment)
        orthogonal = np.array([-last_segment[1], last_segment[0]]) * 20

        A = positions[-1] - orthogonal
        B = positions[-1] + orthogonal
        painter.drawLine(int(A[0]), int(A[1]), int(B[0]), int(B[1]))

        C = A + last_segment * 20
        painter.drawLine(int(A[0]), int(A[1]), int(C[0]), int(C[1]))
        D = B + last_segment * 20
        painter.drawLine(int(B[0]), int(B[1]), int(D[0]), int(D[1]))

    # interface methods
    def reset_position(self):
        self.chain.set_angles([0]*len(self.chain))
        self.update()
        
    def set_arm_lengths(self, lengths):
        self.chain.set_lengths(lengths)
        self.update()
    
    def set_arm_draw_width(self, width):
        self._arm_draw_width = width
        self.update()
        
    def set_arm_draw_color(self, color):
        self._arm_draw_color = color
        self.update()
        
    def set_joint_circles_visible(self, onoff):
        self._draw_joint_circles = onoff
        self.update()

        
if __name__ == "__main__":
    import sys
    # In Spyder kann nur eine Qt-Applikation laufen und sie werden nicht anschliessend geloescht
    if QtCore.QCoreApplication.instance() is not None:
        app = QtCore.QCoreApplication.instance()
    else:
        app = QtWidgets.QApplication(sys.argv)

    rob = RobotWidget()
    rob.show()
    sys.exit(app.exec_())

    
