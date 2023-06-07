import os
import json
from typing import Optional
from datetime import datetime

import numpy as np
import numpy.typing as npt
from PySide6.QtCore import QObject, QTimer

from sdk.NIDAQ import NI9234
from sdk.sensor import AccelerometerChannelSettings,MicrophoneChannelSettings


class NIDAQModel(QObject):
    # daq config
    cfg_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cfg_ni9234.json')
    cfg_file = open(cfg_path)
    default_settings = json.load(cfg_file)

    device_name: str = default_settings['device_name']
    task_name: str = default_settings['default_task_name']
    sample_rate: int = default_settings['default_sample_rate']
    min_sample_rate: int = default_settings['min_sample_rate']
    max_sample_rate: int = default_settings['max_sample_rate']
    frame_duration: int = default_settings['default_frame_duration']
    max_frame_duration: int = default_settings['default_frame_duration']
    min_frame_duration: int = default_settings['min_frame_duration']
    downsample: int = default_settings['default_wave_downsample']
    min_downsample: int = default_settings['min_wave_downsample']
    max_downsample: int = default_settings['max_wave_downsample']
    update_interval: int = frame_duration
    min_update_interval: int = frame_duration
    max_update_interval: int = default_settings['max_update_interval']
    buffer_rate: int = default_settings['min_buffer_rate']
    min_buffer_rate: int = default_settings['min_buffer_rate']
    max_buffer_rate: int = default_settings['max_buffer_rate']
    chunk_len = int(sample_rate * frame_duration * 0.001)
    buffer_duration: int = frame_duration * buffer_rate
    wave_buffer_len: int = int(sample_rate * buffer_duration * 0.001)
    channels: list[int] = list()
    sensor_types: list[str] = list()
    writer_switch_flag: bool = False
    nidaq: NI9234 = None
    write_file_directory = default_settings['default_write_file_dir']

    # sensor config
    cfg_sensor_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'sensor_cfg')
    cfg_sensor_path: str = None
    sensor_model: str = None

    # channel setting
    accel_chan_settings:Optional[AccelerometerChannelSettings] = None
    mic_chan_settings:Optional[MicrophoneChannelSettings] = None

    # buffer for visualize data
    data_buffer_update_timer = QTimer()
    wave_data_buffer: Optional[npt.NDArray[np.float64]]
    spectrum_data_buffer: Optional[npt.NDArray[np.float64]]

    wave_data_buffer_mean: float = 0.0
    wave_data_buffer_count: int = 0
    wave_mean_threshold: float = 0.005   # 上線前做調整
    abnormal_flag: bool = False

    def __init__(self):
        super().__init__()
        self.data_buffer_update_timer.timeout.connect(self.update_plot_data_buffer)

    # @property
    # def task_name(self):
    #     return self.task_name

    # @task_name.setter
    # def task_name(self, value: str):
    #     self.task_name = value

    # @property
    # def sample_rate(self):
    #     return self.sample_rate

    # @sample_rate.setter
    # def sample_rate(self, value: int):
    #     self.sample_rate = value

    # @property
    # def frame_duration(self):
    #     return self.frame_duration

    # @frame_duration.setter
    # def frame_duration(self, value: int):
    #     self.frame_duration = value

    # @property
    # def buffer_rate(self):
    #     return self.buffer_rate

    # @buffer_rate.setter
    # def buffer_rate(self, value: int):
    #     self.buffer_rate = value

    # @property
    # def buffer_duration(self):
    #     return self.buffer_duration

    # @buffer_duration.setter
    # def buffer_duration(self, value: int):
    #     self.buffer_duration = value

    # @property
    # def update_interval(self):
    #     return self.buffer_rate

    # @update_interval.setter
    # def update_interval(self, value: int):
    #     self.update_interval = value

    # @property
    # def channels(self):
    #     return self.channels

    # @channels.setter
    # def channels(self, value: list[int]):
    #     self.channels = value

    # @property
    # def sensor_types(self):
    #     return self.sensor_types

    # @sensor_types.setter
    # def sensor_types(self, value: list[str]):
    #     self.sensor_types = value

    # @property
    # def writer_switch_flag(self):
    #     return self.writer_switch_flag

    # @writer_switch_flag.setter
    # def writer_switch_flag(self, value: bool):
    #     self.writer_switch_flag = value
    
    # @property
    # def sensor_model(self):
    #     return self.sensor_model

    # @sensor_model.setter
    # def sensor_model(self, value: bool):
    #     self.sensor_model = value

    # TODO: 要寫一個讀取設定檔的功能
    # 內容包含錄製時間總長、錄製設備、採樣率...
    def read_sensor_cfg_352C33(self):
        sensor_model='352C33'
        cfg_sensor_path = os.path.join(self.cfg_sensor_dir,f'{sensor_model}.json')
        self.accel_chan_settings = AccelerometerChannelSettings(cfg_sensor_path)
        print(
            f'config path:{cfg_sensor_path}\n',
            f'Model : {sensor_model}\n',
            f'physical channel : {self.accel_chan_settings.physical_channel}\n',
            f'channel name : {self.accel_chan_settings.name_to_assign_to_channel}\n',
            f'terminal config : {self.accel_chan_settings.terminal_config}\n',
            f'min value : {self.accel_chan_settings.min_val}\n',
            f'max value : {self.accel_chan_settings.max_val}\n',
            f'units : {self.accel_chan_settings.units}\n',
            f'sensitivity : {self.accel_chan_settings.sensitivity}\n',
            f'sensitivity units : {self.accel_chan_settings.sensitivity_units}\n',
            f'current excitation source : {self.accel_chan_settings.current_excit_source}\n',
            f'current excitation val : {self.accel_chan_settings.current_excit_val}\n',
            f'custom scale name : {self.accel_chan_settings.custom_scale_name}')
        
    def read_sensor_cfg_130F20(self):
        sensor_model='130F20'
        cfg_sensor_path = os.path.join(self.cfg_sensor_dir,f'{sensor_model}.json')
        self.mic_chan_settings = MicrophoneChannelSettings(cfg_sensor_path)
        print(
            f'config path:{cfg_sensor_path}\n',
            f'Model : {sensor_model}\n',
            f'physical channel : {self.mic_chan_settings.physical_channel}\n',
            f'channel name : {self.mic_chan_settings.name_to_assign_to_channel}\n',
            f'terminal config : {self.mic_chan_settings.terminal_config}\n',
            f'min value : {self.mic_chan_settings.mic_sensitivity}\n',
            f'units : {self.mic_chan_settings.units}\n',
            f'mic sensitivity : {self.mic_chan_settings.mic_sensitivity}\n',
            f'max sound pressure level : {self.mic_chan_settings.max_snd_press_level}\n',
            f'current excitation source : {self.mic_chan_settings.current_excit_source}\n',
            f'current excitation val : {self.mic_chan_settings.current_excit_val}\n',
            f'custom scale name : {self.mic_chan_settings.custom_scale_name}')

    def create(self):
        try:
            print('try to clear task')
            self.clear()
        except:
            pass
        self.nidaq = NI9234(device_name=self.device_name)
        self.nidaq.create_task(task_name=self.task_name)
        for channel, sensor_type in zip(self.channels, self.sensor_types):
            if sensor_type == 'Accelerometer':
                self.nidaq.add_accel_channel(channel)
            if sensor_type == 'Microphone':
                self.nidaq.add_microphone_channel(channel)
        self.nidaq.set_sample_rate(self.sample_rate)
        self.nidaq.set_frame_duration(self.frame_duration)
        self.nidaq.show_daq_params()
        self.nidaq.ready_read(callback_method=lambda foo1, foo2, foo3, foo4: self.nidaq.callback_method(
            self.nidaq.task._handle, self.nidaq.every_n_samples_event_type, self.nidaq.frame_size, callback_data=self.nidaq))

        self.data_buffer_update_timer.setInterval(self.frame_duration)
        self.chunk_len = int(self.sample_rate * self.frame_duration * 0.001)
        self.buffer_duration: int = self.frame_duration * self.buffer_rate
        self.wave_buffer_len: int = int(self.sample_rate * self.buffer_duration * 0.001)

        self.wave_data_buffer = np.zeros(
            (self.nidaq.task.number_of_channels, self.wave_buffer_len))
        self.spectrum_freqs = np.fft.rfftfreq(self.chunk_len, 1/self.sample_rate)
        # spectrum array format: (number of channels, buffer rate, chunk len)
        self.spectrum_data_buffer = np.zeros(
            (self.nidaq.task.number_of_channels, self.buffer_rate, self.spectrum_freqs.shape[0]))

    def start(self):
        self.nidaq.start_task()
        self.data_buffer_update_timer.start()
        self.wave_data_cycle_count = 0

    def stop(self):
        if self.writer_switch_flag and self.nidaq.writer.file != None:
            self.nidaq.set_writer_disable()
            self.nidaq.writer
        self.nidaq.stop_task()
        self.data_buffer_update_timer.stop()

    def clear(self):
        self.nidaq.close_task()
        if self.nidaq.writer.file != None:
            self.nidaq.writer.close_file()

    def ready_write_file(self,mode='segment'):
        self.nidaq.set_writer_type(mode)

        if self.writer_switch_flag:
            self.nidaq.set_writer_enable()
            self.write_stream_file()
        if not self.writer_switch_flag:
            if mode=='stream':    
                self.nidaq.set_writer_disable()
                self.nidaq.writer.close_file()
            if mode=='segment':
                self.nidaq.set_writer_disable()
            
    def write_stream_file(self):
        '''
        write all signal to one file while this function is working
        '''
        start_record_time = datetime.now().strftime("%Y%m%dT%H%M%S")
        task_path = os.path.join(self.write_file_directory,self.task_name)
        if not os.path.isdir(task_path):
            os.mkdir(task_path)
        record_path = os.path.join(task_path,start_record_time)
        if not os.path.isdir(record_path):
            os.mkdir(record_path)
        self.nidaq.writer.set_directory(record_path)
        file_path = f'{self.task_name}_{datetime.now().strftime("%Y%m%dT%H%M%S")}.csv'
        self.nidaq.writer.set_file_name(file_path)
        self.nidaq.writer.open_file()

    def write_segment_file(self,period=10):
        '''
        period : seconds, define a time period for a file
        '''
        start_record_time = datetime.now().strftime("%Y%m%dT%H%M%S")
        task_path = os.path.join(self.write_file_directory,self.task_name)
        if not os.path.isdir(task_path):
            os.mkdir(task_path)
        record_path = os.path.join(task_path,start_record_time)
        if not os.path.isdir(record_path):
            os.mkdir(record_path)
        self.nidaq.writer.set_directory(record_path)
        self.nidaq.writer.reset_write_file_count()

    def update_plot_data_buffer(self):
        self.wave_data_buffer = np.roll(
            self.wave_data_buffer, self.chunk_len)
        self.wave_data_buffer[:, :self.chunk_len] = self.nidaq.chunk

        self.spectrum_data = np.abs(np.fft.rfft(self.nidaq.chunk))
        self.spectrum_data[:, 0] = 0  # suppress 0 Hz to 0
        self.spectrum_data_buffer = np.roll(self.spectrum_data_buffer, 1, axis=1)
        for i in range(self.spectrum_data.shape[0]):
            self.spectrum_data_buffer[i, 0, :] = self.spectrum_data[i]
        self.wave_data_buffer_mean = np.mean(np.abs(self.wave_data_buffer))
        # TODO: 需要新增spectrum的開關嗎??

    def get_wave_data_buffer(self):
        return self.wave_data_buffer

    def get_spectrum_data_buffer(self):
        return self.spectrum_data_buffer

    def get_spectrum_freqs(self):
        return self.spectrum_freqs

    def get_wave_buffer_len(self):
        return self.wave_buffer_len

    def get_wave_buffer_mean(self):
        print(f'wave mean:{np.abs(self.wave_data_buffer_mean)}')
        return self.wave_data_buffer_mean

    def get_abnormal_flag(self):
        if np.abs(self.wave_data_buffer_mean) > self.wave_mean_threshold:
            self.wave_data_cycle_count += 1
        else:
            self.wave_data_cycle_count -= 1

        if self.wave_data_cycle_count >= 5:
            self.wave_data_cycle_count = 5
        elif self.wave_data_cycle_count <= 0:
            self.wave_data_cycle_count = 0
        if self.wave_data_cycle_count == 5:
            self.abnormal_flag = True
        else:
            self.abnormal_flag = False
        return self.abnormal_flag

    def write_record_info(self):
        '''
        properties format: 
        {
            machine_ID,
            [sensor_model_0, sensor_model_1, ...],
            [data_name_0, data_name_1, ...],
            [physical_unit_0, physical_unit_1, ],
            DAQ_model,
            start_time,
            sampling_rate,
            end_time,
            chunk_length,
            chunk_count,
            
        }
        '''
        {
            'machine_ID':'dummy_machine',
            'sensor_model':['model_dummy_0'],
            'sensor_serial_number':[],
            'data_name':['data_name_0']
        }
        self.sample_rate

    def record_cfg_checker(self):
        
        ...