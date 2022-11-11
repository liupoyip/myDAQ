from TranslateObjectID import create_callback_data_id, get_callback_data_from_id, MyList

import os
import queue
from datetime import datetime
from typing import Union

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
import matplotlib.pyplot as plt

callback_data = MyList()
callback_data_id = create_callback_data_id(callback_data)
WRITE_CSV_TRIG = False
callback_data.append(WRITE_CSV_TRIG)
chunk = None
daq = None


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
        super().__init__()

    def show_local_deivce(self):
        for device in self.system.devices:
            print(device)

    def show_driver_version(self):
        print(self.system.driver_version)

    def check_device_is_exsit(self,):
        if len(self.system.devices) == 0:
            raise BaseException('Cannot find local device.')


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
        self.create_task(task_name)

    def clear_task(self):
        if self.task != None:
            self.task.close()

    def create_task(self, task_name: str):
        self.task = nidaqmx.Task(new_task_name=task_name)

    def add_ai_channel(self, channel):
        # TODO: refactor to decorater, with analog input channel
        # target function: add_accel_channel, add_microphone_channel
        pass

    def add_accel_channel(self, channel: Union[int, str]):
        if channel not in self.channel_num_list:
            raise BaseException(f'Illegal channel number. Legal channel : {self.channel_num_list}')
        if len(self.task.channel_names) > 4:
            raise BaseException(f'All channels have added to task.')

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
        self.task.timing.cfg_samp_clk_timing(
            rate=self.sample_rate, sample_mode=AcquisitionType.CONTINUOUS)
        print(f'Channel added, exist channel: {self.task.channel_names}')
        self.exist_channel_quantity = len(self.task.channel_names)
        self.set_buffer_size()

    def add_microphone_channel(self, channel: Union[int, str]):
        if channel not in self.channel_num_list:
            raise BaseException(f'Illegal channel number. Legal channel : {self.channel_num_list}')
        if len(self.task.channel_names) > 4:
            raise BaseException(f'All channels have added to task.')

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
        self.task.timing.cfg_samp_clk_timing(
            rate=self.sample_rate, sample_mode=AcquisitionType.CONTINUOUS)
        print(f'Channel added, exist channel: {self.task.channel_names}')
        self.exist_channel_quantity = len(self.task.channel_names)
        self.set_buffer_size()

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
        print(f'Device name: {self.device_name}')
        self.show_device_channel_names()
        print(f'max sampling rate: {self.max_sample_rate} Hz (single and multiple channel)')
        print(f'min sampling rate: {self.min_sample_rate} Hz')
        print(f'Sampling rate: {self.sample_rate} Hz')
        print(f'Frame duration: {self.frame_duration} ms')
        print(f'Frame size: {self.frame_size}')
        print(f'Buffer Size: {self.buffer_size}')
        print(f'Task exist channel num: {len(self.task.channel_names)}')
        self.show_task_exist_channels()
        print(f'Chunk size: [{self.exist_channel_quantity}, {self.frame_size}]')

    def show_device_channel_names(self):
        print(f'{self.device_name} channels:')
        for name in list(self.device.ai_physical_chans):
            print(f'  {str(name)}')

    def show_task_exist_channels(self):
        print('Task exist_channels:')
        for channel_name in self.task.channel_names:
            print(f'  {channel_name}')

    def show_max_sample_rate(self):
        print(self.max_sample_rate)

    def show_daq_chassis_device_name(self):
        print(self.device.compact_daq_chassis_device)

    def start_streaming(self):
        global chunk
        self.task.register_every_n_samples_acquired_into_buffer_event(
            sample_interval=self.frame_size,
            callback_method=callback_NI9234)
        callback_data.clear()
        chunk = np.zeros((self.exist_channel_quantity, self.frame_size))
        callback_data.append(WRITE_CSV_TRIG)
        callback_data.append(self.task)
        callback_data.append(chunk)
        self.task.start()
        input('Running task. Press Enter to stop and see number of '
              'accumulated samples.\n')
        self.task.stop()
        print('Task is done!!')

    def close_task(self):
        self.task.close()
        print('Task is closed.')


class CSVStreamWriter:
    def __init__(self, directory: str, file_name: str):
        self.directory = directory
        self.file_name = file_name
        self.check_file_extension()
        self.file_path = os.path.join(self.directory, self.file_name)
        self.file = None
        self.open_file()

    def write_csv_on(self):
        global WRITE_CSV_TRIG
        WRITE_CSV_TRIG = True

    def write_csv_off(self):
        global WRITE_CSV_TRIG
        WRITE_CSV_TRIG = False

    def open_file(self):
        self.file = open(self.file_path, mode='a')

    def close_file(self):
        self.file.close()

    def check_file_extension(self):
        name, extension = os.path.splitext(self.file_name)
        if extension != '.csv':
            raise BaseException('Illegal file extension, *.csv required.')

    def write(self):
        global chunk
        np.savetxt(fname=self.file, X=np.transpose(chunk), delimiter=',')


def callback_NI9234(task_handle, every_n_samples_event_type,
                    number_of_samples, foo):
    global chunk
    # get data from memory address and retrieve
    callback_data = get_callback_data_from_id(callback_data_id)
    WRITE_CSV_TRIG = callback_data[0]
    task = callback_data[1]
    chunk = callback_data[2]

    stream_reader = NiStreamReaders.AnalogMultiChannelReader(task.in_stream)
    stream_reader.read_many_sample(chunk)
    if WRITE_CSV_TRIG:
        csv_stream_writer.write()
    print(datetime.now().isoformat(sep=' ', timespec='milliseconds'))
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
    directory = '.'
    file_name = 'foo.csv'
    csv_stream_writer = CSVStreamWriter(directory, file_name)
    csv_stream_writer.write_csv_on()

    ni9234 = NI9234(device_name='NI_9234', task_name='myTask')
    ni9234.add_accel_channel(0)
    ni9234.add_microphone_channel(1)
    ni9234.set_frame_duration(100)
    ni9234.set_sample_rate(12800)
    ni9234.start_streaming()
    ni9234.close_task()
    csv_stream_writer.write_csv_off()
    csv_stream_writer.close_file()
