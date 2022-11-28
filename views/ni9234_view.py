import numpy as np
from .ui_ni9234 import Ui_NI9234
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCharts import QChartView
from PySide6.QtCore import Slot, QTimer
from .wave_chart import WaveChart
#from ..model.ModelNIDAQ import NIDAQModel
#from ..controllers.ni9234_crtl import NI9234Controller


class NI9234View(QWidget, Ui_NI9234):
    # def __init__(self, model: NIDAQModel, controller: NI9234Controller):

    def __init__(self, model, controller):
        super().__init__()
        self._model = model
        self._controller = controller

        # setup view
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

        self._channel_checkbox_list = [
            self._ui.Channel0_CheckBox,
            self._ui.Channel1_CheckBox,
            self._ui.Channel2_CheckBox,
            self._ui.Channel3_CheckBox]
        self._channel_combox_list = [
            self._ui.Channel0_ComboBox,
            self._ui.Channel1_ComboBox,
            self._ui.Channel2_ComboBox,
            self._ui.Channel3_ComboBox]

        for checkbox, combox in zip(self._channel_checkbox_list, self._channel_combox_list):
            checkbox.toggled.connect(combox.setEnabled)

        self._ui.WriteFile_CheckBox.toggled.connect(self.on_write_file_checkbox_toggled)

        # self._model.task_name_changed.connect(self.on_task_name_changed)
        # self._model.sample_rate_changed.connect(self.on_sample_rate_changed)
        # self._model.frame_duration_changed.connect
        # self._model.buffer_rate_changed.connect
        # self._model.update_interval_changed.connect
        # self._model.downsample_changed.connect
        # self._model.channels_changed.connect
        # self._model.write_file_flag_changed.connect

        self.set_default_values()

    def set_default_values(self):
        # self._controller.change_task_name(
        #     self._model._default_settings['default_task_name'])
        # self._controller.change_sample_rate(
        #    self._model._default_settings['default_sample_rate'])

        self._ui.TaskName_LineEdit.setText(
            self._model._default_settings['default_task_name'])
        self._ui.SampleRate_SpinBox.setValue(
            self._model._default_settings['default_sample_rate'])
        self._ui.SampleRate_SpinBox.setMinimum(
            self._model._default_settings['min_sample_rate'])
        self._ui.SampleRate_SpinBox.setMaximum(
            self._model._default_settings['max_sample_rate'])
        self._ui.SampleRate_HorizontalSlider.setValue(
            self._model._default_settings['default_sample_rate'])
        self._ui.SampleRate_HorizontalSlider.setMinimum(
            self._model._default_settings['min_sample_rate'])
        self._ui.SampleRate_HorizontalSlider.setMaximum(
            self._model._default_settings['max_sample_rate'])

        self._ui.FrameDuration_SpinBox.setValue(
            self._model._default_settings['default_frame_duration'])
        self._ui.FrameDuration_SpinBox.setMinimum(
            self._model._default_settings['min_frame_duration'])
        self._ui.FrameDuration_SpinBox.setMaximum(
            self._model._default_settings['max_frame_duration'])
        self._ui.FrameDuration_HorizontalSlider.setValue(
            self._model._default_settings['default_frame_duration'])
        self._ui.FrameDuration_HorizontalSlider.setMinimum(
            self._model._default_settings['min_frame_duration'])
        self._ui.FrameDuration_HorizontalSlider.setMaximum(
            self._model._default_settings['max_frame_duration'])

        self._ui.BufferRate_SpinBox.setValue(
            self._model._default_settings['min_buffer_rate'])
        self._ui.BufferRate_SpinBox.setMinimum(
            self._model._default_settings['min_buffer_rate'])
        self._ui.BufferRate_SpinBox.setMaximum(
            self._model._default_settings['max_buffer_rate'])
        self._ui.BufferRate_HorizontalSlider.setValue(
            self._model._default_settings['min_buffer_rate'])
        self._ui.BufferRate_HorizontalSlider.setMinimum(
            self._model._default_settings['min_buffer_rate'])
        self._ui.BufferRate_HorizontalSlider.setMaximum(
            self._model._default_settings['max_buffer_rate'])

        self._ui.UpdateInterval_SpinBox.setValue(
            self._ui.FrameDuration_SpinBox.value())
        self._ui.UpdateInterval_SpinBox.setMinimum(
            self._ui.FrameDuration_SpinBox.value())
        self._ui.UpdateInterval_SpinBox.setMaximum(
            self._model._default_settings['max_update_interval'])
        self._ui.UpdateInterval_HorizontalSlider.setValue(
            self._ui.FrameDuration_SpinBox.value())
        self._ui.UpdateInterval_HorizontalSlider.setMinimum(
            self._ui.FrameDuration_SpinBox.value())
        self._ui.UpdateInterval_HorizontalSlider.setMaximum(
            self._model._default_settings['max_update_interval'])

        self._ui.DownSample_SpinBox.setValue(
            self._model._default_settings['default_graph_downsample'])
        self._ui.DownSample_SpinBox.setMinimum(
            self._model._default_settings['min_graph_downsample'])
        self._ui.DownSample_SpinBox.setMaximum(
            self._model._default_settings['max_graph_downsample'])
        self._ui.DownSample_HorizontalSlider.setValue(
            self._model._default_settings['default_graph_downsample'])
        self._ui.DownSample_HorizontalSlider.setMinimum(
            self._model._default_settings['min_graph_downsample'])
        self._ui.DownSample_HorizontalSlider.setMaximum(
            self._model._default_settings['max_graph_downsample'])

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

        for checkbox, combox in zip(self._channel_checkbox_list, self._channel_combox_list):
            checkbox.setChecked(False)
            combox.clear()
            combox.addItems(self._model._default_settings["sensor_type"])
            combox.setDisabled(True)

    @Slot(str)
    def on_task_name_changed(self, value):
        self._ui.TaskName_LineEdit.setText(value)

    # @Slot(int)
    # def on_sample_rate_changed(self, value):
    #     self._ui.SampleRate_SpinBox.setValue(value)

    @Slot(int)
    def on_frame_duration_changed(self, value):
        # self._ui.BufferRate_SpinBox.setMinimum(value)
        self._ui.UpdateInterval_SpinBox.setMinimum(value)

    @Slot()
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
            self.graph_update_timer.setInterval(self._ui.UpdateInterval_SpinBox.value())

            self._controller.change_task_name(self._ui.TaskName_LineEdit.text())
            self._controller.change_sample_rate(self._ui.SampleRate_SpinBox.value())
            self._controller.change_frame_duration(self._ui.FrameDuration_SpinBox.value())
            self._controller.change_buffer_rate(self._ui.BufferRate_SpinBox.value())
            self._controller.change_update_interval(self._ui.UpdateInterval_SpinBox.value())
            self._controller.change_downsample(self._ui.DownSample_SpinBox.value())
            channels, sensor_types = self.add_channels()
            self._controller.change_channels(channels)
            self._controller.change_sensor_types(sensor_types)
            self._model.create()
            self.reset_wave_chart_axis()

    @Slot()
    def on_clear_task_button_clicked(self):
        self._ui.PreparationSetting_Frame.setEnabled(True)
        self._ui.CreateTask_PushButton.setEnabled(True)
        self._ui.Start_PushButton.setDisabled(True)
        self._ui.ClearTask_PushButton.setDisabled(True)
        self._ui.WriteFile_GroupBox.setDisabled(True)
        self._ui.WriteFile_CheckBox.setChecked(False)
        self._model.clear()

    @Slot()
    def on_start_button_clicked(self):
        self._ui.Stop_PushButton.setEnabled(True)
        self._ui.Start_PushButton.setDisabled(True)
        self._ui.Reset_PushButton.setDisabled(True)
        self._ui.ClearTask_PushButton.setDisabled(True)
        self.graph_update_timer.start()
        self._model.start()

    @Slot()
    def on_stop_button_clicked(self):
        self._ui.Start_PushButton.setEnabled(True)
        self._ui.ClearTask_PushButton.setEnabled(True)
        self._ui.Reset_PushButton.setEnabled(True)
        self._ui.Stop_PushButton.setDisabled(True)
        self.graph_update_timer.stop()
        self._model.stop()

    @Slot()
    def on_write_file_checkbox_toggled(self):
        self._controller.change_write_file_flag(self._ui.WriteFile_CheckBox.isChecked())
        self._model.ready_write_file()

    @Slot()
    def on_reset_button_clicked(self):
        self.set_default_values()

    @Slot()
    def on_graph_update_timer_timeout(self):
        self.wave_data_buffer = self._controller.read_wave_data_buffer()
        self.update_wave_chart()
        # print('veiw', self.wave_data_buffer[:, 0:2])

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
        if set([checkbox.isChecked() for checkbox in self._channel_checkbox_list]) == {False}:
            QMessageBox.critical(None, "Channel error", "Please select channels!!")
            return False

        for i, (checkbox, combox) in enumerate(zip(self._channel_checkbox_list, self._channel_combox_list)):
            if checkbox.isChecked() and combox.currentText() == '':
                error_channels.append(i)

        if len(error_channels) == 0:
            return True
        else:
            QMessageBox.critical(None, "Channel error",
                                 f"Incorrect sensor type!!\n Channel: {error_channels}")
            return False

    def add_channels(self):
        channels = list()
        sensor_types = list()
        for i, (checkbox, combox) in enumerate(zip(self._channel_checkbox_list, self._channel_combox_list)):
            if checkbox.isChecked():
                channels.append(i)
                sensor_types.append(combox.currentText())
        return channels, sensor_types

    def reset_wave_chart_axis(self):
        self.Channel0_WaveChart.reset_axis(
            self._model.buffer_duration, buffer_len=self._model.buffer_len)

    def update_wave_chart(self):
        self.Channel0_WaveChart.set_y(self.wave_data_buffer[0])
