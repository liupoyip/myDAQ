import os
import json
from typing import Optional
from datetime import datetime

import numpy as np
import numpy.typing as npt
from PySide6.QtCore import Signal, QObject

from .utils import CSVStreamWriter
from . import NIDAQ


class DAQModel(QObject):
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
    _buffer_duration: int = _frame_duration
    _min_buffer_duration: int = _frame_duration
    _max_buffer_duration: int = _default_settings['max_buffer_duration']
    _channels: list[int] = list()
    _sensor_types: list[str] = list()
    _graph_plot_data_buffer: Optional[npt.NDArray[np.float64]]
    _write_file_tirg: bool = False

    _nidaq: NIDAQ.NI9234 = None
    _stream_writer: CSVStreamWriter = None
    _write_file_directory = _default_settings['default_write_file_dir']

    task_name_changed = Signal(str)
    sample_rate_changed = Signal(int)
    frame_duration_changed = Signal(int)
    buffer_duration_changed = Signal(int)
    update_interval_changed = Signal(int)
    downsample_changed = Signal(int)
    channels_changed = Signal(list)
    sensor_types_changed = Signal(list)
    write_file_flag_changed = Signal(bool)

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
        self._nidaq.set_sample_rate(self.sample_rate)
        self._nidaq.set_frame_duration(self.frame_duration)
        self._nidaq.show_daq_params()
        NIDAQ.callback_obj_ptr = self._nidaq.self_ptr
        self._nidaq.ready_read(callback_method=self._nidaq.callback_method)

        self._nidaq.stream_writer.set_directory(self._write_file_directory)

    def start(self):
        if self.write_file_flag:
            self.write_file()

        self._nidaq.set_stream_enable()
        self._nidaq.start_task()

    def stop(self):
        self._nidaq.set_stream_disable()
        self._nidaq.stop_task()
        if self.write_file_flag:
            self._nidaq.stream_writer.close_file()

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

    def interval_split_write_file():
        pass
