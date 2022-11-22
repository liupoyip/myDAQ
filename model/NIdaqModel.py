from datetime import datetime
import os
import json
from typing import Optional
import numpy as np
import numpy.typing as npt
from PySide6.QtCore import Signal, QObject

from .NIDAQ import NI9234
from .utils import CSVStreamWriter

nidaq: Optional[NI9234] = None
stream_writer: Optional[CSVStreamWriter] = None


class DAQModel(QObject, NI9234):
    cfg_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cfg_ni9234.json')
    cfg_file = open(cfg_path)
    default_settings = json.load(cfg_file)

    _device_name: str = default_settings['device_name']
    _task_name: str = default_settings['default_task_name']
    _sample_rate: int = default_settings['default_sample_rate']
    _min_sample_rate: int = default_settings['min_sample_rate']
    _max_sample_rate: int = default_settings['max_sample_rate']
    _frame_duration: int = default_settings['default_frame_duration']
    _max_frame_duration: int = default_settings['default_frame_duration']
    _min_frame_duration: int = default_settings['min_frame_duration']
    _downsample: int = default_settings['default_graph_downsample']
    _min_downsample: int = default_settings['min_graph_downsample']
    _max_downsample: int = default_settings['max_graph_downsample']
    _update_interval: int = _frame_duration
    _min_update_interval: int = _frame_duration
    _max_update_interval: int = default_settings['max_update_interval']
    _buffer_duration: int = _frame_duration
    _min_buffer_duration: int = _frame_duration
    _max_buffer_duration: int = default_settings['max_buffer_duration']
    _channels: list[int] = list()
    _sensor_types: list[str] = list()
    graph_plot_data_buffer: Optional[npt.NDArray[np.float64]]

    task_name_changed = Signal(str)
    sample_rate_changed = Signal(int)
    frame_duration_changed = Signal(int)
    buffer_duration_changed = Signal(int)
    update_interval_changed = Signal(int)
    downsample_changed = Signal(int)
    channels_changed = Signal(list)
    sensor_types_changed = Signal(list)

    def __init__(self):
        super().__init__()

    @property
    def task_name(self):
        return self._task_name

    @task_name.setter
    def task_name(self, value: str):
        self._task_name = value
        self.task_name_changed.emit(value)

    @property
    def sample_rate(self):
        return self._sample_rate

    @sample_rate.setter
    def sample_rate(self, value: int):
        self._sample_rate = value
        self.sample_rate_changed.emit(value)

    @property
    def frame_duration(self):
        return self._frame_duration

    @frame_duration.setter
    def frame_duration(self, value: int):
        self._frame_duration = value
        self.frame_duration_changed.emit(value)

    @property
    def buffer_duration(self):
        return self._buffer_duration

    @buffer_duration.setter
    def buffer_duration(self, value: int):
        self._buffer_duration = value
        self.buffer_duration_changed.emit(value)

    @property
    def update_interval(self):
        return self._buffer_duration

    @update_interval.setter
    def update_interval(self, value: int):
        self._update_interval = value
        self.update_interval_changed.emit(value)

    @property
    def downsample(self):
        return self._downsample

    @downsample.setter
    def downsample(self, value: int):
        self._downsample = value
        self.downsample_changed.emit(value)

    @property
    def channels(self):
        return self._channels

    @channels.setter
    def channels(self, value: list[int]):
        self._channels = value
        self.channels_changed.emit(value)

    @property
    def sensor_types(self):
        return self._sensor_types

    @sensor_types.setter
    def sensor_types(self, value: list[str]):
        self._sensor_types = value
        self.sensor_types_changed.emit(value)

    def create(self):
        global nidaq
        try:
            nidaq.close_task()
        except:
            pass
        nidaq = NI9234(device_name=self._device_name)
        nidaq.create_task(task_name=self.task_name)
        for channel, sensor_type in zip(self.channels, self.sensor_types):
            if sensor_type == 'Accelerometer':
                nidaq.add_accel_channel(channel)
            if sensor_type == 'Microphone':
                nidaq.add_microphone_channel(channel)
        nidaq.set_sample_rate(self.sample_rate)
        nidaq.set_frame_duration(self.frame_duration)
        nidaq.show_daq_params()
        nidaq.ready_read(callback_method=callback_NIDAQ)

    def start(self):
        nidaq.set_stream_on()
        nidaq.start_task()

    def stop(self):
        nidaq.set_stream_off
        nidaq.stop_task()

    def clear(self):
        nidaq.clear_task()


WRTIE_FILE_TRIG = False
stream_writer = CSVStreamWriter(directory='.', file_name='foo.csv')


def callback_NIDAQ(task_handle, every_n_samples_event_type,
                   number_of_samples, callback_data):
    stream_reader = nidaq.callback_data_ptr.value[0]
    chunk = nidaq.callback_data_ptr.value[1]
    stream_reader.read_many_sample(chunk)
    if WRTIE_FILE_TRIG:
        stream_writer.write(nidaq.callback_data_ptr.value[1])
    current_time = datetime.now().isoformat(sep=' ', timespec='milliseconds')
    print(
        f'Current time: {current_time} / Recording... every {number_of_samples} Samples callback invoked. stream trig: {nidaq.stream_trig}\n'
        'Press "p" to stop streaming, "q" to quit program.')

    if not nidaq.stream_trig:
        nidaq.stop_task()
    return 0
