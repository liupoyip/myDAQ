import numpy as np
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QSplineSeries
from PySide6.QtCore import QPointF, Slot, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget, QGraphicsView, QGraphicsScene, QSizePolicy, QRubberBand
from PySide6.QtGui import QPen, QColor


class LineChart(QChart):

    def __init__(self):
        super().__init__()
        self.pen = QPen()
        self.pen.setWidth(1)
        self.pen.setColor(QColor('blue'))
        self._series = QLineSeries()
        self._series.setPen(self.pen)

        self.addSeries(self._series)
        self._axis_x = QValueAxis()
        self._axis_x.setRange(0, 100)
        self._axis_x.setGridLineVisible(False)

        self._axis_y = QValueAxis()
        self._axis_y.setRange(-1, 1)
        self._axis_y.setGridLineVisible(True)

        self.addAxis(self._axis_x, Qt.AlignBottom)
        self.addAxis(self._axis_y, Qt.AlignLeft)
        self._series.attachAxis(self._axis_x)
        self._series.attachAxis(self._axis_y)
        self.legend().hide()

        self.setBackgroundRoundness(10)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.chart_view = QChartView()
        self.chart_view.setChart(self)
        self._x = np.linspace(0, 100, 512)
        self._y = np.zeros(512)
        self._buffer = [QPointF(x, y) for x, y in zip(self._x, self._y)]
        self._series.append(self._buffer)

    def reset_axis(self, end_point, buffer_len):
        self._axis_x.setRange(0, end_point)
        self._x = np.linspace(0, end_point, buffer_len)
        self._y = np.zeros(buffer_len)
        self._buffer = [QPointF(x, y) for x, y in zip(self._x, self._y)]
        self._series.replace(self._buffer)

    def set_y(self, y_line):
        for i in range(y_line.shape[0]):
            self._buffer[i].setY(y_line[i])
        self._series.replace(self._buffer)


class WaveChart(LineChart):
    def __init__(self):
        super(WaveChart, self).__init__()

        self._axis_x.setRange(0, 100)
        # self._axis_x.setLabelFormat("%g")
        # self._axis_x.setTitleText("time (ms)")
        # self._axis_x.setTitleVisible(False)
        self._axis_x.setGridLineVisible(False)

        self._axis_y.setRange(-0.1, 0.1)
        # self._axis_y.setTitleText("Amp")
        # self._axis_y.setTitleVisible(False)
        self._axis_y.setGridLineVisible(True)

        self._x = np.linspace(0, 100, 512)
        self._y = np.zeros(512)
        self._buffer = [QPointF(x, y) for x, y in zip(self._x, self._y)]
        self._series.append(self._buffer)


class SpectrumChart(LineChart):
    def __init__(self):
        super(SpectrumChart, self).__init__()

        self._axis_x.setRange(0, 1600)
        self._axis_y.setRange(0, 1600)

        self._x = np.linspace(0, 1600, 512)
        self._y = np.zeros(512)

        self._buffer = [QPointF(x, y) for x, y in zip(self._x, self._y)]
        self._series.append(self._buffer)


if __name__ == "__main__":
    app = QApplication()
    wave_chart = WaveChart()
    wave_chart.chart_view.show()
    app.exec()
