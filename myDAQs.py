import queue
from typing import Union
import ctypes

import nidaqmx
from nidaqmx import stream_readers as NiStreamReaders
from nidaqmx.constants import (AcquisitionType,
                               TerminalConfiguration,
                               AccelUnits,
                               AccelSensitivityUnits,
                               SoundPressureUnits,
                               ExcitationSource)
import sounddevice as sd
import numpy as np
from PySide6.QtCore import Signal, QObject


class ValueChangedSignalEmitter(QObject):
    valueChanged = Signal(int)

    def __init__(self, parent=None):
        super(ValueChangedSignalEmitter, self).__init__(parent)
        self._value = 0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self.valueChanged.emit(value)
        print('value emit!')


class NiCallbackDataList(list):
    """
    Properties:
        list[0]: NiStreamReaders.AnalogMultiChannelReader
            stream_reader for nidaqmx
            ```
            stream_reader = NiStreamReaders.AnalogMultiChannelReader(nidaqmx.Task.in_stream)
            ```
        list[1]: numpy.array
            chunk for acquiring data

    Limitation: max length is 3
    """

    def __init__(self):
        self.max_len = 3

    def append(self, item):
        if len(self) < self.max_len:
            super().append(item)
        else:
            raise BaseException(
                f'Too many elements. {self.__class__.__name__} max length is {self.max_len} ')


niDAQ = None  # default variable for DAQ object instance
callback_data = NiCallbackDataList()
callback_data_ptr = ctypes.py_object(callback_data)


class GeneralDAQParams:
    device: str = None
    sample_rate: int = 12800
    record_duration: float = 1.0
    frame_duration: float = 1000.0  # millisecond
    exist_channel_quantity: int = 0
    downsample: float = 1   # Down sampling ratio, greater than 1
    buffer_size: int = sample_rate * 5


class NIDAQ(GeneralDAQParams):
    system = nidaqmx.system.System.local()
    task = None

    def __init__(self):
        super(NIDAQ, self).__init__()

    def show_local_deivce(self):
        for device in self.system.devices:
            print(device)

    def show_driver_version(self):
        print(self.system.driver_version)

    def check_device_is_exsit(self,):
        if len(self.system.devices) == 0:
            raise BaseException('Cannot find local device.')

    def show_daq_params(self):
        self.show_daq_chassis_device_name()
        self.show_device_name()
        self.show_device_channel_names()
        self.show_sample_rate_range()
        self.show_sample_rate()
        print(f'Frame duration: {self.frame_duration} ms')
        print(f'Frame size: {self.frame_size}')
        print(f'Buffer Size: {self.buffer_size}')
        self.show_task_exist_channels()
        print(f'Chunk size: [{self.exist_channel_quantity}, {self.frame_size}]')

    def show_device_name(self):
        print(f'Device name: {self.device_name}')

    def show_device_channel_names(self):
        print(f'{self.device_name} channels:')
        print(''.join(f'  {name}\n' for name in list(self.device.ai_physical_chans)))

    def show_task_exist_channels(self):
        print(f'Task exist channel num: {len(self.task.channel_names)}')
        print('Task exist_channels:')
        print(''.join(f'  {channel_name}\n' for channel_name in self.task.channel_names))

    def show_sample_rate(self):
        print(f'Current sampling rate: {self.sample_rate} Hz')

    def show_sample_rate_range(self):
        print(f'Sampling rate range: {self.min_sample_rate:.2f} ~ {self.max_sample_rate} Hz')

    def show_daq_chassis_device_name(self):
        print(f'DAQ chassis name: {self.device.compact_daq_chassis_device}')

    def create_task(self, task_name: str):
        self.task = nidaqmx.Task(new_task_name=task_name)

    def clear_task(self):
        if self.task != None:
            self.task.close()


