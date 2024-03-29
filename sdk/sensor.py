from typing import Optional, Union
import json

from sdk.utils import get_func_name
from debug_flags import PRINT_FUNC_NAME_FLAG


class AccelerometerChannelSettings:

    def __init__(self, sensor_cfg_path, physical_channel) -> None:
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.__init__)}')

        self.sensor_cfg_file = open(sensor_cfg_path)
        self.sensor_cfg = json.load(self.sensor_cfg_file)
        self.physical_channel = physical_channel
        self.name_to_assign_to_channel = self.sensor_cfg['name_to_assign_to_channel']
        self.terminal_config = self.sensor_cfg['terminal_config']
        self.min_val = self.sensor_cfg['min_val']
        self.max_val = self.sensor_cfg['max_val']
        self.units = self.sensor_cfg['units']
        self.sensitivity = self.sensor_cfg['sensitivity']
        self.sensitivity_units = self.sensor_cfg['sensitivity_units']
        self.current_excit_source = self.sensor_cfg['current_excit_source']
        self.current_excit_val = self.sensor_cfg['current_excit_val']
        self.custom_scale_name = self.sensor_cfg['custom_scale_name']
        self.sensor_type = self.sensor_cfg['sensor_type']
        
        self.sensor_cfg_file.close()

    def paramters_checker(self):
        # TODO: 根據Sensor種類、使用的API來限制設定檔內容
        pass


class MicrophoneChannelSettings:

    def __init__(self, sensor_cfg_path, physical_channel) -> None:
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.__init__)}')

        self.sensor_cfg_file = open(sensor_cfg_path)
        self.sensor_cfg = json.load(self.sensor_cfg_file)
        self.physical_channel = physical_channel
        self.name_to_assign_to_channel = self.sensor_cfg['name_to_assign_to_channel']
        self.terminal_config = self.sensor_cfg['terminal_config']
        self.units = self.sensor_cfg['units']
        self.mic_sensitivity = self.sensor_cfg['mic_sensitivity']
        self.max_snd_press_level = self.sensor_cfg['max_snd_press_level']
        self.current_excit_source = self.sensor_cfg['current_excit_source']
        self.current_excit_val = self.sensor_cfg['current_excit_val']
        self.custom_scale_name = self.sensor_cfg['custom_scale_name']
        self.sensor_type = self.sensor_cfg['sensor_type']

        self.sensor_cfg_file.close()

    def paramters_checker(self):
        # TODO: 根據Sensor種類、使用的API來限制設定檔內容
        pass

if __name__ == '__main__':
    sensor_cfg_file = './352C33.json'
    accel_setting = AccelerometerChannelSettings(sensor_cfg_file)
    print(accel_setting.current_excit_source)
    sensor_cfg_file = './130F20.json'
    mic_setting = MicrophoneChannelSettings(sensor_cfg_file)
    print(mic_setting.current_excit_source)

