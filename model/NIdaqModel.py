
import os
import json
from typing import Optional, Union
import numpy as np
import numpy.typing as npt
from PySide6.QtCore import Signal, QObject

from .NIdaq import NI9234

cfg_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cfg_ni9234.json')
cfg_file = open(cfg_path)


class DAQModel(QObject, NI9234):
    default_settings = json.load(cfg_file)
    _device_name: str = default_settings['device_name']
    _default_task_name: str = default_settings['default_task_name']
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
    sample_rate_changed = Signal(int)
    frame_duration_changed = Signal(int)
    buffer_duration_changed = Signal(int)
    update_interval_changed = Signal(int)
    downsample_changed = Signal(int)
    channels_changed = Signal(list)

    def __init__(self):
        super().__init__()
        #self.nidaq = NI9234(device_name=self._device_name)

    @property
    def sample_rate(self):
        return self._sample_rate

    @sample_rate.setter
    def sample_rate(self, value: int):
        self._sample_rate = value
        self.sample_rate_changed.emit(value)

    @property
    def frame_duration(self):
        return self._sample_rate

    @frame_duration.setter
    def frame_duration(self, value: int):
        self._sample_rate = value
        self.sample_rate_changed.emit(value)

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

    def start_record(self):
        self.niDAQ = NI9234(device_name=self._device_name)
        self.niDAQ.create_task(task_name='myTask')
        for channel in self.channels:
            self.niDAQ.add_accel_channel(channel)
            self.niDAQ.add_accel_channel(channel)
        # niDAQ.add_microphone_channel(2)
        # niDAQ.add_microphone_channel(3)
        self.niDAQ.set_sample_rate(self.sample_rate)
        self.niDAQ.set_frame_duration(self.frame_duration)
