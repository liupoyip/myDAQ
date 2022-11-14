# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

"""PySide6 port of the charts/audio example from Qt v5.x"""

import sys
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QSplineSeries
from PySide6.QtCore import Qt, QPointF, Slot
from PySide6.QtMultimedia import (QAudioDevice, QAudioFormat,
                                  QAudioSource, QMediaDevices)
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox


SAMPLE_COUNT = 2000
RESOLUTION = 100
SAMPLE_RATE = 44100
SAMPLE_COUNT = int(SAMPLE_RATE*0.1)


class WaveChart(QChart):
    def __init__(self, device):
        super().__init__()
        self.line_series = QLineSeries()
        self.addSeries(self.line_series)
        self.axis_x = QValueAxis()
        self.axis_y = QValueAxis()

        self.axis_x.setRange(0, SAMPLE_COUNT)
        self.axis_x.setLabelFormat("%g")
        self.axis_x.setTitleText("Samples")
        self.axis_y.setRange(-1, 1)
        self.axis_y.setTitleText("Audio level")

        self.addAxis(self.axis_x, Qt.AlignBottom)
        self.addAxis(self.axis_y, Qt.AlignLeft)
        self.line_series.attachAxis(self.axis_x)
        self.line_series.attachAxis(self.axis_y)
        self.legend().hide()
        name = device.description()
        self.setTitle(f"Data from the microphone ({name})")
        format_audio = QAudioFormat()
        format_audio.setSampleRate(SAMPLE_RATE)
        format_audio.setChannelCount(1)
        format_audio.setSampleFormat(QAudioFormat.UInt8)

        self._audio_input = QAudioSource(device, format_audio, self)
        self._io_device = self._audio_input.start()
        self._io_device.readyRead.connect(self._readyRead)

        self.chart_view = QChartView(self)

        self._buffer = [QPointF(x, 0) for x in range(SAMPLE_COUNT)]
        self.line_series.append(self._buffer)

    def closeEvent(self, event):
        if self._audio_input is not None:
            self._audio_input.stop()
        event.accept()

    @Slot()
    def _readyRead(self):
        data = self._io_device.readAll()
        available_samples = data.size() // RESOLUTION
        start = 0
        if (available_samples < SAMPLE_COUNT):
            start = SAMPLE_COUNT - available_samples
            for s in range(start):
                self._buffer[s].setY(self._buffer[s + available_samples].y())

        data_index = 0
        for s in range(start, SAMPLE_COUNT):
            value = (ord(data[data_index]) - 128) / 128
            self._buffer[s].setY(value)
            data_index = data_index + RESOLUTION
        self.line_series.replace(self._buffer)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    input_devices = QMediaDevices.audioInputs()
    if not input_devices:
        QMessageBox.warning(
            None, "audio", "There is no audio input device available.")
        sys.exit(-1)
    chart = WaveChart(input_devices[0])
    available_geometry = chart.chart_view.screen().availableGeometry()
    size = available_geometry.height() * 3 / 4
    chart.chart_view.resize(size, size*0.75)
    chart.chart_view.show()
    sys.exit(app.exec())
