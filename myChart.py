import sys
import random

import numpy as np

from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PySide6.QtCore import Qt, QTimer, QPointF, Slot
from PySide6.QtMultimedia import (QAudioDevice, QAudioFormat,
                                  QAudioSource, QMediaDevices)
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtGui import QPen, QPainter

FRAME_SIZE = 12800
chunk = np.zeros(25600)
SAMPLE_COUNT = 1600  # points on chart
DOWNSAMPLE = 8


class WaveChart(QChart):
    def __init__(self, parent=None):
        super().__init__(QChart.ChartTypeCartesian, parent, Qt.WindowFlags())

        self.timer = QTimer()
        # self.series_line = QSplineSeries(self)
        self.series_line = QLineSeries(self)   # series line
        self.titles = []
        self.axis_x = QValueAxis()
        self.axis_y = QValueAxis()
        self.time = 0
        self.value = 1
        self.buffer = [QPointF(x, 0) for x in range(SAMPLE_COUNT)]
        self.series_line.append(self.buffer)

        self.timer.timeout.connect(self.handleTimeout)
        self.timer.setInterval(500)

        color_pen = QPen()
        color_pen.setWidth(1)
        color_pen.setColor(Qt.blue)

        self.addSeries(self.series_line)
        self.addAxis(self.axis_x, Qt.AlignBottom)
        self.addAxis(self.axis_y, Qt.AlignLeft)
        self.series_line.attachAxis(self.axis_x)
        self.series_line.attachAxis(self.axis_y)
        self.axis_x.setLabelFormat('%.1f')
        self.axis_x.setTickCount(5)
        self.axis_y.setTickCount(5)
        #self.axis_x.setRange(0, 500)
        self.axis_y.setRange(-1, 1)
        self.axis_x.setMax(500)
        self.axis_x.setMin(100)
        self.timer.start()  # delete this line after button is completed in the future
        self.value = np.zeros(FRAME_SIZE)

    # TODO: add start button for start_plotting
    # if start_plotting
    #     self.timer.start()

    @Slot()
    def handleTimeout(self):

        self.value = np.random.uniform(low=-1, high=1, size=FRAME_SIZE)
        available_samples = self.value.shape[0]  # // DOWNSAMPLE
        #
        # scroll_dx = self.plotArea().width() / self.axis_x.tickCount()
        # self.scroll(scroll_dx, 0)
        start = 0
        if (available_samples < SAMPLE_COUNT):
            start = SAMPLE_COUNT - available_samples
            for i in range(start):
                self.buffer[i].setY(self.buffer[i + available_samples].y())
        # y = (self.axis_x.max()) - self.axis_x.min()/self.axis_x.tickCount()
        self.time += self.timer.interval() * 0.001

        data_index = 0
        for i in range(start, SAMPLE_COUNT):
            self.buffer[i].setY(self.value[data_index])
            data_index = data_index + DOWNSAMPLE
        #random.uniform(-1, 1)
        #self.series_line.append(self.time, self.value)
        # for i in range(len(self.buffer)):
        # self.series_line.append(self.buffer[i])
        self.series_line.replace(self.buffer)
        #self.scroll(scroll_dx, 0)

        # TODO: add stop function which trigger by buttom leave
        # if stop_plotting_button_beend_press():
        #    self.timer.stop()


if __name__ == "__main__":

    a = QApplication(sys.argv)

    chart = WaveChart()
    chart.setTitle("Dynamic series line chart")
    chart.legend().hide()

    # chart.setAnimationOptions(QChart.AllAnimations)
    chart.setAnimationOptions(QChart.SeriesAnimations)
    # chart.setAnimationOptions(QChart.GridAxisAnimations)

    chart_view = QChartView(chart)
    # chart_view.setRenderHint(QPainter.Antialiasing)
    chart_view.show()
    chart_view.resize(400, 300)
    # window = QMainWindow()
    # window.setCentralWidget(chart_view)
    # window.resize(400, 300)
    # window.show()

    sys.exit(a.exec())
