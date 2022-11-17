
import myDAQs
import utils

import sys
import os
from datetime import datetime
import asyncio

import numpy as np

from PySide6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis, QSplineSeries
from PySide6.QtCore import Qt, QPointF, Slot, Signal, QObject, QThread, QTimer
from PySide6.QtMultimedia import QAudioDevice, QAudioFormat, QAudioSource, QMediaDevices
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox, QWidget, QHBoxLayout
from PySide6.QtGui import QKeyEvent

"""
myDAQs.NI9234.callback_data_ptr.value[0] : NiStreamReaders.AnalogMultiChannelReader(nidaqmx.Task.in_stream)
myDAQs.NI9234.callback_data_ptr.value[1] : chunk in myDAQs module
"""

WRTIE_CSV_TRIG = True
CALLBACK_COUNT = 0
WAVE_PLOT_CHUNK = None
FRAME_INTERVAL = 250


class NiWaveChunkChanger(QObject):

    valueChanged = Signal(int)

    def __init__(self, niDAQ: myDAQs.NI9234, parent=None):
        super(NiWaveChunkChanger, self).__init__(parent)
        self._count = 0
        self.wave_plot_chunk = niDAQ.callback_data_ptr.value[1]

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, count):
        self._value = count
        self.valueChanged.emit(count)
        self.wave_plot_chunk = niDAQ.callback_data_ptr.value[1]
        print(self.wave_plot_chunk.shape)
        print('value emit!')


class WaveChart(QChart):
    def __init__(self):
        super().__init__()

        self.timer = QTimer()
        self.timer.timeout.connect(self.interval_update_line)
        self.timer.setInterval(FRAME_INTERVAL)

        self.setTitle(f"Wave Plot")
        self.line_series = QLineSeries()
        self.addSeries(self.line_series)
        self.axis_x = QValueAxis()
        self.axis_y = QValueAxis()

        #self.sample_count = len(chunk_changer.wave_plot_chunk)
        self.sample_count = 1024
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
        self.pre_buffer = [QPointF(x, 0) for x in range(self.sample_count)]
        self.chart_view = QChartView(self)
        self.line_series.append(self.buffer)

        self.timer.start()

    @Slot()
    def interval_update_line(self):

        if niDAQ.stream_trig:
            self.buffer = [QPointF(x, y) for x, y in zip(
                range(self.sample_count), WAVE_PLOT_CHUNK[0])]
            # self.buffer != self.pre_buffer:
            self.pre_buffer = self.buffer
            print('interval_update_line')
            self.line_series.replace(self.buffer)


class ChartHorizonLayout(QWidget):
    def __init__(self, chart_view: QChartView):
        super().__init__()

        self.box_layout = QHBoxLayout()
        self.box_layout.addWidget(chart_view)
        self.setLayout(self.box_layout)

        print('Press "s" to start streaming')

    def keyPressEvent(self, event: QKeyEvent) -> None:
        print(f'key num: {event.key()} / key text: {event.text()}')
        if event.text() == 's':
            event_loop = asyncio.get_event_loop()
            tasks = [
                asyncio.ensure_future(niDAQ.async_streaming()),
                asyncio.ensure_future(niDAQ.key_stop_event())
            ]
            event_loop.run_until_complete(asyncio.wait(tasks))
            # TODO: 用event 更新plot


def callback_NIDAQ(task_handle, every_n_samples_event_type,
                   number_of_samples, callback_data):
    global CALLBACK_COUNT

    CALLBACK_COUNT += 1
    stream_reader = niDAQ.callback_data_ptr.value[0]
    chunk = niDAQ.callback_data_ptr.value[1]
    stream_reader.read_many_sample(chunk)
    ni_wave_chunk_changer.value = CALLBACK_COUNT

    if WRTIE_CSV_TRIG:
        csv_stream_writer.write(chunk)
    current_time = datetime.now().isoformat(sep=' ', timespec='milliseconds')
    print(f'Current time: {current_time}')
    print(
        f'Current time: {current_time} Recording... every {number_of_samples} Samples callback invoked. stream trig: {niDAQ.stream_trig}\n'
        'Press "p" to stop streaming.\t Press "q" to quit program.')

    if not niDAQ.stream_trig:
        niDAQ.stop_task()

    return 0


directory = '.'
file_name = 'foo.csv'
csv_stream_writer = utils.CSVStreamWriter(directory, file_name)


niDAQ = myDAQs.NI9234(device_name='NI_9234', task_name='myTask')
niDAQ.add_accel_channel(0)
niDAQ.add_accel_channel(1)
niDAQ.add_microphone_channel(2)
niDAQ.add_microphone_channel(3)
niDAQ.set_frame_duration(FRAME_INTERVAL)
niDAQ.set_sample_rate(12800)
niDAQ.show_daq_params()
niDAQ.ready_read(callback_method=callback_NIDAQ)


app = QApplication(sys.argv)
ni_wave_chunk_changer = NiWaveChunkChanger(niDAQ)
chart_wave = WaveChart()
window = ChartHorizonLayout(chart_view=chart_wave.chart_view)
window.resize(400, 300)
available_geometry = window.screen().availableGeometry()
size = available_geometry.height() * 3 / 4
window.resize(size, size*0.75)
window.show()
# niDAQ.start_streaming(callback_method=callback_NIDAQ)

# niDAQ.close_task()

app.exec()
sys.exit(app.exec())
