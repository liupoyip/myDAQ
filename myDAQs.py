from typing import Optional, Union
import ctypes
import asyncio
from datetime import datetime

import keyboard
import nidaqmx
import nidaqmx.system
import nidaqmx.system.device
import nidaqmx.task
from nidaqmx import stream_readers as NiStreamReaders
from nidaqmx.constants import (AcquisitionType,
                               TerminalConfiguration,
                               AccelUnits,
                               AccelSensitivityUnits,
                               SoundPressureUnits,
                               ExcitationSource)
# DigitalWidthUnits)
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


class GeneralDAQParams:
    device: Optional[str]
    sample_rate: Optional[float]
    record_duration: Optional[float]
    frame_duration: Optional[float]  # millisecond
    exist_channel_quantity: Optional[int]
    buffer_size: Optional[int]


class NIDAQ(GeneralDAQParams):
    system = nidaqmx.system.System.local()
    stream_trig: Optional[bool] = False
    task: Optional[nidaqmx.task.Task] = None
    device: Optional[nidaqmx.system.device.Device] = None

    def __init__(self):
        super(NIDAQ, self).__init__()

        self.sample_rate: Optional[float] = 12800
        self.record_duration: Optional[float] = 5.0
        self.frame_duration: Optional[int] = 1000  # millisecond
        self.exist_channel_quantity: Optional[int] = 0
        self.frame_size: Optional[int] = int(self.sample_rate * self.frame_duration*0.001)
        self.buffer_size: Optional[int] = self.frame_size * 5
        self.device_name: Optional[str] = None
        self.min_sample_rate: Optional[float] = None
        self.max_sample_rate: Optional[float] = None

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
        self.task = nidaqmx.task.Task(new_task_name=task_name)

    def clear_task(self):
        if self.task != None:
            self.task.close()


class NI9234(NIDAQ):
    channel_num_list = (0, 1, 2, 3, '0', '1', '2', '3')
    chunk: np.float64
    callback_data_ptr = ctypes.py_object(NiCallbackDataList())
    stream_reader: NiStreamReaders.AnalogMultiChannelReader

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
                raise BaseException('All channels have added to task.')

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

    def set_stream_on(self):
        self.stream_trig = True

    def set_stream_off(self):
        self.stream_trig = False

    def ready_read(self, callback_method):
        self.callback_data_ptr.value.clear()

        print('Ready to stream.\n'
              'Press\n'
              '  "s" to start'
              '  "p" to stop')

        self.task.register_every_n_samples_acquired_into_buffer_event(
            sample_interval=self.frame_size,
            callback_method=callback_method)

        self.chunk = np.zeros((self.exist_channel_quantity, self.frame_size))
        self.stream_reader = NiStreamReaders.AnalogMultiChannelReader(self.task.in_stream)
        self.callback_data_ptr.value.append(self.stream_reader)
        self.callback_data_ptr.value.append(self.chunk)

    def start_task(self):
        self.task.start()

    def start_streaming_period_time(self, time: Union[float, int]):
        """
        time: second
        """
        number_of_samples: int = int(time * self.sample_rate)
        return self.task.in_stream.read(number_of_samples_per_channel=number_of_samples)

    async def async_streaming(self):
        self.task.start()

    def stop_task(self):
        self.task.stop()
        print('Task is stopped!!')

    def close_task(self):
        self.set_stream_off()
        self.task.close()
        print('Task is done!!')

    async def key_stop_event(self):
        while True:
            await asyncio.sleep(0.1)
            if keyboard.is_pressed('q'):
                self.set_stream_off()
                print('stop streamming')
                break

    async def key_switch_event(self):
        while True:
            await asyncio.sleep(0.1)
            if keyboard.is_pressed('s') and not self.stream_trig:
                self.set_stream_on()
                self.task.start()
                print('start streaming')
            elif keyboard.is_pressed('p'):
                self.set_stream_off()
                print('stop streamming')
            elif keyboard.is_pressed('q'):
                self.set_stream_off()
                self.close_task()
                print('close task')
                break


def callback_NIDAQ(task_handle, every_n_samples_event_type,
                   number_of_samples, callback_data):
    stream_reader = niDAQ.callback_data_ptr.value[0]
    chunk = niDAQ.callback_data_ptr.value[1]
    stream_reader.read_many_sample(chunk)

    current_time = datetime.now().isoformat(sep=' ', timespec='milliseconds')
    print(
        f'Current time: {current_time} Recording... every {number_of_samples} Samples callback invoked. stream trig: {niDAQ.stream_trig}\n'
        'Press "p" to stop streaming, "q" to quit program.')

    if not niDAQ.stream_trig:
        niDAQ.stop_task()
    return 0


if __name__ == '__main__':
    niDAQ = NI9234(device_name='NI_9234', task_name='myTask')
    niDAQ.add_accel_channel(0)
    niDAQ.add_accel_channel(1)
    # niDAQ.add_microphone_channel(2)
    # niDAQ.add_microphone_channel(3)
    # tasks = [niDAQ.key_stop_event()]
    # asyncio.run(asyncio.wait(tasks))
    niDAQ.set_frame_duration(50)
    niDAQ.set_sample_rate(25600)
    niDAQ.ready_read(callback_method=callback_NIDAQ)

    # method 1 thread
    # thread = BaseThread(name='streaming', target=niDAQ.start_task(), callback=callback_NIDAQ)
    # thread.start()

    # method 2 async function with event loop
    # loop = asyncio.get_event_loop()
    # tasks = [asyncio.ensure_future(niDAQ.key_switch_event())]
    # loop.run_until_complete(asyncio.wait(tasks))

    # method 3 async run (similiar with method 2)
    tasks = [niDAQ.key_switch_event()]
    asyncio.run(asyncio.wait(tasks))

    # method 4 read with period time
    # niDAQ.start_streaming(callback_method=callback_NIDAQ)
    # data = niDAQ.start_streaming_period_time(10)    # only read ch0??
    # print(data.shape)

    # niDAQ.close_task()
