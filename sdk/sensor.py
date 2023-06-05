# %%

from typing import Optional, Union
import json


class AiChannelBasicParameters:

    sensor_cfg_file: Optional[str] = 'dummy_model.json'
    physical_channel: Optional[str] = None  # format: {device_name}/{channel}, ex: dev0/ai0
    name_to_assign_to_channel: Optional[str] = None  # custom channel name
    min_val: Optional[float] = None
    max_val: Optional[float] = None
    physical_unit: Optional[str] = None
    sensitivity: Optional[float] = None
    sensitivity_units: Optional[str] = None
    current_excit_source: Optional[str] = None
    current_excit_val: Optional[float] = None
    custom_scale_name: Optional[str] = ''


class AccelerometerChannelSetting(AiChannelBasicParameters):

    def __init__(self, sensor_cfg_path) -> None:
        self.sensor_cfg_file = open(sensor_cfg_path)
        self.sensor_cfg = json.load(self.sensor_cfg_file)
        self.physical_channel = self.sensor_cfg['physical_channel']
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

    def paramters_checker(self):

        pass


class MicrophoneChannelSetting(AiChannelBasicParameters):

    def __init__(self, sensor_cfg_path) -> None:
        self.sensor_cfg_file = open(sensor_cfg_path)
        self.sensor_cfg = json.load(self.sensor_cfg_file)
        self.physical_channel = self.sensor_cfg['physical_channel']
        self.name_to_assign_to_channel = self.sensor_cfg['name_to_assign_to_channel']
        self.terminal_config = self.sensor_cfg['terminal_config']
        self.units = self.sensor_cfg['units']
        self.mic_sensitivity = self.sensor_cfg['mic_sensitivity']
        self.max_snd_press_level = self.sensor_cfg['max_snd_press_level']
        self.current_excit_source = self.sensor_cfg['current_excit_source']
        self.current_excit_val = self.sensor_cfg['current_excit_val']
        self.custom_scale_name = self.sensor_cfg['custom_scale_name']


if __name__ == '__main__':
    sensor_cfg_file = './sensor_cfg/352C33.json'
    accel_setting = AccelerometerChannelSetting(sensor_cfg_file)
    print(accel_setting.current_excit_source)
    sensor_cfg_file = './sensor_cfg/130F20.json'
    mic_setting = MicrophoneChannelSetting(sensor_cfg_file)
    print(mic_setting.current_excit_source)
