import numpy as np
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QSplineSeries
from PySide6.QtCore import QPointF, Slot, Qt, Signal, QPoint
from PySide6.QtWidgets import (QApplication, QMainWindow, QMessageBox, QWidget,
                               QGraphicsView, QGraphicsScene, QSizePolicy, QRubberBand,
                               QVBoxLayout, QFormLayout, QHBoxLayout, QSizePolicy, QPushButton)
from PySide6.QtGui import QPen, QColor, QPalette, QBrush, QWheelEvent, qRgb, QMouseEvent


class ChartView(QChartView):
    pass


class LineChart(QWidget):
    mouse_moved = Signal(QPoint)

    def __init__(self):
        super().__init__()
        self._chart = QChart()
        self._series = QLineSeries()
        self.PushButton = QPushButton()

        self._chart.addSeries(self._series)
        self._axis_x = QValueAxis()
        self._axis_x.setRange(0, 100)
        self._axis_x.setGridLineVisible(False)

        self._axis_y = QValueAxis()
        self._axis_y.setRange(-1, 1)
        self._axis_y.setGridLineVisible(True)

        self._chart.addAxis(self._axis_x, Qt.AlignBottom)
        self._chart.addAxis(self._axis_y, Qt.AlignLeft)
        self._series.attachAxis(self._axis_x)
        self._series.attachAxis(self._axis_y)
        self._chart.legend().hide()

        self._chart.setBackgroundRoundness(0)
        self._chart.layout().setContentsMargins(0, 0, 0, 0)
        self.chart_view = ChartView()
        self.chart_view.setChart(self._chart)
        self._x = np.linspace(0, 100, 512)
        self._y = np.zeros(512)
        self._buffer = [QPointF(x, y) for x, y in zip(self._x, self._y)]
        self._series.append(self._buffer)

        self.set_dark_theme()

    # @Slot()
    def mouseMoveEvent(self, event) -> None:
        self.mouse_moved.emit(event.pos())
        print(event.x(), event.y())
        # return QChartView.mouseMoveEvent(self, event)
        # return QChartView.mouseMoveEvent(self, event)

    def set_y(self, y_line):
        if len(self._buffer) != y_line.shape[0]:
            raise BaseException('Length of buffer and y-line is not match!')
        for i in range(y_line.shape[0]):
            self._buffer[i].setY(y_line[i])
        self._series.replace(self._buffer)

    def set_dark_theme(self):
        self._pen = QPen()
        self._pen.setWidth(1)
        self._pen.setColor(QColor(Qt.cyan))
        self._series.setPen(self._pen)

        self._chart.setBackgroundBrush(QBrush(QColor(qRgb(35, 35, 45))))
        self._axis_x.setTitleBrush(QBrush(QColor(Qt.white)))
        self._axis_y.setTitleBrush(QBrush(QColor(Qt.white)))
        self._axis_x.setLabelsBrush(QBrush(QColor(Qt.white)))
        self._axis_y.setLabelsBrush(QBrush(QColor(Qt.white)))


class WaveChart(LineChart):
    def __init__(self):
        super(WaveChart, self).__init__()

        self._axis_x.setRange(0, 100)
        self._axis_x.setLabelFormat('%d')
        self._axis_x.setLabelsEditable(True)
        self._axis_x.setTitleText("time (ms)")
        # self._axis_x.setTitleVisible(False)
        self._axis_x.setGridLineVisible(False)

        self._axis_y.setRange(-0.1, 0.1)
        self._axis_y.setLabelFormat('%.2f')
        self._axis_y.setLabelsEditable(True)
        self._axis_y.setTitleText("value")
        # self._axis_y.setTitleVisible(False)
        self._axis_y.setGridLineVisible(True)

        self._x = np.linspace(0, 100, 512)
        self._y = np.zeros(512)
        self._buffer = [QPointF(x, y) for x, y in zip(self._x, self._y)]
        self._series.append(self._buffer)

        #self.mouse_moved = Signal(QPoint)
        # self.mouse_moved.connect(self.mouseMoveEvent)

    def reset_axis(self, end_point, buffer_len):
        self._axis_x.setRange(0, end_point)
        self._x = np.linspace(0, end_point, buffer_len)
        self._y = np.zeros(buffer_len)
        self._buffer = [QPointF(x, y) for x, y in zip(self._x, self._y)]
        self._series.replace(self._buffer)


class SpectrumChart(LineChart):
    def __init__(self):
        super(SpectrumChart, self).__init__()

        self._axis_x.setRange(0, 1600)
        self._axis_x.setLabelFormat('%d')
        self._axis_x.setLabelsEditable(True)
        self._axis_x.setTitleText("Hz")
        self._axis_x.setGridLineVisible(False)

        self._axis_y.setRange(0, 1)
        self._axis_y.setLabelFormat('%.2f')
        self._axis_y.setLabelsEditable(True)
        self._axis_y.setTitleText("power (norm 0~1)")

        self._x = np.linspace(0, 1600, 512)
        self._y = np.zeros(512)

        self._buffer = [QPointF(x, y) for x, y in zip(self._x, self._y)]
        self._series.append(self._buffer)

        #self.mouse_moved = Signal(QPoint)
        # self.mouse_moved.connect(self.mouseMoveEvent)

    def reset_axis(self, end_point, buffer_len):
        self._axis_x.setRange(0, end_point)
        self._axis_y.setRange(0, 1)
        self._x = np.linspace(0, end_point, buffer_len)
        self._y = np.zeros(buffer_len)
        self._buffer = [QPointF(x, y) for x, y in zip(self._x, self._y)]
        self._series.replace(self._buffer)


if __name__ == "__main__":
    app = QApplication()
    layout = QHBoxLayout()

    wave_chart_1 = WaveChart()
    wave_chart_2 = SpectrumChart()

    layout.addWidget(wave_chart_1.chart_view, 3)
    layout.addWidget(wave_chart_2.chart_view, 2)
    layout.setSpacing(0)
    window = QWidget()

    window.setLayout(layout)
    window.layout().setContentsMargins(0, 0, 0, 0)
    window.setFixedSize(640, 360)
    window.show()

    app.exec()
