
import myDAQs
import numpy as np
import sys
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QSplineSeries
from PySide6.QtCore import Qt, QPointF, Slot, Signal, QObject
from PySide6.QtMultimedia import (QAudioDevice, QAudioFormat,
                                  QAudioSource, QMediaDevices)
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget


class ChunkValueChangedCounter(QObject):
    valueChanged = Signal(int)

    def __init__(self, parent=None):
        super(ChunkValueChangedCounter, self).__init__(parent)
        self._chunk_count = 0

    @property
    def chunk_count(self):
        return self._chunk_count

    @chunk_count.setter
    def chunk_count(self, value):
        self._chunk_count = value
        self.valueChanged.emit(value)
        print('value emit!')


chunk_counter = ChunkValueChangedCounter()

myDAQs.niDAQ.add_accel_channel(0)
myDAQs.niDAQ.add_microphone_channel(1)
myDAQs.niDAQ.set_frame_duration(100)
myDAQs.niDAQ.set_sample_rate(12800)
myDAQs.niDAQ.show_daq_params()
myDAQs.niDAQ.start_streaming()
chunk_count = myDAQs.callback_count
myDAQs.niDAQ.close_task()
