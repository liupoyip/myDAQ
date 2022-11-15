# %%
import myDAQs
import numpy as np

import time
import sys

from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QSplineSeries
from PySide6.QtCore import Qt, QPointF, Slot, Signal, QCoreApplication, QThread
from PySide6.QtMultimedia import (QAudioDevice, QAudioFormat,
                                  QAudioSource, QMediaDevices)
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget

# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

"""PySide6 port of the charts/audio example from Qt v5.x"""

import myDAQs
import numpy as np

import sys
from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QSplineSeries
from PySide6.QtCore import Qt, QPointF, Slot, Signal, QObject, Property
from PySide6.QtMultimedia import (QAudioDevice, QAudioFormat,
                                  QAudioSource, QMediaDevices)
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget


# class DAQValueChanged(QObject):
#     valueChanged = Signal()

#     def __init__(self, parent=None):
#         super(DAQValueChanged, self).__init__(parent)
#         self._t = 0

#     @property
#     def t(self):
#         return self._t

#     @t.setter
#     def t(self, value):
#         self._t = value
#         self.valueChanged.emit(value)


# app = QCoreApplication(sys.argv)
# obj = DAQValueChanged()


# class ChunkTracker(QObject):
#     def __init__(self, startval=0):
#         super(ChunkTracker, self).__init__()
#         self.ppval = startval

#     @Property(int)
#     def pp(self):
#         return self.ppval

#     @pp.setter
#     def pp(self, val):
#         self.ppval = val


# obj = ChunkTracker()
# obj.pp = 47
# print(obj.pp)

# %%

user_name = 'hello'


class ChunkTracker(QObject):

    def __init__(self, name):
        super(ChunkTracker, self).__init__()
        self._person_name = name

    def _name(self):
        return self._person_name

    @Signal
    def name_changed(self):
        print(self._person_name)
        pass

    name = Property(str, _name, notify=name_changed)


chunk_tracker = ChunkTracker(user_name)
user_name = 'world'

# myDAQs.niDAQ.add_accel_channel(0)
# myDAQs.niDAQ.add_microphone_channel(1)
# myDAQs.niDAQ.set_frame_duration(100)
# myDAQs.niDAQ.set_sample_rate(12800)

# myDAQs.niDAQ.show_daq_params()
# myDAQs.niDAQ.start_streaming()

# myDAQs.niDAQ.close_task()
# %%
# chunk = 0


# # class DAQChunkSignal(QThread):


# class DAQChunkSignal(QWidget):
#     signal = Signal()

#     def __init__(self, parent=None):
#         super(DAQChunkSignal, self).__init__(parent)
#         self.signal.connect(show_chunk)
#         self.start()

#     def run(self):
#         while True:
#             # show_chunk
#             print('run')
#             self.signal.emit()
#             time.sleep(1)

#     # @property
#     # def t(self):
#     #    return self._t

# #    @t.setter
# #    def t(self, value):
# #        self._t = value
# #        self.valueChanged.emit(value)
# #        self.valueChanged.connect(show_chunk)


# def show_chunk():
#     print(chunk)


# if __name__ == '__main__':
#     #app = QCoreApplication(sys.argv)
#     app = QApplication(sys.argv)
#     daq_chunk_value_change_signal = DAQChunkSignal()

#     # print(chunk)

#     chunk += 1
#     sys.exit(app.exec())
