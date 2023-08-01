from typing import Optional, Union
import asyncio
from datetime import datetime
import dataclasses

import keyboard
import nidaqmx
import nidaqmx.system
import nidaqmx.system.device
import nidaqmx.system.system
import nidaqmx.task
from nidaqmx import stream_readers as NiStreamReaders
from nidaqmx.constants import (AcquisitionType,
                               TerminalConfiguration,
                               AccelUnits,
                               AccelSensitivityUnits,
                               SoundPressureUnits,
                               ExcitationSource,
                               EveryNSamplesEventType)
import numpy as np
import numpy.typing as npt

from .utils import CSVStreamWriter, NPYWriter
from .utils import get_func_name
from debug_flags import PRINT_FUNC_NAME_FLAG


@dataclasses.dataclass
class GeneralDAQParams:

    sample_rate: Optional[float] = None
    record_duration: Optional[float] = None
    frame_duration: Optional[int] = None  # millisecond
    frame_size: Optional[int] = None
    buffer_size: Optional[int] = None


class NIDAQ(GeneralDAQParams):

    system: Optional[nidaqmx.system.system.System] = None
    stream_switch_flag: Optional[bool] = None
    task: Optional[nidaqmx.task.Task] = None
    device: Optional[nidaqmx.system.device.Device] = None
    device_name: Optional[str] = None
    min_sample_rate: Optional[float] = None
    max_sample_rate: Optional[float] = None
    stream_reader: Optional[NiStreamReaders.AnalogMultiChannelReader] = None
    stream_writer: Optional[CSVStreamWriter] = None
    segment_writer: Optional[NPYWriter] = None
    writer: Optional[Union[CSVStreamWriter, NPYWriter]] = None
    writer_switch_flag: Optional[bool] = None
    chunk: Optional[npt.NDArray[np.float64]] = None
    # "stream" for *.csv / "segment" for *.npy
    writer_type: Optional[str] = None

    def __init__(self) -> None:
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.__init__)}')

        super(NIDAQ, self).__init__()

    def show_local_deivce(self) -> None:
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.show_local_deivce)}')

        for device in self.system.devices:
            print(device)

    def show_driver_version(self) -> None:
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.show_driver_version)}')

        print(self.system.driver_version)

    def check_device_is_exsit(self) -> None:
        if PRINT_FUNC_NAME_FLAG:
            print(
                f'run function - {get_func_name(self.check_device_is_exsit)}')

        if len(self.system.devices) == 0:
            raise BaseException('Cannot find local device.')

    def start_task(self) -> None:
        pass

    def stop_task(self) -> None:
        pass

    def show_daq_params(self) -> None:
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.show_daq_params)}')

        self.show_daq_chassis_device_name()
        self.show_device_name()
        self.show_device_channel_names()
        self.show_sample_rate_range()
        self.show_sample_rate()
        print(f'Frame duration: {self.frame_duration} ms')
        print(f'Frame size: {self.frame_size}')
        print(f'Buffer Size: {self.buffer_size}')
        self.show_task_exist_channels()
        print(
            f'Chunk size: [{self.task.number_of_channels}, {self.frame_size}]')

    def show_device_name(self) -> None:
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.show_device_name)}')
        print(f'Device name: {self.device_name}')

    def show_device_channel_names(self) -> None:
        if PRINT_FUNC_NAME_FLAG:
            print(
                f'run function - {get_func_name(self.show_device_channel_names)}')

        print(f'{self.device_name} channels:')
        print(''.join(f'  {name}\n' for name in list(
            self.device.ai_physical_chans)))

    def show_task_exist_channels(self) -> None:
        if PRINT_FUNC_NAME_FLAG:
            print(
                f'run function - {get_func_name(self.show_task_exist_channels)}')

        print(f'Task exist channel num: {len(self.task.channel_names)}')
        print('Task exist_channels:')
        print(
            ''.join(f'  {channel_name}\n' for channel_name in self.task.channel_names))

    def show_sample_rate(self) -> None:
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.show_sample_rate)}')

        print(f'Current sampling rate: {self.sample_rate} Hz')

    def show_sample_rate_range(self) -> None:
        if PRINT_FUNC_NAME_FLAG:
            print(
                f'run function - {get_func_name(self.show_sample_rate_range)}')

        print(
            f'Sampling rate range: {self.min_sample_rate:.2f} ~ {self.max_sample_rate} Hz')

    def show_daq_chassis_device_name(self) -> None:
        if PRINT_FUNC_NAME_FLAG:
            print(
                f'run function - {get_func_name(self.show_daq_chassis_device_name)}')

        print(f'DAQ chassis name: {self.device.compact_daq_chassis_device}')