class NI9234(NIDAQ):
    channel_num_list = (0, 1, 2, 3, '0', '1', '2', '3')

    def __init__(self, device_name, task_name):
        super(NI9234, self).__init__()
        self.device_name = device_name
        self.device = nidaqmx.system.device.Device(device_name)
        self.device.reset_device()
        # max/min sampling rate of multi-channel and single-channel is same in NI-9234
        self.max_sample_rate = self.device.ai_max_single_chan_rate
        self.min_sample_rate = self.device.ai_min_rate
        self.frame_size = int(self.sample_rate * self.frame_duration * 0.001)
        self.buffer_size = self.frame_size * 10
        self.create_task(task_name)

    def clear_task(self):
        if self.task != None:
            self.task.close()

    def create_task(self, task_name: str):
        self.task = nidaqmx.Task(new_task_name=task_name)

    def add_ai_channel(add_ai_channel_func):
        def wrap(self, channel: Union[int, str]):
            if channel not in self.channel_num_list:
                raise BaseException(
                    f'Illegal channel number. Legal channel : {self.channel_num_list}')
            if len(self.task.channel_names) > 4:
                raise BaseException(f'All channels have added to task.')

            add_ai_channel_func(self, channel)

            self.task.timing.cfg_samp_clk_timing(
                rate=self.sample_rate, sample_mode=AcquisitionType.CONTINUOUS)
            print(f'Channel added, exist channel: {self.task.channel_names}')
            self.exist_channel_quantity = len(self.task.channel_names)
            self.set_buffer_size()
        return wrap

    @add_ai_channel
    def add_accel_channel(self, channel: Union[int, str]):
        self.task.ai_channels.add_ai_accel_chan(
            physical_channel=f'{self.device_name}/ai{channel}',
            name_to_assign_to_channel=f'{self.device_name}-ch{channel}-accelerometer',
            terminal_config=TerminalConfiguration.DEFAULT,
            min_val=-5.0,
            max_val=5.0,
            units=AccelUnits.G,
            sensitivity=1000.0,
            sensitivity_units=AccelSensitivityUnits.MILLIVOLTS_PER_G,
            current_excit_source=ExcitationSource.INTERNAL,
            current_excit_val=0.004,
            custom_scale_name='')

    @add_ai_channel
    def add_microphone_channel(self, channel: Union[int, str]):
        self.task.ai_channels.add_ai_microphone_chan(
            physical_channel=f'{self.device_name}/ai{channel}',
            name_to_assign_to_channel=f'{self.device_name}-ch{channel}-microphone',
            terminal_config=TerminalConfiguration.DEFAULT,
            units=SoundPressureUnits.PA,
            mic_sensitivity=10.0,
            max_snd_press_level=100.0,
            current_excit_source=ExcitationSource.INTERNAL,
            current_excit_val=0.004,
            custom_scale_name='')

    def set_sample_rate(self, sample_rate: float):
        self.sample_rate = sample_rate
        self.task.timing.cfg_samp_clk_timing(
            rate=self.sample_rate, sample_mode=AcquisitionType.CONTINUOUS)
        self.set_buffer_size()

    def set_frame_duration(self, frame_duration: int):
        self.frame_duration = frame_duration
        self.set_buffer_size()

    def set_buffer_size(self):
        self.frame_size = int(self.sample_rate * self.frame_duration * 0.001)
        self.buffer_size = self.frame_size * self.exist_channel_quantity * 10
        self.task.in_stream.input_buf_size = self.buffer_size

    def start_streaming(self, callback_method=None):
        if callback_method != None:
            self.task.register_every_n_samples_acquired_into_buffer_event(
                sample_interval=self.frame_size,
                callback_method=callback_method)
            callback_data.clear()
            chunk = np.zeros((self.exist_channel_quantity, self.frame_size))
            stream_reader = NiStreamReaders.AnalogMultiChannelReader(self.task.in_stream)
            callback_data.append(stream_reader)
            callback_data.append(chunk)

        self.task.start()
        input('Running task.\n'
              'Press Enter to stop and see number of accumulated samples.\n')
        self.task.stop()
        print('Task is done!!')

    def close_task(self):
        self.task.close()
        print('Task is closed.')


class AudioRecorder:
    def __init__(self, fs, window, channels):
        self.name = "audio recorder"
        self.fs = fs
        self.channels = channels  # specific channel list
        self.window = window    # interval of each frame (ms)
        self.frame_size = int(self.fs * self.window * 0.001)
        self.trigger = False
        self.downsample = 1  # down sampling ratio (greater than 1)
        # self.input_device = sd.default.device
        self.input_device = 2
        # mapping channel index
        self.mapping = [c - 1 for c in (self.channels)]
        self.max_qsize = 20
        self.queue_plot_data = queue.Queue(maxsize=self.max_qsize)
        self.queue_raw_data = queue.Queue(maxsize=self.max_qsize)
        self.stream = sd.InputStream(
            device=self.input_device,
            channels=max(self.channels),
            samplerate=self.fs,
            callback=self.audio_callback,
            blocksize=self.frame_size,
            latency="low",
        )
        self.pa_ref = 0.00002  # pa ref

        self.plot_len = int(self.frame_size / self.downsample)

    def audio_callback(self, indata, frames, time, status):

        # print("doing audio callback, chunk length:", len(indata))
        # print("print part of input data:", indata[0], indata[1])
        self.queue_plot_data.put(np.squeeze(
            indata[:: self.downsample, self.mapping]))
        self.queue_raw_data.put(np.squeeze(indata[:, self.mapping]))
        print("recording")

    def start_streaming(self):
        print("doing start_streaming Function")
        self.stream.start()
        print("stream active:", self.stream.active)

    def stop_streaming(self):
        print("doing stop_streaming Function")
        self.stream.stop()
        print("stream active:", self.stream.active)


if __name__ == '__main__':
    niDAQ = NI9234(device_name='NI_9234', task_name='myTask')
    niDAQ.add_accel_channel(0)
    niDAQ.add_microphone_channel(1)
    niDAQ.set_frame_duration(100)
    niDAQ.set_sample_rate(12800)
    niDAQ.start_streaming()
    niDAQ.close_task()
