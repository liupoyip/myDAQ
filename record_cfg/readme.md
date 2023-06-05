## Properties Format:
sensormodel
sensor_series_number

```
{
    'machine_ID'            :   'machine_01',
    'sensor_model'          :   [sensor_model_0, sensor_model_1]
    'sensor_series_number'  :   [series_num_0, series_num_1]
    'sensor_setting'        :   [sensor_model_0.json, sensor_model_1.json]
    'data_name'             :   [data_name_0, data_name_1],
    'physical_unit'         :   [physical_unit_0, physical_unit_1]
    'DAQ_model',            :   
    'start_time',           :   
    'sampling_rate',        :   
    'end_time',             :   
    'chunk_length',         :   
    'chunk_count',          :   
}
```

## 支援Sensor種類
- accelerometer
  - library URL : https://nidaqmx-python.readthedocs.io/en/latest/ai_channel_collection.html?highlight=add_ai_mic#nidaqmx._task_modules.ai_channel_collection.AIChannelCollection.add_ai_accel_chan
  - function default paramters

        add_ai_accel_chan(
            physical_channel,
            name_to_assign_to_channel='',
            terminal_config=TerminalConfiguration.DEFAULT,
            min_val=-5.0,
            max_val=5.0,
            units=AccelUnits.G,
            sensitivity=100.0,
            sensitivity_units=AccelSensitivityUnits.MILLIVOLTS_PER_G,
            current_excit_source=ExcitationSource.INTERNAL,
            current_excit_val=0.004,
            custom_scale_name='')

- microphone
  - library URL : https://nidaqmx-python.readthedocs.io/en/latest/ai_channel_collection.html?highlight=add_ai_microphone#nidaqmx._task_modules.ai_channel_collection.AIChannelCollection.add_ai_microphone_chan
  - function default parameters

        add_ai_microphone_chan(
            physical_channel,                               # 硬體channel名稱
            name_to_assign_to_channel='',                   # 
            terminal_config=TerminalConfiguration.DEFAULT,
            units=SoundPressureUnits.PA,
            mic_sensitivity=45.0,
            max_snd_press_level=100.0,
            current_excit_source=ExcitationSource.INTERNAL,
            current_excit_val=0.004,
            custom_scale_name='')