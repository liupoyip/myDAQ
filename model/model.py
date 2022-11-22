import numpy as np
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import QObject
from PySide6.QtCore import Signal

from datetime import datetime
from .NIDAQ import NI9234
from ..views.ni9234_form import NI9234Form
from ..utils import CSVStreamWriter

WRTIE_FILE_TRIG = False
CALLBACK_COUNT = 0
WAVE_PLOT_CHUNK = None
FRAME_INTERVAL = 100
niDAQ = NI9234(device_name='NI_9234')


class NiWaveChunkChanger(QObject):
    valueChanged = Signal(int)

    def __init__(self, parent=None):
        super(NiWaveChunkChanger, self).__init__(parent)
        self._count = 0

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, count):
        global WAVE_PLOT_CHUNK
        self._count = count
        self.valueChanged.emit(count)
        WAVE_PLOT_CHUNK = niDAQ.callback_data_ptr.value[1]
        print(f'chunk for plotting wave is recieve! , chunk shape: {WAVE_PLOT_CHUNK.shape}')


ni_wave_chunk_changer = NiWaveChunkChanger()
csv_stream_writer = CSVStreamWriter()


def callback_NIDAQ(task_handle, every_n_samples_event_type,
                   number_of_samples, callback_data):
    global CALLBACK_COUNT

    CALLBACK_COUNT += 1
    stream_reader = niDAQ.callback_data_ptr.value[0]
    stream_reader.read_many_sample(niDAQ.callback_data_ptr.value[1])    # read daq buffer data
    ni_wave_chunk_changer.count = CALLBACK_COUNT

    if WRTIE_FILE_TRIG:
        csv_stream_writer.write(niDAQ.callback_data_ptr.value[1])
    current_time = datetime.now().isoformat(sep=' ', timespec='milliseconds')
    print(
        f'Current time: {current_time}\tCallback count: {CALLBACK_COUNT}\tstream trig: {niDAQ.stream_trig}\n'
        f'Recording...\t every {number_of_samples} Samples callback invoked. \n'
        'Press "s" to start streaming, "p" to stop streamming.')

    if not niDAQ.stream_trig:
        niDAQ.stop_task()

    return 0
