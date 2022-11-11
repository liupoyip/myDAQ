import sys
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtCore import Qt, QTimer, QPointF, Slot
from PySide6.QtMultimedia import (QAudioDevice, QAudioFormat,
                                  QAudioSource, QMediaDevices)
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtGui import QPen
import


class WaveChart(QChart):
    def __init__(self, parent=None):
        super().__init__(QChart.ChartTypeCartesian, parent, Qt.WindowFlags())
        self._timer = QTimer()
        #self._series = QSplineSeries(self)
        self.line = QLineSeries(self)
        self.titles = []
        self.x_axis = QValueAxis()
        self.y_axis = QValueAxis()
        color_pen = QPen()
        color_pen.setWidth(1)
        color_pen.setColor(Qt.blue)

        self.addSeries(self.line_series)
        self.addAxis(self.x_axis, Qt.AlignBottom)
        self.addAxis(self.y_axis, Qt.AlignLeft)
        self.line.attachAxis(self.x_axis)
        self.line.attachAxis(self.y_axis)
        self.x_axis.setTickCount
        self.x_axis.setRange(0, 25600)
        self.y_axis.setRange(-1, 1)
        self._timer.start()

    @Slot()
    def handleTimeout(self):
        pass
