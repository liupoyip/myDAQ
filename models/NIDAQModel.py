import os
import json
from typing import Optional
from datetime import datetime

import numpy as np
import numpy.typing as npt
from PySide6.QtCore import QObject, QTimer

from sdk.NIDAQ import NI9234


class NIDAQModel(QObject):
    _cfg_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cfg_ni9234.json')
    _cfg_file = open(_cfg_path)
    default_settings = json.load(_cfg_file)

    _device_name: str = default_settings['device_name']
    _task_name: str = default_settings['default_task_name']
    _sample_rate: int = default_settings['default_sample_rate']
    _min_sample_rate: int = default_settings['min_sample_rate']
    _max_sample_rate: int = default_settings['max_sample_rate']
    _frame_duration: int = default_settings['default_frame_duration']
    _max_frame_duration: int = default_settings['default_frame_duration']
    _min_frame_duration: int = default_settings['min_frame_duration']
    _downsample: int = default_settings['default_wave_downsample']
    _min_downsample: int = default_settings['min_wave_downsample']
    _max_downsample: int = default_settings['max_wave_downsample']
    _update_interval: int = _frame_duration
    _min_update_interval: int = _frame_duration
    _max_update_interval: int = default_settings['max_update_interval']
    _buffer_rate: int = default_settings['min_buffer_rate']
    _min_buffer_rate: int = default_settings['min_buffer_rate']
    _max_buffer_rate: int = default_settings['max_buffer_rate']
    _chunk_len = int(_sample_rate * _frame_duration * 0.001)
    _buffer_duration: int = _frame_duration * _buffer_rate
    _wave_buffer_len: int = int(_sample_rate * _buffer_duration * 0.001)
    _channels: list[int] = list()
    _sensor_types: list[str] = list()
    _write_file_flag: bool = False
    _nidaq: NI9234 = None
    _write_file_directory = default_settings['default_write_file_dir']

    # buffer for visualize data
    _data_buffer_update_timer = QTimer()
    _wave_data_buffer: Optional[npt.NDArray[np.float64]]
    _spectrum_data_buffer: Optional[npt.NDArray[np.float64]]

    _wave_data_buffer_mean: float = 0.0
    _wave_data_buffer_count: int = 0
    _wave_mean_threshold: float = 0.005   # 上線前做調整
    _abnormal_flag: bool = False

    def __init__(self):
        super().__init__()
        self._data_buffer_update_timer.timeout.connect(self._update_plot_data_buffer)

    @property
    def task_name(self):
        return self._task_name

    @task_name.setter
    def task_name(self, value: str):
        self._task_name = value

    @property
    def sample_rate(self):
        return self._sample_rate

    @sample_rate.setter
    def sample_rate(self, value: int):
        self._sample_rate = value

    @property
    def frame_duration(self):
        return self._frame_duration

    @frame_duration.setter
    def frame_duration(self, value: int):
        self._frame_duration = value

    @property
    def buffer_rate(self):
        return self._buffer_rate

    @buffer_rate.setter
    def buffer_rate(self, value: int):
        self._buffer_rate = value

    @property
    def buffer_duration(self):
        return self._buffer_duration

    @buffer_duration.setter
    def buffer_duration(self, value: int):
        self._buffer_duration = value

    @property
    def update_interval(self):
        return self._buffer_rate

    @update_interval.setter
    def update_interval(self, value: int):
        self._update_interval = value

    @property
    def channels(self):
        return self._channels

    @channels.setter
    def channels(self, value: list[int]):
        self._channels = value

    @property
    def sensor_types(self):
        return self._sensor_types

    @sensor_types.setter
    def sensor_types(self, value: list[str]):
        self._sensor_types = value

    @property
    def write_file_flag(self):
        return self._write_file_flag

    @write_file_flag.setter
    def write_file_flag(self, value: bool):
        self._write_file_flag = value

    def create(self):
        try:
            self.clear()
        except:
            pass
        self._nidaq = NI9234(device_name=self._device_name)
        self._nidaq.create_task(task_name=self.task_name)
        for channel, sensor_type in zip(self.channels, self.sensor_types):
            if sensor_type == 'Accelerometer':
                self._nidaq.add_accel_channel(channel)
            if sensor_type == 'Microphone':
                self._nidaq.add_microphone_channel(channel)
        self._nidaq.set_sample_rate(self._sample_rate)
        self._nidaq.set_frame_duration(self._frame_duration)
        self._nidaq.show_daq_params()
        self._nidaq.ready_read(callback_method=lambda foo1, foo2, foo3, foo4: self._nidaq.callback_method(
            self._nidaq.task._handle, self._nidaq.every_n_samples_event_type, self._nidaq.frame_size, callback_data=self._nidaq))
        self._nidaq.stream_writer.set_directory(self._write_file_directory)

        self._data_buffer_update_timer.setInterval(self._frame_duration)
        self._chunk_len = int(self._sample_rate * self._frame_duration * 0.001)
        self._buffer_duration: int = self._frame_duration * self._buffer_rate
        self._wave_buffer_len: int = int(self._sample_rate * self._buffer_duration * 0.001)

        self._wave_data_buffer = np.zeros(
            (self._nidaq.task.number_of_channels, self._wave_buffer_len))
        self._spectrum_freqs = np.fft.rfftfreq(self._chunk_len, 1/self._sample_rate)
        # spectrum array format: (number of channels, buffer rate, chunk len)
        self._spectrum_data_buffer = np.zeros(
            (self._nidaq.task.number_of_channels, self._buffer_rate, self._spectrum_freqs.shape[0]))

    def start(self):
        if self._write_file_flag:
            self.write_file()
        self._nidaq.set_stream_enable()
        self._nidaq.start_task()
        self._data_buffer_update_timer.start()
        self._wave_data_cycle_count = 0

    def stop(self):
        self._nidaq.set_stream_disable()
        self._nidaq.stop_task()
        if self._write_file_flag:
            self._nidaq.stream_writer.close_file()
        self._data_buffer_update_timer.stop()

    def clear(self):
        self._nidaq.close_task()
        if self._nidaq.stream_writer.file != None:
            self._nidaq.stream_writer.close_file()

    def ready_write_file(self,mode='stream'):
        if mode=='stream':
            if self._write_file_flag:
                self._nidaq.set_write_file_enable()
                self.write_stream_file(mode)
            elif not self._write_file_flag:
                self._nidaq.set_write_file_disable()
                self._nidaq.stream_writer.close_file()
        
        #if mode=='chunk':
        #    ...

    
    def write_stream_file(self,mode):
        #file_name = f'{self.task_name}_{datetime.now().isoformat()}.csv'
        file_name = f'{self.task_name}_{datetime.now().strftime("%Y%m%dT%H%M%S")}.csv'
        self._nidaq.stream_writer.set_file_name(file_name)
        self._nidaq.stream_writer.open_file()

    def _update_plot_data_buffer(self):
        self._wave_data_buffer = np.roll(
            self._wave_data_buffer, self._chunk_len)
        self._wave_data_buffer[:, :self._chunk_len] = self._nidaq.chunk

        self._spectrum_data = np.abs(np.fft.rfft(self._nidaq.chunk))
        self._spectrum_data[:, 0] = 0  # suppress 0 Hz to 0
        self._spectrum_data_buffer = np.roll(self._spectrum_data_buffer, 1, axis=1)
        for i in range(self._spectrum_data.shape[0]):
            self._spectrum_data_buffer[i, 0, :] = self._spectrum_data[i]
        self._wave_data_buffer_mean = np.mean(np.abs(self._wave_data_buffer))
        # TODO: 需要新增spectrum的開關嗎??

    def get_wave_data_buffer(self):
        return self._wave_data_buffer

    def get_spectrum_data_buffer(self):
        return self._spectrum_data_buffer

    def get_spectrum_freqs(self):
        return self._spectrum_freqs

    def get_wave_buffer_len(self):
        return self._wave_buffer_len

    def get_wave_buffer_mean(self):
        print(f'wave mean:{np.abs(self._wave_data_buffer_mean)}')
        return self._wave_data_buffer_mean

    def get_abnormal_flag(self):
        if np.abs(self._wave_data_buffer_mean) > self._wave_mean_threshold:
            self._wave_data_cycle_count += 1
        else:
            self._wave_data_cycle_count -= 1

        if self._wave_data_cycle_count >= 5:
            self._wave_data_cycle_count = 5
        elif self._wave_data_cycle_count <= 0:
            self._wave_data_cycle_count = 0
        if self._wave_data_cycle_count == 5:
            self._abnormal_flag = True
        else:
            self._abnormal_flag = False
        return self._abnormal_flag

    def interval_split_write_file():
        ...
