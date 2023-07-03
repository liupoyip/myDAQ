from typing import Optional
from datetime import datetime
import os
import json

import numpy as np
import numpy.typing as npt
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import QTimer, Qt,  QRectF
from PySide6.QtGui import QFocusEvent, QWindow, QPainter, QPen, QColor

from .ni9234_ui import Ui_NI9234
from .chart import WaveChart, SpectrumChart
from models.NIDAQModel import NIDAQModel
from debug_flags import PRINT_FUNC_NAME_FLAG
from sdk.utils import get_func_name


class NI9234ViewModel(QWidget):

    wave_downsample_rate: Optional[int] = None
    spectrum_downsample_rate: Optional[int] = None
    abnormal_flags: npt.NDArray = np.array([False, False, False, False])
    vertical_line_painter = QPainter()
    vertical_line_rectf = QRectF()
    vertical_line_pen = QPen(QColor('red'))
    vertical_line_pen.setWidth(2)
    vertical_line_painter.setPen(vertical_line_pen)
    record_cfg_path = f'.{os.sep}models{os.sep}record_cfg.json'
    record_cfg = None
    sensor_cfg_dir = f'.{os.sep}models{os.sep}sensors'
    sensor_cfg_list: list[str] = list()
    sensor_cfg_names: list[str] = list()
    
    active_channel_num_list: list = list()
    active_sensor_model_list: list = list()
    active_sensor_cfg_list: list = list()


    def __init__(self, model):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.__init__)}')

        super().__init__()
        self.model: NIDAQModel = model
        # set focus status
        # self.focusInEvent(self.setMouseTracking(True))
        # self.focusOutEvent(self.setMouseTracking(False))
        # self.setFocusPolicy(Qt.StrongFocus)

        # setup view
        self.setFixedWidth(1600)
        self.setFixedHeight(900)
        self.ui: Optional[Ui_NI9234] = Ui_NI9234()
        self.ui.setupUi(self)
        self.Channel0_WaveChart: Optional[WaveChart] = WaveChart()
        self.Channel1_WaveChart: Optional[WaveChart] = WaveChart()
        self.Channel2_WaveChart: Optional[WaveChart] = WaveChart()
        self.Channel3_WaveChart: Optional[WaveChart] = WaveChart()
        self.channel_wave_charts: Optional[list[WaveChart, WaveChart, WaveChart, WaveChart]] = [
            self.Channel0_WaveChart,
            self.Channel1_WaveChart,
            self.Channel2_WaveChart,
            self.Channel3_WaveChart]

        self.Channel0_SpectrumChart = SpectrumChart()
        self.Channel1_SpectrumChart = SpectrumChart()
        self.Channel2_SpectrumChart = SpectrumChart()
        self.Channel3_SpectrumChart = SpectrumChart()
        self.channel_spectrum_charts = [
            self.Channel0_SpectrumChart,
            self.Channel1_SpectrumChart,
            self.Channel2_SpectrumChart,
            self.Channel3_SpectrumChart]

        for i, (wave_chart, spectrum_chart) in enumerate(zip(self.channel_wave_charts, self.channel_spectrum_charts)):
            self.ui.Charts_GridLayout.addWidget(wave_chart.chart_view, i, 1)
            self.ui.Charts_GridLayout.addWidget(spectrum_chart.chart_view, i, 2)

        # Timers
        self.graph_update_timer = QTimer()
        self.graph_update_timer.setInterval(100)
        self.now_time_timer = QTimer()
        self.now_time_timer.setInterval(1000)

        # listen for model event
        self.ui.FrameDuration_SpinBox.valueChanged.connect(self.on_frame_duration_changed)
        self.ui.Reset_PushButton.clicked.connect(self.on_reset_button_clicked)
        self.ui.Start_PushButton.clicked.connect(self.on_start_button_clicked)
        self.ui.Stop_PushButton.clicked.connect(self.on_stop_button_clicked)
        self.ui.CreateTask_PushButton.clicked.connect(self.on_create_task_button_clicked)
        self.ui.ClearTask_PushButton.clicked.connect(self.on_clear_task_button_clicked)
        self.channel_checkboxes = [
            self.ui.Channel0_CheckBox,
            self.ui.Channel1_CheckBox,
            self.ui.Channel2_CheckBox,
            self.ui.Channel3_CheckBox]
        self.channel_comboxes = [
            self.ui.Channel0_ComboBox,
            self.ui.Channel1_ComboBox,
            self.ui.Channel2_ComboBox,
            self.ui.Channel3_ComboBox]
        for checkbox, combox in zip(self.channel_checkboxes, self.channel_comboxes):
            checkbox.toggled.connect(combox.setEnabled)
        self.ui.WriteFile_CheckBox.toggled.connect(self.on_write_file_checkbox_toggled)
        self.ui.VisualizeSwitch_Checkbox.toggled.connect(self.on_visualize_switch_checkbox_toggled)
        self.graph_update_timer.timeout.connect(self.on_graph_update_timer_timeout)
        self.now_time_timer.timeout.connect(self.on_now_time_timer_timeout)
        self.ui.WriteFileType_ComboBox.currentTextChanged.connect(
            self.on_write_file_type_combox_current_text_changed)

        self.wave_data_buffer: Optional[npt.NDArray] = None
        self.spectrum_data_buffer: Optional[npt.NDArray] = None

        # set default params
        self.set_default_values()
        self.ui.WriteFileStatus_Label.setText('Status: Off')
        self.now_time_timer.start()
        self.writer_type = self.ui.WriteFileType_ComboBox.currentIndex()

        # import config
        self.ui.ImportConfig_Pushbutton.clicked.connect(self.on_import_config_button_clicked)

        # func test button
        self.ui.FunctionTest_Pushbutton.clicked.connect(self.on_function_test_pushbutton_clicked)


    def on_function_test_pushbutton_clicked(self):
        '''
        This function is for testing while function built or function modified
        Don't let this function online
        '''
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.on_function_test_pushbutton_clicked)}')


    def set_default_values(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.set_default_values)}')

        self.ui.ImportConfigPath_LineEdit.setText(self.record_cfg_path)
        self.ui.MachineID_LineEdit.setText('dummy_machine')
        
        self.ui.TaskName_LineEdit.setText(
            self.model.default_settings['default_task_name'])
        self.ui.SampleRate_SpinBox.setMinimum(
            self.model.default_settings['min_sample_rate'])
        self.ui.SampleRate_SpinBox.setMaximum(
            self.model.default_settings['max_sample_rate'])
        self.ui.SampleRate_SpinBox.setValue(
            self.model.default_settings['default_sample_rate'])
        self.ui.SampleRate_HorizontalSlider.setMinimum(
            self.model.default_settings['min_sample_rate'])
        self.ui.SampleRate_HorizontalSlider.setMaximum(
            self.model.default_settings['max_sample_rate'])
        self.ui.SampleRate_HorizontalSlider.setValue(
            self.model.default_settings['default_sample_rate'])

        self.ui.FrameDuration_SpinBox.setMinimum(
            self.model.default_settings['min_frame_duration'])
        self.ui.FrameDuration_SpinBox.setMaximum(
            self.model.default_settings['max_frame_duration'])
        self.ui.FrameDuration_SpinBox.setValue(
            self.model.default_settings['default_frame_duration'])
        self.ui.FrameDuration_HorizontalSlider.setMinimum(
            self.model.default_settings['min_frame_duration'])
        self.ui.FrameDuration_HorizontalSlider.setMaximum(
            self.model.default_settings['max_frame_duration'])
        self.ui.FrameDuration_HorizontalSlider.setValue(
            self.model.default_settings['default_frame_duration'])

        self.ui.BufferRate_SpinBox.setMinimum(
            self.model.default_settings['min_buffer_rate'])
        self.ui.BufferRate_SpinBox.setMaximum(
            self.model.default_settings['max_buffer_rate'])
        self.ui.BufferRate_SpinBox.setValue(
            self.model.default_settings['default_buffer_rate'])
        self.ui.BufferRate_HorizontalSlider.setMinimum(
            self.model.default_settings['min_buffer_rate'])
        self.ui.BufferRate_HorizontalSlider.setMaximum(
            self.model.default_settings['max_buffer_rate'])
        self.ui.BufferRate_HorizontalSlider.setValue(
            self.model.default_settings['default_buffer_rate'])

        self.ui.ChartUpdateInterval_SpinBox.setMinimum(
            self.ui.FrameDuration_SpinBox.value())
        self.ui.ChartUpdateInterval_SpinBox.setMaximum(
            self.model.default_settings['max_update_interval'])
        self.ui.ChartUpdateInterval_SpinBox.setValue(
            self.ui.FrameDuration_SpinBox.value())
        self.ui.ChartUpdateInterval_HorizontalSlider.setMinimum(
            self.ui.FrameDuration_SpinBox.value())
        self.ui.ChartUpdateInterval_HorizontalSlider.setMaximum(
            self.model.default_settings['max_update_interval'])
        self.ui.ChartUpdateInterval_HorizontalSlider.setValue(
            self.ui.FrameDuration_SpinBox.value())

        self.ui.WaveDownSample_SpinBox.setMinimum(
            self.model.default_settings['min_wave_downsample'])
        self.ui.WaveDownSample_SpinBox.setMaximum(
            self.model.default_settings['max_wave_downsample'])
        self.ui.WaveDownSample_SpinBox.setValue(
            self.model.default_settings['default_wave_downsample'])
        self.ui.WaveDownSample_HorizontalSlider.setMinimum(
            self.model.default_settings['min_wave_downsample'])
        self.ui.WaveDownSample_HorizontalSlider.setMaximum(
            self.model.default_settings['max_wave_downsample'])
        self.ui.WaveDownSample_HorizontalSlider.setValue(
            self.model.default_settings['default_wave_downsample'])

        self.ui.SpectrumDownSample_SpinBox.setMinimum(
            self.model.default_settings['min_spectrum_downsample'])
        self.ui.SpectrumDownSample_SpinBox.setMaximum(
            self.model.default_settings['max_spectrum_downsample'])
        self.ui.SpectrumDownSample_SpinBox.setValue(
            self.model.default_settings['default_spectrum_downsample'])
        self.ui.SpectrumDownSample_HorizontalSlider.setMinimum(
            self.model.default_settings['min_spectrum_downsample'])
        self.ui.SpectrumDownSample_HorizontalSlider.setMaximum(
            self.model.default_settings['max_spectrum_downsample'])
        self.ui.SpectrumDownSample_HorizontalSlider.setValue(
            self.model.default_settings['default_spectrum_downsample'])

        self.ui.WriteFileType_ComboBox.addItems(
            self.model.default_settings['write_file_type'])
        self.ui.WriteFile_LineEdit.setText(
            self.model.default_settings['default_write_file_dir'])

        # set component initial enable
        self.ui.CreateTask_PushButton.setEnabled(True)
        self.ui.PreparationSetting_Frame.setEnabled(True)
        self.ui.Visualize_Groupbox.setEnabled(True)

        # set component initial disable
        self.ui.Stop_PushButton.setDisabled(True)
        self.ui.Start_PushButton.setDisabled(True)
        self.ui.ClearTask_PushButton.setDisabled(True)
        self.ui.WriteFile_GroupBox.setDisabled(True)
        self.ui.ChannelOption_GroupBox.setEnabled(True)

        # initail sensor config
        self.sensor_cfg_list.clear()
        self.sensor_cfg_names.clear()
        self.get_sensor_cfgs()
        for checkbox, combox in zip(self.channel_checkboxes, self.channel_comboxes):
            checkbox.setChecked(False)
            checkbox.setEnabled(True)
            combox.clear()
            combox.addItem('Sensor config')
            combox.addItems(self.sensor_cfg_names)
            combox.setEnabled(True)
        self.ui.VisualizeSwitch_Checkbox.setChecked(False)


    def on_import_config_button_clicked(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.on_import_config_button_clicked)}')

        record_cfg_file = open(self.record_cfg_path)
        self.record_cfg = json.load(record_cfg_file)
        record_cfg_file.close()
        self.ui.MachineID_LineEdit.setText(self.record_cfg['machine_ID'])
        self.ui.TaskName_LineEdit.setText(self.record_cfg['task_name'])
        self.ui.SampleRate_HorizontalSlider.setValue(self.record_cfg['sample_rate'])
        self.ui.FrameDuration_HorizontalSlider.setValue(self.record_cfg['frame_duration'])
        self.ui.DAQParameters_GroupBox.setDisabled(True)
        self.set_sensor_cfg_with_record_cfg()
        

    def get_sensor_cfgs(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.get_sensor_cfgs)}')

        for cfg in os.listdir(self.sensor_cfg_dir):
            cfg_name, ext = os.path.splitext(cfg)
            if ext == '.json':
                self.sensor_cfg_list.append(os.path.join(self.sensor_cfg_dir, cfg))
        for cfg in self.sensor_cfg_list:
            cfg_name, _ = os.path.splitext(os.path.basename(cfg))
            self.sensor_cfg_names.append(cfg_name)
        print(f'sensor config detected: {self.sensor_cfg_list}')


    def set_sensor_cfg_with_record_cfg(self):
        '''
        For ImportConfig_Pushbutton
        '''
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.set_sensor_cfg_with_record_cfg)}')

        for checkbox, combox in zip(self.channel_checkboxes, self.channel_comboxes):
            checkbox.setChecked(False)
            checkbox.setDisabled(True)
            combox.setDisabled(True)

        for channel, cfg_path in zip(self.record_cfg['channels'], self.record_cfg['sensor_cfg']):
            cfg_file_name, _ = os.path.splitext(os.path.basename(cfg_path))
            print(f'cfg_path: {cfg_path}, target chan: {channel}, cfg_file_name:{cfg_file_name}')
            self.channel_comboxes[channel].setCurrentText(cfg_file_name)
            self.channel_checkboxes[channel].setChecked(True)
            self.channel_comboxes[channel].setDisabled(True)


    def on_focus_changed(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.on_focus_changed)}')

        if self.isActiveWindow():
            self.setMouseTracking(True)
            #print('focus in!!')
        else:
            self.setMouseTracking(False)
            #print('focus out!!')


    def on_frame_duration_changed(self, value):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.on_frame_duration_changed)}')

        self.ui.ChartUpdateInterval_SpinBox.setMinimum(value)
        self.ui.ChartUpdateInterval_SpinBox.setSingleStep(value)
        self.ui.ChartUpdateInterval_HorizontalSlider.setSingleStep(value)
        self.ui.ChartUpdateInterval_HorizontalSlider.setPageStep(value)


    def on_create_task_button_clicked(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.on_create_task_button_clicked)}')

        # 這個 function 耦合程度和 NIDAQModel.py 程度極高，改動時要謹慎

        if self.channel_is_seleted():
            self.ui.Start_PushButton.setEnabled(True)
            self.ui.ClearTask_PushButton.setEnabled(True)
            self.ui.CreateTask_PushButton.setDisabled(True)
            self.ui.PreparationSetting_Frame.setDisabled(True)
            self.graph_update_timer.setInterval(self.ui.ChartUpdateInterval_SpinBox.value())
            self.wave_downsample_rate = self.ui.WaveDownSample_SpinBox.value()
            self.spectrum_downsample_rate = self.ui.SpectrumDownSample_SpinBox.value()

            # setting task for nidaq model
            # TODO : get parameters from this block for output data
            # ------block start------
            self.add_channels()
            self.model.machine_name = self.ui.MachineID_LineEdit.text()
            self.model.task_name = self.ui.TaskName_LineEdit.text()
            self.model.export_cfg_file_name = self.record_cfg['export_cfg_file_name']
            self.model.sample_rate = self.ui.SampleRate_SpinBox.value()
            self.model.frame_duration = self.ui.FrameDuration_SpinBox.value()
            self.model.buffer_rate = self.ui.BufferRate_SpinBox.value()
            self.model.update_interval = self.ui.ChartUpdateInterval_SpinBox.value()
            self.model.channels = self.active_channel_num_list
            self.model.active_sensor_model_list = self.active_sensor_model_list
            self.model.active_sensor_cfg_list = self.active_sensor_cfg_list
            self.model.create()
            # ------block end------

            self.reset_wave_chart()
            self.reset_spectrum_chart()
            for num, channel_setting in zip(self.active_channel_num_list, self.model.all_channel_settings):
                if channel_setting.sensor_type == 'accelerometer':
                    self.channel_wave_charts[num].set_y_range(-0.5, 0.5)
                    self.channel_wave_charts[num].set_y_label('value (g)')
                    self.channel_spectrum_charts[num].set_x_range(0, 6000)
                elif channel_setting.sensor_type == 'microphone':
                    self.channel_wave_charts[num].set_y_range(-1, 1)
                    self.channel_wave_charts[num].set_y_label('value (Pa)')
                    self.channel_spectrum_charts[num].set_x_range(0, 6000)


    def on_clear_task_button_clicked(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.on_clear_task_button_clicked)}')

        self.ui.PreparationSetting_Frame.setEnabled(True)
        self.ui.CreateTask_PushButton.setEnabled(True)
        self.ui.Start_PushButton.setDisabled(True)
        self.ui.ClearTask_PushButton.setDisabled(True)
        self.ui.WriteFile_GroupBox.setDisabled(True)
        self.ui.WriteFile_CheckBox.setChecked(False)
        self.ui.Visualize_Groupbox.setDisabled(True)
        self.ui.VisualizeSwitch_Checkbox.setChecked(False)
        self.model.clear()
        self.reset_wave_chart()
        self.reset_spectrum_chart()


    def on_start_button_clicked(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.on_start_button_clicked)}')

        self.ui.Stop_PushButton.setEnabled(True)
        self.ui.Start_PushButton.setDisabled(True)
        self.ui.Reset_PushButton.setDisabled(True)
        self.ui.ClearTask_PushButton.setDisabled(True)
        self.ui.WriteFile_GroupBox.setEnabled(True)
        self.ui.ChartParameters_GroupBox.setDisabled(True)
        self.model.start()


    def on_stop_button_clicked(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.on_stop_button_clicked)}')

        self.ui.Start_PushButton.setEnabled(True)
        self.ui.ClearTask_PushButton.setEnabled(True)
        self.ui.Reset_PushButton.setEnabled(True)
        self.ui.Stop_PushButton.setDisabled(True)
        self.ui.WriteFile_CheckBox.setChecked(False)
        self.ui.WriteFile_GroupBox.setDisabled(True)
        # self.ui.VisualizeSwitch_Checkbox.setChecked(False)
        self.ui.ChartParameters_GroupBox.setEnabled(True)
        self.model.stop()


    def on_write_file_type_combox_current_text_changed(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.on_write_file_type_combox_current_text_changed)}')

        self.writer_type = self.ui.WriteFileType_ComboBox.currentText()
        if self.ui.WriteFileType_ComboBox.currentIndex() == 0:
            self.ui.WriteFile_CheckBox.setChecked(False)
            self.ui.WriteFile_CheckBox.setDisabled(True)
        else:
            self.ui.WriteFile_CheckBox.setEnabled(True)


    def on_write_file_checkbox_toggled(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.on_write_file_checkbox_toggled)}')

        print(f'write file checkbox toggled : {self.ui.WriteFile_CheckBox.isChecked()}')
        self.model.writer_switch_flag = self.ui.WriteFile_CheckBox.isChecked()
        if self.ui.WriteFile_CheckBox.isChecked():
            self.model.start_write_file(mode=self.writer_type)
            self.ui.WriteFileStatus_Label.setText('Status: On')
            self.ui.WriteFileType_ComboBox.setDisabled(True)
        if not self.ui.WriteFile_CheckBox.isChecked():
            self.model.stop_write_file()
            self.ui.WriteFileStatus_Label.setText('Status: Off')
            self.ui.WriteFileType_ComboBox.setEnabled(True)


    def on_visualize_switch_checkbox_toggled(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.on_visualize_switch_checkbox_toggled)}')

        if self.ui.VisualizeSwitch_Checkbox.isChecked():
            print('Signal Visualized enable')
            self.graph_update_timer.start()
        if not self.ui.VisualizeSwitch_Checkbox.isChecked():
            print('Signal Visualized disable')
            self.graph_update_timer.stop()


    def on_reset_button_clicked(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.on_reset_button_clicked)}')

        self.set_default_values()


    def on_graph_update_timer_timeout(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.on_graph_update_timer_timeout)}')

        self.wave_data_buffer = self.model.get_wave_data_buffer()
        self.spectrum_data_buffer = self.model.get_spectrum_data_buffer()
        self.wave_data_buffer_mean = np.mean(self.wave_data_buffer)
        self.update_wave_chart()
        self.update_spectrum_chart()


    def on_now_time_timer_timeout(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.on_now_time_timer_timeout)}')

        self.ui.NowTime_Label.setText(datetime.now().isoformat(sep=' ', timespec='seconds'))


    def channel_is_seleted(self):
        '''
        Depend on Channel_Checkbox and SensorType_Combox

        If no channel been selected
            return `False`

        If any channels be selected but channel type is not selected
            return `False`

        If channels and sensor types be selected
            return `True`
        '''
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.channel_is_seleted)}')

        error_channels = list()
        if set([checkbox.isChecked() for checkbox in self.channel_checkboxes]) == {False}:
            QMessageBox.critical(None, "Channel error", "Please select channels!!")
            return False

        for i, (checkbox, combox) in enumerate(zip(self.channel_checkboxes, self.channel_comboxes)):
            if checkbox.isChecked() and combox.currentIndex() == 0:
                error_channels.append(i)

        if len(error_channels) == 0:
            return True
        else:
            QMessageBox.critical(None, "Channel error",
                                 f"Incorrect sensor type!!\n Channel: {error_channels}")
            return False


    def add_channels(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.add_channels)}')

        self.active_channel_num_list.clear()
        self.active_sensor_model_list.clear()
        for channel_num, (checkbox, combox) in enumerate(zip(self.channel_checkboxes, self.channel_comboxes)):
            if checkbox.isChecked():
                self.active_channel_num_list.append(channel_num)
                sensor_cfg_path = os.path.join(self.sensor_cfg_dir, f'{combox.currentText()}.json')
                cfg_file = open(sensor_cfg_path)
                sensor_cfg = json.load(cfg_file)
                cfg_file.close()
                self.active_sensor_model_list.append(sensor_cfg['sensor_model'])
                self.active_sensor_cfg_list.append(sensor_cfg_path)
        print(f'active sensor models: {self.active_sensor_model_list}')


    def reset_wave_chart(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.reset_wave_chart)}')

        time_limit = self.model.buffer_duration
        wave_len = self.model.get_wave_buffer_len()
        wave_tail = wave_len % self.wave_downsample_rate
        if wave_tail == 0:
            wave_len = wave_len // self.wave_downsample_rate
        else:
            wave_len = wave_len // self.wave_downsample_rate + 1

        for num in self.active_channel_num_list:
            wave_chart: WaveChart = self.channel_wave_charts[num]
            wave_chart.reset_axis(time_limit, wave_len)


    def reset_spectrum_chart(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.reset_spectrum_chart)}')
            
        freqs = self.model.get_spectrum_freqs()
        spectrum_len = len(freqs)
        freqs_tail = spectrum_len % self.spectrum_downsample_rate
        if freqs_tail == 0:
            spectrum_len = spectrum_len // self.spectrum_downsample_rate
        else:
            spectrum_len = spectrum_len // self.spectrum_downsample_rate + 1
        freqs_tail += 1
        self.freq_limit = freqs[-freqs_tail]

        for num in self.active_channel_num_list:
            spectrum_chart: SpectrumChart = self.channel_spectrum_charts[num]
            spectrum_chart.reset_axis(self.freq_limit, spectrum_len)


    def update_wave_chart(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.update_wave_chart)}')

        for i, num in enumerate(self.active_channel_num_list):
            wave_chart: WaveChart = self.channel_wave_charts[num]
            wave_data_downsample = self.wave_data_buffer[i, ::self.wave_downsample_rate]
            wave_chart.set_y(wave_data_downsample)


    def update_spectrum_chart(self):
        if PRINT_FUNC_NAME_FLAG:
            print(f'run function - {get_func_name(self.update_spectrum_chart)}')
            
        for i, num in enumerate(self.active_channel_num_list):
            abnormal_flag = self.model.get_abnormal_flag()
            spectrum_chart: SpectrumChart = self.channel_spectrum_charts[num]
            mean_spectrum = np.mean(self.spectrum_data_buffer[i], axis=0)
            # mean_spectrum = mean_spectrum / np.max(mean_spectrum) # normalize 0~1
            spectrum_data_downsample = mean_spectrum[::self.spectrum_downsample_rate]
            # normalize 0~1
            spectrum_data_downsample = spectrum_data_downsample / np.max(spectrum_data_downsample)
            spectrum_chart.set_y(spectrum_data_downsample)

            if abnormal_flag:
                max_power_idx = np.where(mean_spectrum == np.max(mean_spectrum))[0][0]
                spectrum_chart.chart_view.vertical_line_x = self.model.get_spectrum_freqs()[
                    max_power_idx]
                spectrum_chart.chart_view.drawForeground(
                    self.vertical_line_painter, self.vertical_line_rectf)

            if not abnormal_flag:
                spectrum_chart.chart_view.vertical_line_x = None
                spectrum_chart.chart_view.drawForeground(
                    self.vertical_line_painter, self.vertical_line_rectf)