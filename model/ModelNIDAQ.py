import os
import json
from typing import Optional
from datetime import datetime

import numpy as np
import numpy.typing as npt
from PySide6.QtCore import Signal, QObject, QTimer

from .utils import CSVStreamWriter
from . import NIDAQ


class NIDAQModel(QObject):
    _cfg_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cfg_ni9234.json')
    _cfg_file = open(_cfg_path)
    _default_settings = json.load(_cfg_file)

    _device_name: str = _default_settings['device_name']
    _task_name: str = _default_settings['default_task_name']
    _sample_rate: int = _default_settings['default_sample_rate']
    _min_sample_rate: int = _default_settings['min_sample_rate']
    _max_sample_rate: int = _default_settings['max_sample_rate']
    _frame_duration: int = _default_settings['default_frame_duration']
    _max_frame_duration: int = _default_settings['default_frame_duration']
    _min_frame_duration: int = _default_settings['min_frame_duration']
    _downsample: int = _default_settings['default_graph_downsample']
    _min_downsample: int = _default_settings['min_graph_downsample']
    _max_downsample: int = _default_settings['max_graph_downsample']
    _update_interval: int = _frame_duration
    _min_update_interval: int = _frame_duration
    _max_update_interval: int = _default_settings['max_update_interval']
    _buffer_rate: int = _default_settings['min_buffer_rate']
    _min_buffer_rate: int = _default_settings['min_buffer_rate']
    _max_buffer_rate: int = _default_settings['max_buffer_rate']
    _chunk_len = int(_sample_rate * _frame_duration * 0.001)
    _buffer_duration: int = _frame_duration * _buffer_rate
    _buffer_len: int = int(_sample_rate * _buffer_duration * 0.001)
    _channels: list[int] = list()
    _sensor_types: list[str] = list()
    _write_file_tirg: bool = False
    _nidaq: NIDAQ.NI9234 = None
    _stream_writer: CSVStreamWriter = None
    _write_file_directory = _default_settings['default_write_file_dir']

    # buffer for visualize data
    _data_buffer_update_timer = QTimer()
    _wave_data_buffer: Optional[npt.NDArray[np.float64]]
    _spectrum_data_buffer: Optional[npt.NDArray[np.float64]]

    task_name_changed = Signal(str)
    sample_rate_changed = Signal(int)
    frame_duration_changed = Signal(int)
    buffer_rate_changed = Signal(int)
    update_interval_changed = Signal(int)
    downsample_changed = Signal(int)
    channels_changed = Signal(list)
    sensor_types_changed = Signal(list)
    write_file_flag_changed = Signal(bool)
    #buffer_duration_changed = Signal(int)

    def __init__(self):
        super().__init__()
        self._data_buffer_update_timer.timeout.connect(self._update_wave_data_buffer)

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
    def buffer_rate(self):
        return self._buffer_rate

    @buffer_rate.setter
    def buffer_rate(self, value: int):
        self._buffer_rate = value
        self.buffer_rate_changed.emit(value)

    @property
    def buffer_duration(self):
        return self._buffer_duration

    @buffer_duration.setter
    def buffer_duration(self, value: int):
        self._buffer_duration = value
        self.buffer_rate_changed.emit(value)

    @property
    def update_interval(self):
        return self._buffer_rate

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

    @property
    def write_file_flag(self):
        return self._write_file_tirg

    @write_file_flag.setter
    def write_file_flag(self, value: bool):
        self._write_file_tirg = value
        self.write_file_flag_changed.emit(value)

    def create(self):
        try:
            self.clear()
        except:
            pass
        self._nidaq = NIDAQ.NI9234(device_name=self._device_name)
        self._nidaq.create_task(task_name=self.task_name)
        for channel, sensor_type in zip(self.channels, self.sensor_types):
            if sensor_type == 'Accelerometer':
                self._nidaq.add_accel_channel(channel)
            if sensor_type == 'Microphone':
                self._nidaq.add_microphone_channel(channel)
        self._nidaq.set_sample_rate(self._sample_rate)
        self._nidaq.set_frame_duration(self._frame_duration)
        self._nidaq.show_daq_params()
        NIDAQ.callback_obj_ptr = self._nidaq.self_ptr
        self._nidaq.ready_read(callback_method=NIDAQ.callback_method)
        self._nidaq.stream_writer.set_directory(self._write_file_directory)

        self._data_buffer_update_timer.setInterval(self._frame_duration)
        self._chunk_len = int(self._sample_rate * self._frame_duration * 0.001)
        self._buffer_duration: int = self._frame_duration * self._buffer_rate
        self._buffer_len: int = int(self._sample_rate * self._buffer_duration * 0.001)

        self._wave_data_buffer = np.zeros((self._nidaq.task.number_of_channels, self._buffer_len))
        # spectrum array format: (number of channels, buffer rate, chunk len)

        self._spectrum_freqs = np.fft.rfftfreq(self._chunk_len, 1/self._sample_rate)
        self._spectrum_data_buffer = np.zeros(
            (self._nidaq.task.number_of_channels, self._buffer_rate, self._spectrum_freqs.shape[0]))

    def start(self):
        if self.write_file_flag:
            self.write_file()

        self._nidaq.set_stream_enable()
        self._nidaq.start_task()
        self._data_buffer_update_timer.start()

    def stop(self):
        self._nidaq.set_stream_disable()
        self._nidaq.stop_task()
        if self.write_file_flag:
            self._nidaq.stream_writer.close_file()
        self._data_buffer_update_timer.stop()

    def clear(self):
        self._nidaq.close_task()
        if self._nidaq.stream_writer.file != None:
            self._nidaq.stream_writer.close_file()

    def ready_write_file(self):
        if self.write_file_flag:
            self._nidaq.set_write_file_enable()
            self.write_file()
        elif not self.write_file_flag:
            self._nidaq.set_write_file_disable()
            self._nidaq.stream_writer.close_file()

    def write_file(self):
        file_name = f'{self.task_name}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        self._nidaq.stream_writer.set_file_name(file_name)
        self._nidaq.stream_writer.open_file()

    def _update_wave_data_buffer(self):
        self._wave_data_buffer = np.roll(
            self._wave_data_buffer, self._chunk_len)
        self._wave_data_buffer[:, :self._chunk_len] = self._nidaq.chunk

        # if _spectrum_flag == True:
        self._spectrum_data = np.abs(np.fft.rfft(self._nidaq.chunk))
        self._spectrum_data_buffer = np.roll(self._spectrum_data_buffer, 1, axis=1)
        self._spectrum_data_buffer[:, 0, :] = self._spectrum_data
        print(self._spectrum_data_buffer[:, 0, 0])

    def interval_split_write_file():
        ...