class NI9234(NIDAQ):

    channel_num_list: tuple = (0, 1, 2, 3, '0', '1', '2', '3')

    def __init__(self, device_name) -> None:
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.__init__)}')

        super(NI9234, self).__init__()

        self.device_name = device_name
        self.device = nidaqmx.system.device.Device(device_name)
        self.device.reset_device()
        self.system = nidaqmx.system.System.local()
        self.sample_rate = 12800
        self.record_duration = 5.0
        self.frame_duration = 1000  # millisecond
        self.min_sample_rate = self.device.ai_min_rate
        self.max_sample_rate = self.device.ai_max_single_chan_rate
        self.frame_size = int(self.sample_rate * self.frame_duration * 0.001)
        self.buffer_size = self.frame_size * 10
        self.every_n_samples_event_type = EveryNSamplesEventType.ACQUIRED_INTO_BUFFER
        self.writer_switch_flag = False
        self.write_file_dir = '.'
        self.stream_writer = CSVStreamWriter(directory=self.write_file_dir)
        self.segment_writer = NPYWriter(directory=self.write_file_dir)
        self.stream_switch_flag = False

    def create_task(self, task_name: str) -> None:
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.create_task)}')

        if self.task == None:
            self.task = nidaqmx.task.Task(new_task_name=task_name)
        else:
            self.close_task()
            self.task = nidaqmx.task.Task(new_task_name=task_name)

    def clear_task(self) -> None:
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.clear_task)}')

        if self.task != None:
            self.task.close()

    def channel_check(self, physical_channel):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.channel_check)}')

        if physical_channel not in self.channel_num_list:
            raise BaseException(
                f'Illegal channel number. Legal channel : {self.channel_num_list}')
        if self.task.number_of_channels > 4:
            raise BaseException('All channels have added to task.')

    def add_accel_channel(
            self,
            physical_channel: Union[int, str],
            name_to_assign_to_channel,
            terminal_config,
            min_val,
            max_val,
            units,
            sensitivity,
            sensitivity_units,
            current_excit_source,
            current_excit_val,
            custom_scale_name) -> None:
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.add_accel_channel)}')

        self.channel_check(physical_channel)

        if terminal_config == 'default':
            terminal_config = TerminalConfiguration.DEFAULT
        if sensitivity_units == 'millivolts_per_g':
            sensitivity_units = AccelSensitivityUnits.MILLIVOLTS_PER_G
        if units == 'g':
            units = AccelUnits.G
        if current_excit_source == 'internal':
            current_excit_source = ExcitationSource.INTERNAL

        self.task.ai_channels.add_ai_accel_chan(
            physical_channel=f'{self.device_name}/ai{physical_channel}',
            name_to_assign_to_channel=f'{self.device_name}-ch{physical_channel}-{name_to_assign_to_channel}',
            terminal_config=terminal_config,
            min_val=min_val,
            max_val=max_val,
            units=units,
            sensitivity=sensitivity,
            sensitivity_units=sensitivity_units,
            current_excit_source=current_excit_source,
            current_excit_val=current_excit_val,
            custom_scale_name=custom_scale_name)

    def add_microphone_channel(
            self,
            physical_channel: Union[int, str],
            name_to_assign_to_channel,
            terminal_config,
            units,
            mic_sensitivity,
            current_excit_source,
            current_excit_val,
            custom_scale_name) -> None:
        if PRINT_FUNC_NAME_FLAG:
            print(
                f'run function - {get_func_name(self.add_microphone_channel)}')

        self.channel_check(physical_channel)

        if terminal_config == 'default':
            terminal_config = TerminalConfiguration.DEFAULT
        if units == 'Pa':
            units = SoundPressureUnits.PA
        if current_excit_source == 'internal':
            current_excit_source = ExcitationSource.INTERNAL

        self.task.ai_channels.add_ai_microphone_chan(
            physical_channel=f'{self.device_name}/ai{physical_channel}',
            name_to_assign_to_channel=f'{self.device_name}-ch{physical_channel}-{name_to_assign_to_channel}',
            terminal_config=terminal_config,
            units=units,
            mic_sensitivity=mic_sensitivity,
            current_excit_source=current_excit_source,
            current_excit_val=current_excit_val,
            custom_scale_name=custom_scale_name)

    def set_sample_rate(self, sample_rate: float) -> None:
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.set_sample_rate)}')

        self.sample_rate = sample_rate
        self.task.timing.cfg_samp_clk_timing(
            rate=self.sample_rate, sample_mode=AcquisitionType.CONTINUOUS)
        self.set_buffer_size()

    def set_frame_duration(self, frame_duration: int) -> None:
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.set_frame_duration)}')

        self.frame_duration = frame_duration
        self.set_buffer_size()

    def set_buffer_size(self) -> None:
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.set_buffer_size)}')

        self.frame_size = int(self.sample_rate * self.frame_duration * 0.001)
        self.buffer_size = self.frame_size * 10
        self.task.in_stream.input_buf_size = self.buffer_size

    def set_writer_type(self, writer_type) -> None:
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.set_writer_type)}')

        print(f'set writer type: {writer_type}')
        self.writer_type = writer_type
        if writer_type == 'stream':
            self.writer = self.stream_writer
        if writer_type == 'segment':
            self.writer = self.segment_writer

    def set_writer_enable(self) -> None:
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.set_writer_enable)}')

        self.writer_switch_flag = True

    def set_writer_disable(self) -> None:
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.set_writer_disable)}')

        self.writer_switch_flag = False

    def ready_read(self, callback_method) -> None:
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.ready_read)}')

        self.task.register_every_n_samples_acquired_into_buffer_event(
            sample_interval=self.frame_size,
            callback_method=callback_method)

        self.chunk = np.zeros((self.task.number_of_channels, self.frame_size))
        self.stream_reader = NiStreamReaders.AnalogMultiChannelReader(
            self.task.in_stream)

    def start_task(self) -> None:
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.start_task)}')

        self.task.start()

    def start_streaming_period_time(self, time: Union[float, int]) -> None:
        '''
        time: second
        '''
        if PRINT_FUNC_NAME_FLAG:
            print(
                f'run function - {get_func_name(self.start_streaming_period_time)}')

        number_of_samples = int(time * self.sample_rate)
        return self.task.in_stream.read(number_of_samples_per_channel=number_of_samples)

    async def async_start_task(self) -> None:
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.async_start_task)}')

        self.task.start()

    def stop_task(self) -> None:
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.stop_task)}')

        self.task.stop()
        print('Task is stopped!!')

    def close_task(self) -> None:
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.close_task)}')

        self.set_writer_disable()
        self.task.close()
        print('Task is done!!')

    def show_control_manual(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.show_control_manual)}')

        print('Press "s" to start, "q" to quit.')
        print('While recording, press "p" to stop streaming, "q" to quit program.')

    async def key_switch_event(self) -> None:
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.key_switch_event)}')

        while True:

            await asyncio.sleep(0.1)
            if keyboard.is_pressed('s') and not self.stream_switch_flag:
                self.set_writer_enable()
                self.start_task()
                print('start streaming')
            elif keyboard.is_pressed('p'):
                self.set_writer_disable()
                print('stop streamming')
            elif keyboard.is_pressed('q'):
                self.set_writer_disable()
                self.close_task()
                print('close task')
                break

    @staticmethod
    def callback_method(task_handle, every_n_samples_event_type,
                        num_of_samples, callback_data: NIDAQ):
        daq = callback_data
        daq.stream_reader.read_many_sample(daq.chunk)

        if daq.writer_switch_flag:
            daq.writer.write(chunk=daq.chunk, transpose=True)

        current_time = datetime.now().isoformat(timespec='milliseconds')
        print(
            f'run callback - Now time: {current_time} / Recording..., buffer size: {num_of_samples}')

        return 0


if __name__ == '__main__':
    nidaq = NI9234(device_name='NI_9234')
    nidaq.create_task(task_name='myTask')
    nidaq.add_accel_channel(0)
    nidaq.add_microphone_channel(1)
    nidaq.set_sample_rate(12800)
    nidaq.set_frame_duration(100)

    nidaq.ready_read(
        callback_method=lambda task_handle, every_n_samples_event_type,
        number_of_samples, callback_data: nidaq.callback_method(
            nidaq.task._handle, nidaq.every_n_samples_event_type, nidaq.frame_size, callback_data=nidaq))
    nidaq.show_control_manual()

    tasks = [nidaq.key_switch_event()]
    asyncio.run(asyncio.wait(tasks))

    print('Process done!')
