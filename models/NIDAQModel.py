import os
import sys
import json
from typing import Optional, Union
from datetime import datetime

import numpy as np
import numpy.typing as npt
from PySide6.QtCore import QObject, QTimer

from sdk.NIDAQ import NI9234
from sdk.sensor import AccelerometerChannelSettings, MicrophoneChannelSettings
from sdk.utils import get_func_name
from debug_flags import PRINT_FUNC_NAME_FLAG


class NIDAQModel(QObject):
    # machine info
    machine_name: str = 'dummy_machine'

    # daq config
    cfg_path = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'cfg_ni9234.json')
    cfg_file = open(cfg_path)
    default_settings = json.load(cfg_file)
    cfg_file.close()
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
    channel_settings: list[Optional[Union[AccelerometerChannelSettings,
                                          MicrophoneChannelSettings]]] = list()

    writer_switch_flag: bool = False
    nidaq: NI9234 = None
    write_file_directory = default_settings['default_write_file_dir']
    writer_mode = None
    chunk_count = 0

    # sensor config
    sensor_types: list[str] = list()
    active_sensor_model_list: list[str] = list()
    active_sensor_cfg_list: list[str] = list()
    cfg_sensor_dir = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'sensors')
    cfg_sensor_path: str = None
    sensor_model: str = None

    # channel setting
    accel_chan_settings: AccelerometerChannelSettings = None
    mic_chan_settings: MicrophoneChannelSettings = None
    all_channel_settings: list[Union[AccelerometerChannelSettings,
                                     MicrophoneChannelSettings]] = [None, None, None, None]

    # buffer for visualize data
    data_buffer_update_timer = QTimer()
    wave_data_buffer: Optional[npt.NDArray[np.float64]]
    spectrum_data_buffer: Optional[npt.NDArray[np.float64]]

    wave_data_buffer_mean: float = 0.0
    wave_data_buffer_count: int = 0
    wave_mean_threshold: float = 0.005   # 上線前做調整
    abnormal_flag: bool = False

    # record file args
    task_dir = ''
    record_dir = ''
    export_cfg_file_name = 'cfg.json'

    # record time args
    start_record_time = 'record time not set'
    chunk_count_update_timer = QTimer()
    chunk_count = 0

    # export parmas
    task_params = {
        'machine_ID':   None,
        'task_name':   None,
        'start_time':   None,
        'frame_count':   None,
        'sample_rate':   None,
        'frame_duration':   None,
        'chunk_len':   None,
        'channels':   None,
        'channel_names':   None,
        'writer_type':   None,
        'sensor_cfgs':   None,
    }

    def __init__(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.__init__)}')

        super().__init__()
        self.data_buffer_update_timer.timeout.connect(
            self.update_plot_data_buffer)
        self.chunk_count_update_timer.timeout.connect(
            self.update_cfg_chunk_count)

    def read_sensor_cfg_352C33(self, physical_channel, sensor_cfg_path):
        if PRINT_FUNC_NAME_FLAG:
            print(
                f'run function - {get_func_name(self.read_sensor_cfg_352C33)}')

        print(sys._getframe().f_code.co_name)
        sensor_model = '352C33'
        self.accel_chan_settings = AccelerometerChannelSettings(
            sensor_cfg_path, physical_channel)
        print(
            f'config path:{sensor_cfg_path}\n',
            f'Model : {sensor_model}\n',
            f'physical channel : {physical_channel}\n',
            f'channel name : {self.accel_chan_settings.name_to_assign_to_channel}\n',
            f'terminal config : {self.accel_chan_settings.terminal_config}\n',
            f'min value : {self.accel_chan_settings.min_val}\n',
            f'max value : {self.accel_chan_settings.max_val}\n',
            f'units : {self.accel_chan_settings.units}\n',
            f'sensitivity : {self.accel_chan_settings.sensitivity}\n',
            f'sensitivity units : {self.accel_chan_settings.sensitivity_units}\n',
            f'current excitation source : {self.accel_chan_settings.current_excit_source}\n',
            f'current excitation val : {self.accel_chan_settings.current_excit_val}\n',
            f'custom scale name : {self.accel_chan_settings.custom_scale_name}\n',
            f'sensor type : {self.accel_chan_settings.sensor_type}\n')
        self.all_channel_settings[self.accel_chan_settings.physical_channel] = self.accel_chan_settings

    def read_sensor_cfg_130F20(self, physical_channel, sensor_cfg_path):
        if PRINT_FUNC_NAME_FLAG:
            print(
                f'run function - {get_func_name(self.read_sensor_cfg_130F20)}')

        sensor_model = '130F20'
        self.mic_chan_settings = MicrophoneChannelSettings(
            sensor_cfg_path, physical_channel)
        print(
            f'config path:{sensor_cfg_path}\n',
            f'Model : {sensor_model}\n',
            f'physical channel : {physical_channel}\n',
            f'channel name : {self.mic_chan_settings.name_to_assign_to_channel}\n',
            f'terminal config : {self.mic_chan_settings.terminal_config}\n',
            f'min value : {self.mic_chan_settings.mic_sensitivity}\n',
            f'units : {self.mic_chan_settings.units}\n',
            f'mic sensitivity : {self.mic_chan_settings.mic_sensitivity}\n',
            f'max sound pressure level : {self.mic_chan_settings.max_snd_press_level}\n',
            f'current excitation source : {self.mic_chan_settings.current_excit_source}\n',
            f'current excitation val : {self.mic_chan_settings.current_excit_val}\n',
            f'custom scale name : {self.mic_chan_settings.custom_scale_name}\n',
            f'sensor type : {self.mic_chan_settings.sensor_type}\n')
        self.all_channel_settings[self.mic_chan_settings.physical_channel] = self.mic_chan_settings

    def create(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.create)}')

        try:
            print('try to clear task')
            self.clear()
        except:
            pass
        self.nidaq = NI9234(device_name=self.device_name)
        self.nidaq.create_task(task_name=self.task_name)
        for physical_channel, sensor_model, sensor_cfg_path in zip(self.channels, self.active_sensor_model_list, self.active_sensor_cfg_list):

            if sensor_model == '352C33':
                print('setting sensor config: 352C33')
                self.read_sensor_cfg_352C33(physical_channel, sensor_cfg_path)
                self.nidaq.add_accel_channel(
                    physical_channel=physical_channel,
                    name_to_assign_to_channel=self.accel_chan_settings.name_to_assign_to_channel,
                    terminal_config=self.accel_chan_settings.terminal_config,
                    min_val=self.accel_chan_settings.min_val,
                    max_val=self.accel_chan_settings.max_val,
                    units=self.accel_chan_settings.units,
                    sensitivity=self.accel_chan_settings.sensitivity,
                    sensitivity_units=self.accel_chan_settings.sensitivity_units,
                    current_excit_source=self.accel_chan_settings.current_excit_source,
                    current_excit_val=self.accel_chan_settings.current_excit_val,
                    custom_scale_name=self.accel_chan_settings.custom_scale_name)

            if sensor_model == '130F20':
                print('setting sensor config: 130F20')
                self.read_sensor_cfg_130F20(physical_channel, sensor_cfg_path)
                self.nidaq.add_microphone_channel(
                    physical_channel=physical_channel,
                    name_to_assign_to_channel=self.mic_chan_settings.name_to_assign_to_channel,
                    terminal_config=self.mic_chan_settings.terminal_config,
                    units=self.mic_chan_settings.units,
                    mic_sensitivity=self.mic_chan_settings.mic_sensitivity,
                    current_excit_source=self.mic_chan_settings.current_excit_source,
                    current_excit_val=self.mic_chan_settings.current_excit_val,
                    custom_scale_name=self.mic_chan_settings.custom_scale_name)

        self.nidaq.set_sample_rate(self.sample_rate)
        self.nidaq.set_frame_duration(self.frame_duration)
        self.nidaq.show_daq_params()
        self.nidaq.ready_read(callback_method=lambda foo1, foo2, foo3, foo4: self.nidaq.callback_method(
            self.nidaq.task._handle, self.nidaq.every_n_samples_event_type, self.nidaq.frame_size, callback_data=self.nidaq))

        self.data_buffer_update_timer.setInterval(self.frame_duration)
        self.chunk_len = int(self.sample_rate * self.frame_duration * 0.001)
        self.buffer_duration: int = self.frame_duration * self.buffer_rate
        self.wave_buffer_len: int = int(
            self.sample_rate * self.buffer_duration * 0.001)

        self.wave_data_buffer = np.zeros(
            (self.nidaq.task.number_of_channels, self.wave_buffer_len))
        self.spectrum_freqs = np.fft.rfftfreq(
            self.chunk_len, 1/self.sample_rate)
        # spectrum array format: (number of channels, buffer rate, chunk len)
        self.spectrum_data_buffer = np.zeros(
            (self.nidaq.task.number_of_channels, self.buffer_rate, self.spectrum_freqs.shape[0]))

    def start(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.start)}')
        self.nidaq.start_task()
        self.data_buffer_update_timer.start()
        self.wave_data_cycle_count = 0

    def stop(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.stop)}')

        if self.writer_switch_flag and self.nidaq.writer.file != None:
            self.stop_write_file()
        self.nidaq.stop_task()
        self.data_buffer_update_timer.stop()
        self.start_record_time = 'time_not_set'

    def clear(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.clear)}')

        self.nidaq.close_task()
        if self.nidaq.writer != None:
            if self.nidaq.writer.file != None:
                self.nidaq.writer.close_file()

    def start_write_file(self, mode):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.start_write_file)}')

        self.nidaq.set_writer_type(mode)
        self.nidaq.set_writer_enable()
        print(f'nidaq writer switch flag: {self.nidaq.writer_switch_flag}')
        if self.nidaq.writer_type == 'stream':
            self.write_stream_file()
        if self.nidaq.writer_type == 'segment':
            self.chunk_count_update_timer.setInterval(self.frame_duration)
            self.chunk_count_update_timer.start()
            self.write_segment_file()

        self.write_record_info()

    def stop_write_file(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.stop_write_file)}')
        self.chunk_count_update_timer.stop()
        self.get_current_write_file_count()
        self.nidaq.set_writer_disable()
        if self.nidaq.writer_type == 'stream':
            self.nidaq.writer.close_file()

        self.task_params['frame_count'] = self.chunk_count
        self.write_record_info()

    def write_record_info(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.write_record_info)}')

        self.task_params = {
            'machine_ID':   self.machine_name,
            'task_name':   self.task_name,
            'start_time':   self.start_record_time,
            'frame_count':   self.chunk_count,
            'sample_rate':   self.sample_rate,
            'frame_duration':   self.frame_duration,
            'chunk_len':   self.chunk_len,
            'channels':   self.channels,
            'channel_names':   self.nidaq.task.ai_channels.channel_names,
            # 'data_names'  :   []
            'writer_type':   self.nidaq.writer.writer_type,
            'sensor_cfgs':   list(),
        }

        for sensor_cfg_path in self.active_sensor_cfg_list:
            with open(sensor_cfg_path) as sensor_cfg_file:
                sensor_cfg = json.load(sensor_cfg_file)
            self.task_params['sensor_cfgs'].append(sensor_cfg)

        self.export_path = os.path.join(
            self.record_dir, self.export_cfg_file_name)
        with open(self.export_path, 'w') as file:
            json.dump(self.task_params, file)
        print(f'export task params: {self.task_params}')

    def update_cfg_chunk_count(self):
        self.get_current_write_file_count()
        self.task_params['frame_count'] = self.chunk_count
        with open(self.export_path, 'w') as file:
            json.dump(self.task_params, file)
        print(f'update chunk count: {self.task_params["frame_count"]}')

    def get_current_write_file_count(self):
        if PRINT_FUNC_NAME_FLAG:
            print(
                f'run function - {get_func_name(self.get_current_write_file_count)}')

        if self.nidaq.writer.writer_type == 'segment':
            self.chunk_count = self.nidaq.writer.write_file_count
        elif self.nidaq.writer.writer_type == 'stream':
            self.chunk_count = 0

    def write_stream_file(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.write_stream_file)}')
        '''
        write all signal to one file while this function is working
        '''
        self.start_record_time = datetime.now().strftime("%Y%m%dT%H%M%S")
        self.task_dir = os.path.join(self.write_file_directory, self.task_name)
        print(f'record path: {self.task_dir}')
        if not os.path.isdir(self.task_dir):
            os.mkdir(self.task_dir)
        self.record_dir = os.path.join(self.task_dir, self.start_record_time)
        if not os.path.isdir(self.record_dir):
            os.mkdir(self.record_dir)
        self.nidaq.writer.set_directory(self.record_dir)
        file_path = f'{self.task_name}_{datetime.now().strftime("%Y%m%dT%H%M%S")}.csv'
        self.nidaq.writer.set_file_name(file_path)
        self.nidaq.writer.open_file()

    def write_segment_file(self, period=10):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.write_segment_file)}')
        '''
        period : seconds, define a time period for a file
        '''
        self.start_record_time = datetime.now().strftime("%Y%m%dT%H%M%S")
        self.task_dir = os.path.join(self.write_file_directory, self.task_name)
        print(f'record path: {self.task_dir}')
        if not os.path.isdir(self.task_dir):
            os.mkdir(self.task_dir)
        self.record_dir = os.path.join(self.task_dir, self.start_record_time)
        if not os.path.isdir(self.record_dir):
            os.mkdir(self.record_dir)
        self.nidaq.writer.set_directory(self.record_dir)
        self.nidaq.writer.reset_write_file_count()

    def update_plot_data_buffer(self):
        if PRINT_FUNC_NAME_FLAG:
            print(
                f'run function - {get_func_name(self.update_plot_data_buffer)}')

        self.wave_data_buffer = np.roll(
            self.wave_data_buffer, self.chunk_len)
        self.wave_data_buffer[:, :self.chunk_len] = self.nidaq.chunk

        self.spectrum_data = np.abs(np.fft.rfft(self.nidaq.chunk))
        self.spectrum_data[:, 0] = 0  # suppress 0 Hz to 0
        self.spectrum_data_buffer = np.roll(
            self.spectrum_data_buffer, 1, axis=1)
        for i in range(self.spectrum_data.shape[0]):
            self.spectrum_data_buffer[i, 0, :] = self.spectrum_data[i]
        self.wave_data_buffer_mean = np.mean(np.abs(self.wave_data_buffer))

    def get_wave_data_buffer(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.get_wave_data_buffer)}')

        return self.wave_data_buffer

    def get_spectrum_data_buffer(self):
        if PRINT_FUNC_NAME_FLAG:
            print(
                f'run function - {get_func_name(self.get_spectrum_data_buffer)}')

        return self.spectrum_data_buffer

    def get_spectrum_freqs(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.get_spectrum_freqs)}')

        return self.spectrum_freqs

    def get_wave_buffer_len(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.get_wave_buffer_len)}')

        return self.wave_buffer_len

    def get_wave_buffer_mean(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.get_wave_buffer_mean)}')

        print(f'wave mean:{np.abs(self.wave_data_buffer_mean)}')
        return self.wave_data_buffer_mean

    def get_abnormal_flag(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.get_abnormal_flag)}')

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

    def record_cfg_checker(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.record_cfg_checker)}')
        ...
