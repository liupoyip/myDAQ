"""
TODO
NI9234 未來要新增的功能: remove ai channel
"""

# %%
import queue
from datetime import datetime
from dataclasses import dataclass
import weakref
from typing import Union

import nidaqmx
from nidaqmx import stream_readers as NiStreamReaders
from nidaqmx.constants import AcquisitionType
import sounddevice as sd

import numpy as np
import matplotlib.pyplot as plt

_id_to_obj_dict = weakref.WeakValueDictionary()


def create_callback_data_id(obj):
    """
    Uses the weakref module to create and store a reference to obj

    output value: reference to the object

    It is not possible to directly uses python object through a Callback function because
    with ctypes there is no pointer to python object.
    This function store in a dictionary a reference to an object
    This object can be retrieved using the get_callbackdata_from_id function

    For python object that cannot be weakreferenced, one can creat a dummy class to wrap
    the python object :
        def MyList(list)
            pass

        data = MyList()
        id = create_callbackdata_id(data)

    """
    obj_id = id(obj)
    _id_to_obj_dict[obj_id] = obj
    return obj_id


def get_callback_data_from_id(obj_id):
    """
    Retrieve an object stored using create_callbackdata_id
    """
    return _id_to_obj_dict[obj_id]


class MyList(list):
    pass


callback_data = MyList()
callback_data_id = create_callback_data_id(callback_data)


@dataclass
class GeneralDAQParams:
    device: str = None
    sample_rate: int = 12800
    record_duration: float = 1.0
    frame_duration: float = 1000.0  # millisecond
    exist_channel_quantity: int = 0
    downsample: float = 1   # Down sampling ratio, greater than 1
    buffer_size: int = sample_rate * 5


@dataclass
class NIDAQ(GeneralDAQParams):

    system = nidaqmx.system.System.local()
    task = None

    def __init__(self):
        super().__init__()

    def show_local_deivce(self):
        for device in self.system.devices:
            print(device)

    def show_driver_version(self):
        print(self.system.driver_version)

    def check_device_is_exsit(self,):
        if len(self.system.devices) == 0:
            raise BaseException('Cannot find local device.')


@dataclass
class NI9234(NIDAQ):
    channel_num_list = (0, 1, 2, 3, '0', '1', '2', '3')

    def __init__(self, device_name, task_name):
        super().__init__()
        self.device_name = device_name
        self.device = nidaqmx.system.device.Device(device_name)
        self.device.reset_device()
        # sampling rate of multi-channel and single-channel is same in NI-9234
        self.max_sample_rate = self.device.ai_max_single_chan_rate
        self.min_sample_rate = self.device.ai_min_rate
        self.frame_size = int(self.sample_rate * self.frame_duration * 0.001)
        self.buffer_size = self.frame_size * 10
        self.chunk = None
        self.create_task(task_name)

    def clear_task(self):
        if self.task != None:
            self.task.close()

    def create_task(self, task_name: str):
        self.task = nidaqmx.Task(new_task_name=task_name)

    def add_ai_channel(self, channel):
        # refactor to decorater, with analog input channel
        # target function: add_accel_channel, add_microphone_channel
        pass

    def add_accel_channel(self, channel: Union[int, str]):
        if channel not in self.channel_num_list:
            raise BaseException(f'Illegal channel number. Legal channel : {self.channel_num_list}')
        if len(self.task.channel_names) > 4:
            raise BaseException(f'All channels have added to task.')

        self.task.ai_channels.add_ai_accel_chan(f'{self.device_name}/ai{channel}')
        self.task.timing.cfg_samp_clk_timing(
            rate=self.sample_rate, sample_mode=AcquisitionType.CONTINUOUS)
        self.set_buffer_size()
        print(f'Channel added, exist channel: {self.task.channel_names}')
        self.exist_channel_quantity = len(self.task.channel_names)

    def add_microphone_channel(self, channel: Union[int, str]):
        if channel not in self.channel_num_list:
            raise BaseException(f'Illegal channel number. Legal channel : {self.channel_num_list}')
        if len(self.task.channel_names) > 4:
            raise BaseException(f'All channels have added to task.')

        self.task.ai_channels.add_ai_accel_chan(f'{self.device_name}/ai{channel}')
        self.task.timing.cfg_samp_clk_timing(
            rate=self.sample_rate, sample_mode=AcquisitionType.CONTINUOUS)
        self.set_buffer_size()
        print(f'Channel added, exist channel: {self.task.channel_names}')
        self.exist_channel_quantity = len(self.task.channel_names)

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

    def show_daq_params(self):
        self.show_device_channel_names()
        print(f'{self.device_name} max sampling rate: {self.max_sample_rate} Hz')
        print(f'{self.device_name} min sampling rate: {self.min_sample_rate} Hz')
        print(f'Sampling rate: {self.sample_rate} Hz')
        print(f'Frame duration: {self.frame_duration} ms')
        print(f'Buffer Size: {self.buffer_size}')
        print(f'Task exist channel num: {len(self.task.channel_names)}')
        self.show_task_exist_channels()
        print(f'Chunk size: [{self.exist_channel_quantity}, {self.frame_size}]')

    def show_device_channel_names(self):
        print(f'{self.device_name} channels:')
        for name in list(self.device.ai_physical_chans):
            print(f'\t{name}')
        print('\t\n'.join(str(name) for name in list(self.device.ai_physical_chans)))

    def show_task_exist_channels(self):
        print('Task exist_channels:')
        print('\t\n'.join(str(name) for name in self.task.channel_names))

    def show_max_sample_rate(self):
        print(self.max_sample_rate)

    def show_daq_chassis_device_name(self):
        print(self.device.compact_daq_chassis_device)

    def start_streaming(self):
        self.task.register_every_n_samples_acquired_into_buffer_event(
            sample_interval=self.frame_size,
            callback_method=callback_NI9234)
        callback_data.clear()
        self.chunk = np.zeros((self.exist_channel_quantity, self.frame_size))
        callback_data.append(self.task)
        callback_data.append(self.chunk)
        self.task.start()
        input('Running task. Press Enter to stop and see number of '
              'accumulated samples.\n')
        print(self.task.is_task_done())
        self.task.stop()
        self.task.close()
        print('task:', self.task, 'task len:', len(self.task))


def stream_to_csv():
    pass


def callback_NI9234(task_handle, every_n_samples_event_type,
                    number_of_samples, foo):
    # get data from memory address and retrieve
    callback_data = get_callback_data_from_id(callback_data_id)
    task = callback_data[0]
    chunk = callback_data[1]
    print(datetime.now().isoformat(sep=' ', timespec='milliseconds'))
    stream_reader = NiStreamReaders.AnalogMultiChannelReader(task.in_stream)
    stream_reader.read_many_sample(chunk)
    print(f'Every {number_of_samples} Samples callback invoked.')
    return 0


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


# %%
if __name__ == '__main__':
    ni9234 = NI9234(device_name='NI_9234', task_name='myTask')
    ni9234.add_accel_channel(0)
    ni9234.add_microphone_channel(1)
    ni9234.set_frame_duration(100)
    ni9234.set_sample_rate(51200)
    ni9234.start_streaming()
