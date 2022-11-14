# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

import random
import sys

from PySide6.QtCharts import QChart, QSplineSeries, QValueAxis, QChartView
from PySide6.QtCore import Qt, QTimer, Slot
from PySide6.QtGui import QPen, QPainter
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget


class Chart(QChart):
    def __init__(self, parent=None):
        super().__init__(QChart.ChartTypeCartesian, parent, Qt.WindowFlags())
        self._timer = QTimer()
        self._series = QSplineSeries(self)
        self._titles = []
        self._axisX = QValueAxis()
        self._axisY = QValueAxis()
        self._step = 0
        self._x = 5
        self._y = 1

        self._timer.timeout.connect(self.handleTimeout)
        self._timer.setInterval(500)

        green = QPen(Qt.red)
        green.setWidth(3)
        self._series.setPen(green)
        self._series.append(self._x, self._y)

        self.addSeries(self._series)
        self.addAxis(self._axisX, Qt.AlignBottom)
        self.addAxis(self._axisY, Qt.AlignLeft)

        self._series.attachAxis(self._axisX)
        self._series.attachAxis(self._axisY)
        self._axisX.setTickCount(5)
        self._axisX.setRange(0, 10)
        self._axisY.setRange(-5, 5)

        self._timer.start()

    @Slot()
    def handleTimeout(self):
        x = self.plotArea().width() / self._axisX.tickCount()
        print(f'Plot area width: {self.plotArea().width()}')
        y = (self._axisX.max() - self._axisX.min()) / self._axisX.tickCount()
        self._x += y
        self._y = random.uniform(-2.5, 2.5)
        self._series.append(self._x, self._y)
        self.scroll(x, 0)
        if self._x == 100:
            self._timer.stop()


if __name__ == "__main__":

    a = QApplication(sys.argv)

    chart = Chart()
    chart.setTitle("Dynamic spline chart")
    # chart.legend().hide()
    chart.setAnimationOptions(QChart.AllAnimations)
    # chart.setAnimationOptions(QChart.SeriesAnimations)
    chart_view = QChartView(chart)
    chart_view.setRenderHint(QPainter.Antialiasing)
    chart_view.show()
    chart_view.resize(400, 300)
    # window = QMainWindow()
    # window.setCentralWidget(chart_view)
    # window.resize(400, 300)
    # window.show()

    sys.exit(a.exec())
