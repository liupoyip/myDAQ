import sys
import numpy as np
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QSplineSeries
from PySide6.QtCore import QPointF, Slot, Qt
from PySide6.QtMultimedia import (QAudioDevice, QAudioFormat,
                                  QAudioSource, QMediaDevices)
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget, QGraphicsView, QGraphicsScene, QSizePolicy, QRubberBand


class WaveChart(QChart):
    def __init__(self):
        super().__init__()
        self._series = QLineSeries()
        #self._series = QSplineSeries()

        self.addSeries(self._series)

        self._axis_x = QValueAxis()
        self._axis_x.setRange(0, 100)
        # self._axis_x.setLabelFormat("%g")
        # self._axis_x.setTitleText("Samples")
        # self._axis_x.setTitleVisible(False)
        self._axis_x.setGridLineVisible(False)

        self._axis_y = QValueAxis()
        self._axis_y.setRange(-0.05, 0.05)
        # self._axis_y.setTitleText("Audio level")
        # self._axis_y.setTitleVisible(False)
        self._axis_y.setGridLineVisible(True)

        self.addAxis(self._axis_x, Qt.AlignBottom)
        self.addAxis(self._axis_y, Qt.AlignLeft)
        self._series.attachAxis(self._axis_x)
        self._series.attachAxis(self._axis_y)
        self.legend().hide()

        # self.setTitle(f"Data from the microphone ({name})")
        self.setBackgroundRoundness(0)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.chart_view = QChartView()
        self.chart_view.setChart(self)
        self._x = np.linspace(0, 100, 1024)
        self._y = np.zeros(1024)
        self._buffer = [QPointF(x, y) for x, y in zip(self._x, self._y)]
        self._series.append(self._buffer)

    def reset_axis(self, end_time, buffer_len):
        self._axis_x.setRange(0, end_time)
        self._x = np.linspace(0, end_time, buffer_len)
        self._y = np.zeros(buffer_len)
        self._buffer = [QPointF(x, y) for x, y in zip(self._x, self._y)]
        self._series.replace(self._buffer)

    def set_y(self, y_line):
        for i in range(y_line.shape[0]):
            self._buffer[i].setY(y_line[i])
        self._series.replace(self._buffer)


if __name__ == "__main__":
    app = QApplication()
    wave_chart = WaveChart()
    wave_chart.chart_view.show()

    app.exec()
