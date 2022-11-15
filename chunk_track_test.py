
import myDAQs

import sys
import os
from datetime import datetime

import numpy as np

from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QSplineSeries
from PySide6.QtCore import Qt, QPointF, Slot, Signal, QObject
from PySide6.QtMultimedia import (QAudioDevice, QAudioFormat,
                                  QAudioSource, QMediaDevices)
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget

"""
myDAQs.callback_data_ptr.value[0] : NiStreamReaders.AnalogMultiChannelReader(nidaqmx.Task.in_stream)
myDAQs.callback_data_ptr.value[1] : chunk in myDAQs module
"""

WRTIE_CSV_TRIG = True
CALLBACK_COUNT = 0
WAVE_PLOT_CHUNK = None


class CSVStreamWriter:
    def __init__(self, directory: str, file_name: str):
        self.directory = directory
        self.file_name = file_name
        self.check_file_extension()
        self.file_path = os.path.join(self.directory, self.file_name)
        self.file = None
        self.open_file()

    def open_file(self):
        self.file = open(self.file_path, mode='a')

    def close_file(self):
        self.file.close()

    def check_file_extension(self):
        name, extension = os.path.splitext(self.file_name)
        if extension != '.csv':
            raise BaseException('Illegal file extension, *.csv required.')

    def write(self, chunk):
        np.savetxt(fname=self.file, X=np.transpose(chunk), delimiter=',')


class NiWaveChunkChanger(QObject):

    valueChanged = Signal(int)
    wave_plot_chunk = np.zeros(1024)

    def __init__(self, parent=None):
        super(NiWaveChunkChanger, self).__init__(parent)
        self._value = 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self.valueChanged.emit(value)
        self.wave_plot_chunk = myDAQs.callback_data_ptr.value[1].copy()
        print(self.wave_plot_chunk[0])
        print('value emit!')


class WaveChart(QChart):
    def __init__(self, device, chunk_changer: NiWaveChunkChanger):
        super().__init__()
        self.setTitle(f"Wave Plot")
        self.line_series = QLineSeries()
        self.addSeries(self.line_series)
        self.axis_x = QValueAxis()
        self.axis_y = QValueAxis()

        self.sample_count = len(chunk_changer.wave_plot_chunk)
        self.axis_x.setRange(0, self.sample_count)
        self.axis_x.setLabelFormat("%g")
        self.axis_x.setTitleText("Samples")
        self.axis_y.setRange(-1, 1)
        self.axis_y.setTitleText("Audio level")

        self.addAxis(self.axis_x, Qt.AlignBottom)
        self.addAxis(self.axis_y, Qt.AlignLeft)
        self.line_series.attachAxis(self.axis_x)
        self.line_series.attachAxis(self.axis_y)
        self.legend().hide()

        self.buffer = [QPointF(x, 0) for x in range(self.sample_count)]
        self.chart_view = QChartView(self)
        self.line_series.append(self.buffer)


def callback_NIDAQ(task_handle, every_n_samples_event_type,
                   number_of_samples, callback_data):
    global CALLBACK_COUNT, WRTIE_CSV_TRIG
    CALLBACK_COUNT += 1
    stream_reader = myDAQs.callback_data_ptr.value[0]
    chunk = myDAQs.callback_data_ptr.value[1]
    stream_reader.read_many_sample(chunk)

    if WRTIE_CSV_TRIG:
        csv_stream_writer.write(chunk)
    current_time = datetime.now().isoformat(sep=' ', timespec='milliseconds')
    print(f'Current time: {current_time}')
    print(f'NI-DAQ recording... every {number_of_samples} Samples callback invoked.')
    print(f'Task handle id: {task_handle}, Callback count: {CALLBACK_COUNT}')
    ni_wave_chunk_changer.value = CALLBACK_COUNT

    return 0


directory = '.'
file_name = 'foo.csv'
csv_stream_writer = CSVStreamWriter(directory, file_name)
ni_wave_chunk_changer = NiWaveChunkChanger()


def initailize_nidaq():
    myDAQs.niDAQ = myDAQs.NI9234(device_name='NI_9234', task_name='myTask')
    myDAQs.niDAQ.add_accel_channel(0)
    myDAQs.niDAQ.add_microphone_channel(1)
    myDAQs.niDAQ.set_frame_duration(200)
    myDAQs.niDAQ.set_sample_rate(12800)
    myDAQs.niDAQ.show_daq_params()


myDAQs.niDAQ.start_streaming(callback_method=callback_NIDAQ)
myDAQs.niDAQ.close_task()
