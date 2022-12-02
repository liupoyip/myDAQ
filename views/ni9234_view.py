from typing import Optional
import numpy as np
from .ui_ni9234 import Ui_NI9234
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Slot, QTimer
from .chart import WaveChart, SpectrumChart
#from ..model.ModelNIDAQ import NIDAQModel
#from ..controllers.ni9234_crtl import NI9234Controller


class NI9234View(QWidget, Ui_NI9234):
    # def __init__(self, model: NIDAQModel, controller: NI9234Controller):
    _wave_downsample_rate: Optional[int] = None
    _spectrum_downsample_rate: Optional[int] = None

    # def __init__(self, model, controller):

    def __init__(self, model):
        super().__init__()
        self._model = model
        #self._controller = controller

        # setup view
        self.setFixedWidth(1600)
        self.setFixedHeight(900)
        self._ui = Ui_NI9234()
        self._ui.setupUi(self)
        self.Channel0_WaveChart = WaveChart()
        self.Channel1_WaveChart = WaveChart()
        self.Channel2_WaveChart = WaveChart()
        self.Channel3_WaveChart = WaveChart()
        self.channel_wave_charts = [
            self.Channel0_WaveChart,
            self.Channel1_WaveChart,
            self.Channel2_WaveChart,
            self.Channel3_WaveChart]
        for wave_chart in self.channel_wave_charts:
            self._ui.WaveCharts_VBoxLayout.addWidget(wave_chart.chart_view)

        self.Channel0_SpectrumChart = SpectrumChart()
        self.Channel1_SpectrumChart = SpectrumChart()
        self.Channel2_SpectrumChart = SpectrumChart()
        self.Channel3_SpectrumChart = SpectrumChart()
        self.channel_spectrum_charts = [
            self.Channel0_SpectrumChart,
            self.Channel1_SpectrumChart,
            self.Channel2_SpectrumChart,
            self.Channel3_SpectrumChart]
        for spectrum_chart in self.channel_spectrum_charts:
            self._ui.SpectrumCharts_VBoxLayout.addWidget(spectrum_chart.chart_view)

        # graph update timer
        self.graph_update_timer = QTimer()
        self.graph_update_timer.setInterval(100)

        # listen for model event signals
        self._ui.TaskName_LineEdit.textChanged.connect(self.on_task_name_changed)
        self._ui.FrameDuration_SpinBox.valueChanged.connect(self.on_frame_duration_changed)
        self._ui.Reset_PushButton.clicked.connect(self.on_reset_button_clicked)
        self._ui.Start_PushButton.clicked.connect(self.on_start_button_clicked)
        self._ui.Stop_PushButton.clicked.connect(self.on_stop_button_clicked)
        self._ui.CreateTask_PushButton.clicked.connect(self.on_create_task_button_clicked)
        self._ui.ClearTask_PushButton.clicked.connect(self.on_clear_task_button_clicked)
        self.graph_update_timer.timeout.connect(self.on_graph_update_timer_timeout)
        self.wave_data_buffer = None

        self._channel_checkboxes = [
            self._ui.Channel0_CheckBox,
            self._ui.Channel1_CheckBox,
            self._ui.Channel2_CheckBox,
            self._ui.Channel3_CheckBox]
        self._channel_comboxes = [
            self._ui.Channel0_ComboBox,
            self._ui.Channel1_ComboBox,
            self._ui.Channel2_ComboBox,
            self._ui.Channel3_ComboBox]

        for checkbox, combox in zip(self._channel_checkboxes, self._channel_comboxes):
            checkbox.toggled.connect(combox.setEnabled)

        self._ui.WriteFile_CheckBox.toggled.connect(self.on_write_file_checkbox_toggled)

        self.set_default_values()

    def set_default_values(self):

        self._ui.TaskName_LineEdit.setText(
            self._model._default_settings['default_task_name'])

        self._ui.SampleRate_SpinBox.setMinimum(
            self._model._default_settings['min_sample_rate'])
        self._ui.SampleRate_SpinBox.setMaximum(
            self._model._default_settings['max_sample_rate'])
        self._ui.SampleRate_SpinBox.setValue(
            self._model._default_settings['default_sample_rate'])
        self._ui.SampleRate_HorizontalSlider.setMinimum(
            self._model._default_settings['min_sample_rate'])
        self._ui.SampleRate_HorizontalSlider.setMaximum(
            self._model._default_settings['max_sample_rate'])
        self._ui.SampleRate_HorizontalSlider.setValue(
            self._model._default_settings['default_sample_rate'])

        self._ui.FrameDuration_SpinBox.setMinimum(
            self._model._default_settings['min_frame_duration'])
        self._ui.FrameDuration_SpinBox.setMaximum(
            self._model._default_settings['max_frame_duration'])
        self._ui.FrameDuration_SpinBox.setValue(
            self._model._default_settings['default_frame_duration'])
        self._ui.FrameDuration_HorizontalSlider.setMinimum(
            self._model._default_settings['min_frame_duration'])
        self._ui.FrameDuration_HorizontalSlider.setMaximum(
            self._model._default_settings['max_frame_duration'])
        self._ui.FrameDuration_HorizontalSlider.setValue(
            self._model._default_settings['default_frame_duration'])

        self._ui.BufferRate_SpinBox.setMinimum(
            self._model._default_settings['min_buffer_rate'])
        self._ui.BufferRate_SpinBox.setMaximum(
            self._model._default_settings['max_buffer_rate'])
        self._ui.BufferRate_SpinBox.setValue(
            self._model._default_settings['default_buffer_rate'])
        self._ui.BufferRate_HorizontalSlider.setMinimum(
            self._model._default_settings['min_buffer_rate'])
        self._ui.BufferRate_HorizontalSlider.setMaximum(
            self._model._default_settings['max_buffer_rate'])
        self._ui.BufferRate_HorizontalSlider.setValue(
            self._model._default_settings['default_buffer_rate'])

        self._ui.ChartUpdateInterval_SpinBox.setMinimum(
            self._ui.FrameDuration_SpinBox.value())
        self._ui.ChartUpdateInterval_SpinBox.setMaximum(
            self._model._default_settings['max_update_interval'])
        self._ui.ChartUpdateInterval_SpinBox.setValue(
            self._ui.FrameDuration_SpinBox.value())
        self._ui.ChartUpdateInterval_HorizontalSlider.setMinimum(
            self._ui.FrameDuration_SpinBox.value())
        self._ui.ChartUpdateInterval_HorizontalSlider.setMaximum(
            self._model._default_settings['max_update_interval'])
        self._ui.ChartUpdateInterval_HorizontalSlider.setValue(
            self._ui.FrameDuration_SpinBox.value())

        self._ui.WaveDownSample_SpinBox.setMinimum(
            self._model._default_settings['min_wave_downsample'])
        self._ui.WaveDownSample_SpinBox.setMaximum(
            self._model._default_settings['max_wave_downsample'])
        self._ui.WaveDownSample_SpinBox.setValue(
            self._model._default_settings['default_wave_downsample'])
        self._ui.WaveDownSample_HorizontalSlider.setMinimum(
            self._model._default_settings['min_wave_downsample'])
        self._ui.WaveDownSample_HorizontalSlider.setMaximum(
            self._model._default_settings['max_wave_downsample'])
        self._ui.WaveDownSample_HorizontalSlider.setValue(
            self._model._default_settings['default_wave_downsample'])

        self._ui.SpectrumDownSample_SpinBox.setMinimum(
            self._model._default_settings['min_spectrum_downsample'])
        self._ui.SpectrumDownSample_SpinBox.setMaximum(
            self._model._default_settings['max_spectrum_downsample'])
        self._ui.SpectrumDownSample_SpinBox.setValue(
            self._model._default_settings['default_spectrum_downsample'])
        self._ui.SpectrumDownSample_HorizontalSlider.setMinimum(
            self._model._default_settings['min_spectrum_downsample'])
        self._ui.SpectrumDownSample_HorizontalSlider.setMaximum(
            self._model._default_settings['max_spectrum_downsample'])
        self._ui.SpectrumDownSample_HorizontalSlider.setValue(
            self._model._default_settings['default_spectrum_downsample'])

        self._ui.WriteFileType_ComboBox.addItems(
            self._model._default_settings['write_file_type'])
        self._ui.WriteFile_LineEdit.setText(
            self._model._default_settings['default_write_file_dir'])

        self._ui.Parameters_Label.setText(
            'Parameters will show in here \n'
            'after Task created!!')

        # set initial component enable
        self._ui.CreateTask_PushButton.setEnabled(True)
        self._ui.PreparationSetting_Frame.setEnabled(True)

        # set initial component disable
        self._ui.Stop_PushButton.setDisabled(True)
        self._ui.Start_PushButton.setDisabled(True)
        self._ui.ClearTask_PushButton.setDisabled(True)
        self._ui.WriteFile_GroupBox.setDisabled(True)

        for checkbox, combox in zip(self._channel_checkboxes, self._channel_comboxes):
            checkbox.setChecked(False)
            combox.clear()
            combox.addItems(self._model._default_settings["sensor_type"])
            combox.setDisabled(True)

    def on_task_name_changed(self, value):
        self._ui.TaskName_LineEdit.setText(value)

    def on_frame_duration_changed(self, value):
        self._ui.ChartUpdateInterval_SpinBox.setMinimum(value)
        self._ui.ChartUpdateInterval_SpinBox.setSingleStep(value)
        self._ui.ChartUpdateInterval_HorizontalSlider.setSingleStep(value)
        self._ui.ChartUpdateInterval_HorizontalSlider.setPageStep(value)

    def on_create_task_button_clicked(self):
        if self.check_channel_options():
            self._ui.Start_PushButton.setEnabled(True)
            self._ui.ClearTask_PushButton.setEnabled(True)
            self._ui.WriteFile_GroupBox.setEnabled(True)
            self._ui.CreateTask_PushButton.setDisabled(True)
            self._ui.PreparationSetting_Frame.setDisabled(True)
            self._ui.Parameters_Label.setText(
                f'Sample Rate: {self._ui.SampleRate_SpinBox.value()} Hz\n'
                f'Frame Duration: {self._ui.FrameDuration_SpinBox.value()} ms\n'
                f'Buffer Rate: {self._ui.BufferRate_SpinBox.value()}\n')
            self.graph_update_timer.setInterval(self._ui.ChartUpdateInterval_SpinBox.value())
            self._wave_downsample_rate = self._ui.WaveDownSample_SpinBox.value()
            self._spectrum_downsample_rate = self._ui.SpectrumDownSample_SpinBox.value()

            self.add_channels()
            self._model.task_name = self._ui.TaskName_LineEdit.text()
            self._model.sample_rate = self._ui.SampleRate_SpinBox.value()
            self._model.frame_duration = self._ui.FrameDuration_SpinBox.value()
            self._model.buffer_rate = self._ui.BufferRate_SpinBox.value()
            self._model.update_interval = self._ui.ChartUpdateInterval_SpinBox.value()
            self._model.channels = self.active_channel_num_list
            self._model.sensor_types = self.sensor_type_list

            # self._controller.change_task_name(self._ui.TaskName_LineEdit.text())
            # self._controller.change_sample_rate(self._ui.SampleRate_SpinBox.value())
            # self._controller.change_frame_duration(self._ui.FrameDuration_SpinBox.value())
            # self._controller.change_buffer_rate(self._ui.BufferRate_SpinBox.value())
            # self._controller.change_update_interval(self._ui.ChartUpdateInterval_SpinBox.value())
            # self._controller.change_channels(self.active_channel_num_list)
            # self._controller.change_sensor_types(self.sensor_type_list)

            self._model.create()
            self.reset_wave_chart()
            self.reset_spectrum_chart()

    def on_clear_task_button_clicked(self):
        self._ui.PreparationSetting_Frame.setEnabled(True)
        self._ui.CreateTask_PushButton.setEnabled(True)
        self._ui.Start_PushButton.setDisabled(True)
        self._ui.ClearTask_PushButton.setDisabled(True)
        self._ui.WriteFile_GroupBox.setDisabled(True)
        self._ui.WriteFile_CheckBox.setChecked(False)
        self._model.clear()
        self.reset_wave_chart()
        self.reset_spectrum_chart()

    def on_start_button_clicked(self):
        self._ui.Stop_PushButton.setEnabled(True)
        self._ui.Start_PushButton.setDisabled(True)
        self._ui.Reset_PushButton.setDisabled(True)
        self._ui.ClearTask_PushButton.setDisabled(True)
        self.graph_update_timer.start()
        self._model.start()

    def on_stop_button_clicked(self):
        self._ui.Start_PushButton.setEnabled(True)
        self._ui.ClearTask_PushButton.setEnabled(True)
        self._ui.Reset_PushButton.setEnabled(True)
        self._ui.Stop_PushButton.setDisabled(True)
        self.graph_update_timer.stop()
        self._model.stop()

    def on_write_file_checkbox_toggled(self):
        self._model.write_file_flag = self._ui.WriteFile_CheckBox.isChecked()
        # self._controller.change_write_file_flag(self._ui.WriteFile_CheckBox.isChecked())
        self._model.ready_write_file()

    def on_reset_button_clicked(self):
        self.set_default_values()

    def on_graph_update_timer_timeout(self):
        # self.wave_data_buffer = self._controller.read_wave_data_buffer()
        self.wave_data_buffer = self._model.get_wave_data_buffer()
        # self.spectrum_data_buffer = self._controller.read_spectrum_data_buffer()
        self.spectrum_data_buffer = self._model.get_spectrum_data_buffer()
        self.update_wave_chart()
        self.update_spectrum_chart()

    def check_channel_options(self):
        """
        Depend on Channel_Checkbox and SensorType_Combox

        If no channel been selected
            return `False`

        If any channels be selected but channel type is not selected
            return `False`

        If channels and sensor types be selected
            return `True`
        """
        error_channels = list()
        if set([checkbox.isChecked() for checkbox in self._channel_checkboxes]) == {False}:
            QMessageBox.critical(None, "Channel error", "Please select channels!!")
            return False

        for i, (checkbox, combox) in enumerate(zip(self._channel_checkboxes, self._channel_comboxes)):
            if checkbox.isChecked() and combox.currentText() == '':
                error_channels.append(i)

        if len(error_channels) == 0:
            return True
        else:
            QMessageBox.critical(None, "Channel error",
                                 f"Incorrect sensor type!!\n Channel: {error_channels}")
            return False

    def add_channels(self):
        self.active_channel_num_list = list()
        self.sensor_type_list = list()

        for i, (checkbox, combox) in enumerate(zip(self._channel_checkboxes, self._channel_comboxes)):
            if checkbox.isChecked():
                self.active_channel_num_list.append(i)
                self.sensor_type_list.append(combox.currentText())

    def reset_wave_chart(self):
        time_limit = self._model.buffer_duration
        wave_len = self._model.get_wave_buffer_len()
        wave_tail = wave_len % self._wave_downsample_rate
        if wave_tail == 0:
            wave_len = wave_len // self._wave_downsample_rate
        else:
            wave_len = wave_len // self._wave_downsample_rate + 1

        for num in self.active_channel_num_list:
            self.channel_wave_charts[num].reset_axis(time_limit, wave_len)

    def reset_spectrum_chart(self):
        spectrum_len = len(self._model.get_spectrum_freqs())
        freqs_tail = spectrum_len % self._spectrum_downsample_rate
        if freqs_tail == 0:
            spectrum_len = spectrum_len // self._spectrum_downsample_rate
        else:
            spectrum_len = spectrum_len // self._spectrum_downsample_rate + 1
        freqs_tail += 1
        self.freq_limit = self._model.get_spectrum_freqs()[-freqs_tail]

        for num in self.active_channel_num_list:
            self.channel_spectrum_charts[num].reset_axis(self.freq_limit, spectrum_len)

    def update_wave_chart(self):
        for i, num in enumerate(self.active_channel_num_list):
            wave_data_downsample = self.wave_data_buffer[i, ::self._wave_downsample_rate]
            self.channel_wave_charts[num].set_y(wave_data_downsample)

    def update_spectrum_chart(self):
        for i, num in enumerate(self.active_channel_num_list):
            mean_spectrum = np.mean(self.spectrum_data_buffer[i], axis=0)
            # mean_spectrum = mean_spectrum / np.max(mean_spectrum) # normalize 0~1
            spectrum_data_downsample = mean_spectrum[::self._spectrum_downsample_rate]
            # normalize 0~1
            spectrum_data_downsample = spectrum_data_downsample / np.max(spectrum_data_downsample)
            self.channel_spectrum_charts[num].set_y(spectrum_data_downsample)

    def activate_wave_chart(self):
        ...

    def activate_spectrum_chart(self):
        ...
