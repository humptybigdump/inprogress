#! /usr/bin/python3.11
## ------------------------------------------------------------------------
# @file     ising.py
# @brief    Python GUI for an Ising model simulation
# @author   Markus Quandt  \n<markus.quandt@uni-tuebingen.de>
## ------------------------------------------------------------------------

import sys 
import time
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QSlider, QPushButton
from PyQt5.QtCore    import Qt, QTimer
from PyQt5.QtGui     import QImage, QPixmap

import ising_module as ising  # Your pybind11-wrapped C++ module

GRID_SIZE = 256
INIT_MODE = True # hot start
FPS = 50  # Target frames per second


class IsingGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ising Model Simulation")
        self.resize(700, 750)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Main vertical layout for the window
        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setSpacing(20)

        # Horizontal layout: canvas on left, vertical slider on right
        canvas_slider_layout = QHBoxLayout()
        canvas_slider_layout.setSpacing(40)
        canvas_slider_layout.setContentsMargins(40, 0, 0, 0)  

        # Canvas (large label displaying the simulation)
        self.canvas_label = QLabel()
        self.canvas_label.setFixedSize(512, 512)
        canvas_slider_layout.addWidget(self.canvas_label)

        # Vertical slider and its label in a vertical layout
        slider_layout = QVBoxLayout()
        slider_layout.setSpacing(10)
        slider_layout.addSpacing(58)
        self.temp_label = QLabel("Temperature: 2.3")
        slider_layout.addWidget(self.temp_label, alignment=Qt.AlignHCenter)

        self.slider = QSlider(Qt.Vertical)
        self.slider.setMinimum(1)
        self.slider.setMaximum(50)
        self.slider.setValue(23)
        self.slider.valueChanged.connect(self.on_temp_change)
        slider_layout.addWidget(self.slider, alignment=Qt.AlignHCenter)
        slider_layout.addStretch()  # Push slider and label to the top

        canvas_slider_layout.addLayout(slider_layout)
        canvas_slider_layout.addSpacing(40)
        main_layout.addLayout(canvas_slider_layout)
        
        # FPS counter and reset button
        self.fps_label = QLabel("FPS: 0")
        self.restart_button = QPushButton("Restart Simulation")
        self.restart_button.clicked.connect(self.restart_simulation)
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()  # Pushes following widgets to the right
        bottom_layout.addWidget(self.fps_label)
        bottom_layout.addSpacing(20)  # Padding between label and button
        bottom_layout.addWidget(self.restart_button)
        bottom_layout.addSpacing(40)  # Padding from the right edge
        main_layout.addLayout(bottom_layout)
        main_layout.addSpacing(40)

        # Simulation state
        self.temperature = 2.0
        self.grid = ising.init_grid(GRID_SIZE, INIT_MODE)

        # FPS tracking variables
        self.frame_count = 0
        self.last_fps_update = time.time()

        # Timer for continuous updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.run_simulation_and_update)
        self.timer.start(int(1000 // FPS))  # 20 ms interval for 50 FPS

        self.update_canvas()

    def on_temp_change(self, value):
        self.temperature = value / 10.0
        self.temp_label.setText(f"Temperature: {self.temperature:.1f}")

    def run_simulation_and_update(self):
        ising.run_ising(self.grid, self.temperature, 1)
        buf = np.zeros((GRID_SIZE, GRID_SIZE, 4), dtype=np.uint8)
        ising.render_grid(self.grid, buf)
        qimg = QImage(buf.data, GRID_SIZE, GRID_SIZE, QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(qimg).scaled(self.canvas_label.width(), self.canvas_label.height(), Qt.KeepAspectRatio)
        self.canvas_label.setPixmap(pixmap)

        # FPS counting
        self.frame_count += 1
        now = time.time()
        if now - self.last_fps_update >= 1.0:
            fps = self.frame_count / (now - self.last_fps_update)
            self.fps_label.setText(f"FPS: {fps:.1f}")
            self.frame_count = 0
            self.last_fps_update = now

    def restart_simulation(self):
        self.grid = ising.init_grid(GRID_SIZE, INIT_MODE)
        self.update_canvas()

    def update_canvas(self):
        self.run_simulation_and_update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IsingGUI()
    window.show()
    sys.exit(app.exec_())

