from typing import Optional
from datetime import datetime

import numpy as np
import numpy.typing as npt
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import QTimer, Qt,  QRectF
from PySide6.QtGui import QFocusEvent, QWindow, QPainter, QPen, QColor

from .ni9234_ui import Ui_NI9234
from .chart import WaveChart, SpectrumChart
from models.NIDAQModel import NIDAQModel


class NI9234ViewModel(QWidget):
    _wave_downsample_rate: Optional[int] = None
    _spectrum_downsample_rate: Optional[int] = None
    _abnormal_flags: npt.NDArray = np.array([False, False, False, False])
    _vertical_line_painter = QPainter()
    _vertical_line_rectf = QRectF()
    _vertical_line_pen = QPen(QColor('red'))
    _vertical_line_pen.setWidth(2)
    _vertical_line_painter.setPen(_vertical_line_pen)

    def __init__(self, model):
        super().__init__()
        self._model: NIDAQModel = model
        # set focus status
        # self.focusInEvent(self.setMouseTracking(True))
        # self.focusOutEvent(self.setMouseTracking(False))
        # self.setFocusPolicy(Qt.StrongFocus)

        # setup view
        self.setFixedWidth(1600)
        self.setFixedHeight(900)
        self._ui: Optional[Ui_NI9234] = Ui_NI9234()
        self._ui.setupUi(self)
        self.Channel0_WaveChart: Optional[WaveChart] = WaveChart()
        self.Channel1_WaveChart: Optional[WaveChart] = WaveChart()
        self.Channel2_WaveChart: Optional[WaveChart] = WaveChart()
        self.Channel3_WaveChart: Optional[WaveChart] = WaveChart()
        self.channel_wave_charts: Optional[list[WaveChart, WaveChart, WaveChart, WaveChart]] = [
            self.Channel0_WaveChart,
            self.Channel1_WaveChart,
            self.Channel2_WaveChart,
            self.Channel3_WaveChart]
        # for i, wave_chart in enumerate(self.channel_wave_charts):
        #     self._ui.WaveCharts_VBoxLayout.addWidget(wave_chart.chart_view)

        self.Channel0_SpectrumChart = SpectrumChart()
        self.Channel1_SpectrumChart = SpectrumChart()
        self.Channel2_SpectrumChart = SpectrumChart()
        self.Channel3_SpectrumChart = SpectrumChart()
        self.channel_spectrum_charts = [
            self.Channel0_SpectrumChart,
            self.Channel1_SpectrumChart,
            self.Channel2_SpectrumChart,
            self.Channel3_SpectrumChart]
        # for i, spectrum_chart in enumerate(self.channel_spectrum_charts):
        #     self._ui.SpectrumCharts_VBoxLayout.addWidget(spectrum_chart.chart_view)

        for i, (wave_chart, spectrum_chart) in enumerate(zip(self.channel_wave_charts, self.channel_spectrum_charts)):
            self._ui.Charts_GridLayout.addWidget(wave_chart.chart_view, i, 1)
            self._ui.Charts_GridLayout.addWidget(spectrum_chart.chart_view, i, 2)

        # Timers
        self.graph_update_timer = QTimer()
        self.graph_update_timer.setInterval(100)
        self.now_time_timer = QTimer()
        self.now_time_timer.setInterval(1000)

        # listen for model event

        # self._ui.TaskName_LineEdit.textChanged.connect(self.on_task_name_changed)
        self._ui.FrameDuration_SpinBox.valueChanged.connect(self.on_frame_duration_changed)
        self._ui.Reset_PushButton.clicked.connect(self.on_reset_button_clicked)
        self._ui.Start_PushButton.clicked.connect(self.on_start_button_clicked)
        self._ui.Stop_PushButton.clicked.connect(self.on_stop_button_clicked)
        self._ui.CreateTask_PushButton.clicked.connect(self.on_create_task_button_clicked)
        self._ui.ClearTask_PushButton.clicked.connect(self.on_clear_task_button_clicked)
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

        self.graph_update_timer.timeout.connect(self.on_graph_update_timer_timeout)
        self.now_time_timer.timeout.connect(self.on_now_time_timer_timeout)

        self.wave_data_buffer: Optional[npt.NDArray] = None
        self.spectrum_data_buffer: Optional[npt.NDArray] = None

        self.set_default_values()
        self._ui.WriteFileStatus_Label.setText('Status: Off')
        self.now_time_timer.start()
        self.writer_type = self._ui.WriteFileType_ComboBox.currentIndex()
        self._ui.WriteFileType_ComboBox.currentTextChanged.connect(
            self.on_write_file_type_combox_current_text_changed)

    def set_default_values(self):

        self._ui.TaskName_LineEdit.setText(
            self._model.default_settings['default_task_name'])

        self._ui.SampleRate_SpinBox.setMinimum(
            self._model.default_settings['min_sample_rate'])
        self._ui.SampleRate_SpinBox.setMaximum(
            self._model.default_settings['max_sample_rate'])
        self._ui.SampleRate_SpinBox.setValue(
            self._model.default_settings['default_sample_rate'])
        self._ui.SampleRate_HorizontalSlider.setMinimum(
            self._model.default_settings['min_sample_rate'])
        self._ui.SampleRate_HorizontalSlider.setMaximum(
            self._model.default_settings['max_sample_rate'])
        self._ui.SampleRate_HorizontalSlider.setValue(
            self._model.default_settings['default_sample_rate'])

        self._ui.FrameDuration_SpinBox.setMinimum(
            self._model.default_settings['min_frame_duration'])
        self._ui.FrameDuration_SpinBox.setMaximum(
            self._model.default_settings['max_frame_duration'])
        self._ui.FrameDuration_SpinBox.setValue(
            self._model.default_settings['default_frame_duration'])
        self._ui.FrameDuration_HorizontalSlider.setMinimum(
            self._model.default_settings['min_frame_duration'])
        self._ui.FrameDuration_HorizontalSlider.setMaximum(
            self._model.default_settings['max_frame_duration'])
        self._ui.FrameDuration_HorizontalSlider.setValue(
            self._model.default_settings['default_frame_duration'])

        self._ui.BufferRate_SpinBox.setMinimum(
            self._model.default_settings['min_buffer_rate'])
        self._ui.BufferRate_SpinBox.setMaximum(
            self._model.default_settings['max_buffer_rate'])
        self._ui.BufferRate_SpinBox.setValue(
            self._model.default_settings['default_buffer_rate'])
        self._ui.BufferRate_HorizontalSlider.setMinimum(
            self._model.default_settings['min_buffer_rate'])
        self._ui.BufferRate_HorizontalSlider.setMaximum(
            self._model.default_settings['max_buffer_rate'])
        self._ui.BufferRate_HorizontalSlider.setValue(
            self._model.default_settings['default_buffer_rate'])

        self._ui.ChartUpdateInterval_SpinBox.setMinimum(
            self._ui.FrameDuration_SpinBox.value())
        self._ui.ChartUpdateInterval_SpinBox.setMaximum(
            self._model.default_settings['max_update_interval'])
        self._ui.ChartUpdateInterval_SpinBox.setValue(
            self._ui.FrameDuration_SpinBox.value())
        self._ui.ChartUpdateInterval_HorizontalSlider.setMinimum(
            self._ui.FrameDuration_SpinBox.value())
        self._ui.ChartUpdateInterval_HorizontalSlider.setMaximum(
            self._model.default_settings['max_update_interval'])
        self._ui.ChartUpdateInterval_HorizontalSlider.setValue(
            self._ui.FrameDuration_SpinBox.value())

        self._ui.WaveDownSample_SpinBox.setMinimum(
            self._model.default_settings['min_wave_downsample'])
        self._ui.WaveDownSample_SpinBox.setMaximum(
            self._model.default_settings['max_wave_downsample'])
        self._ui.WaveDownSample_SpinBox.setValue(
            self._model.default_settings['default_wave_downsample'])
        self._ui.WaveDownSample_HorizontalSlider.setMinimum(
            self._model.default_settings['min_wave_downsample'])
        self._ui.WaveDownSample_HorizontalSlider.setMaximum(
            self._model.default_settings['max_wave_downsample'])
        self._ui.WaveDownSample_HorizontalSlider.setValue(
            self._model.default_settings['default_wave_downsample'])

        self._ui.SpectrumDownSample_SpinBox.setMinimum(
            self._model.default_settings['min_spectrum_downsample'])
        self._ui.SpectrumDownSample_SpinBox.setMaximum(
            self._model.default_settings['max_spectrum_downsample'])
        self._ui.SpectrumDownSample_SpinBox.setValue(
            self._model.default_settings['default_spectrum_downsample'])
        self._ui.SpectrumDownSample_HorizontalSlider.setMinimum(
            self._model.default_settings['min_spectrum_downsample'])
        self._ui.SpectrumDownSample_HorizontalSlider.setMaximum(
            self._model.default_settings['max_spectrum_downsample'])
        self._ui.SpectrumDownSample_HorizontalSlider.setValue(
            self._model.default_settings['default_spectrum_downsample'])

        self._ui.WriteFileType_ComboBox.addItems(
            self._model.default_settings['write_file_type'])
        self._ui.WriteFile_LineEdit.setText(
            self._model.default_settings['default_write_file_dir'])

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
            combox.addItems(self._model.default_settings["sensor_type"])
            combox.setDisabled(True)

    def on_focus_changed(self):
        if self.isActiveWindow():
            self.setMouseTracking(True)
            print('focus in!!')
        else:
            self.setMouseTracking(False)
            print('focus out!!')

    def on_frame_duration_changed(self, value):
        self._ui.ChartUpdateInterval_SpinBox.setMinimum(value)
        self._ui.ChartUpdateInterval_SpinBox.setSingleStep(value)
        self._ui.ChartUpdateInterval_HorizontalSlider.setSingleStep(value)
        self._ui.ChartUpdateInterval_HorizontalSlider.setPageStep(value)

    def on_create_task_button_clicked(self):
        if self.channel_is_seleted():
            self._ui.Start_PushButton.setEnabled(True)
            self._ui.ClearTask_PushButton.setEnabled(True)
            # self._ui.WriteFile_GroupBox.setEnabled(True)
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

            self._model.create()
            self.reset_wave_chart()
            self.reset_spectrum_chart()

            for num, sensor_type in zip(self.active_channel_num_list, self.sensor_type_list):
                if sensor_type == 'Accelerometer':
                    self.channel_wave_charts[num].set_y_range(-0.3, 0.3)
                    self.channel_wave_charts[num].set_y_label('value (g)')
                    self.channel_spectrum_charts[num].set_x_range(0, 6000)
                elif sensor_type == 'Microphone':
                    self.channel_wave_charts[num].set_y_range(-10, 10)
                    self.channel_wave_charts[num].set_y_label('value (pa)')
                    self.channel_spectrum_charts[num].set_x_range(0, 6000)

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
        self._ui.WriteFile_GroupBox.setEnabled(True)
        self.wave_data_buffer_count = 0
        self.graph_update_timer.start()
        self._model.start()

    def on_stop_button_clicked(self):
        self._ui.Start_PushButton.setEnabled(True)
        self._ui.ClearTask_PushButton.setEnabled(True)
        self._ui.Reset_PushButton.setEnabled(True)
        self._ui.Stop_PushButton.setDisabled(True)
        self._ui.WriteFile_CheckBox.setChecked(False)
        self._ui.WriteFile_GroupBox.setEnabled(False)
        self.graph_update_timer.stop()
        self._model.stop()

    def on_write_file_type_combox_current_text_changed(self):
        self.writer_type = self._ui.WriteFileType_ComboBox.currentText()

    def on_write_file_checkbox_toggled(self):
        print('write file checkbox toggled')
        self._model.writer_switch_flag = self._ui.WriteFile_CheckBox.isChecked()
        self._model.ready_write_file(mode=self.writer_type)
        if self._ui.WriteFile_CheckBox.isChecked():
            self._ui.WriteFileStatus_Label.setText('Status: On')
        if not self._ui.WriteFile_CheckBox.isChecked():
            self._ui.WriteFileStatus_Label.setText('Status: Off')

    def on_reset_button_clicked(self):
        self.set_default_values()

    def on_graph_update_timer_timeout(self):
        self.wave_data_buffer = self._model.get_wave_data_buffer()
        self.spectrum_data_buffer = self._model.get_spectrum_data_buffer()
        self.wave_data_buffer_mean = np.mean(self.wave_data_buffer)
        self.update_wave_chart()
        self.update_spectrum_chart()

    def on_now_time_timer_timeout(self):
        self._ui.NowTime_Label.setText(datetime.now().isoformat(sep=' ', timespec='seconds'))

    def channel_is_seleted(self):
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
            wave_chart: WaveChart = self.channel_wave_charts[num]
            wave_chart.reset_axis(time_limit, wave_len)

    def reset_spectrum_chart(self):
        freqs = self._model.get_spectrum_freqs()
        spectrum_len = len(freqs)
        freqs_tail = spectrum_len % self._spectrum_downsample_rate
        if freqs_tail == 0:
            spectrum_len = spectrum_len // self._spectrum_downsample_rate
        else:
            spectrum_len = spectrum_len // self._spectrum_downsample_rate + 1
        freqs_tail += 1
        self.freq_limit = freqs[-freqs_tail]

        for num in self.active_channel_num_list:
            spectrum_chart: SpectrumChart = self.channel_spectrum_charts[num]
            spectrum_chart.reset_axis(self.freq_limit, spectrum_len)

    def update_wave_chart(self):
        for i, num in enumerate(self.active_channel_num_list):
            wave_chart: WaveChart = self.channel_wave_charts[num]
            wave_data_downsample = self.wave_data_buffer[i, ::self._wave_downsample_rate]
            wave_chart.set_y(wave_data_downsample)

    def update_spectrum_chart(self):
        for i, num in enumerate(self.active_channel_num_list):
            abnormal_flag = self._model.get_abnormal_flag()
            spectrum_chart: SpectrumChart = self.channel_spectrum_charts[num]
            mean_spectrum = np.mean(self.spectrum_data_buffer[i], axis=0)
            # mean_spectrum = mean_spectrum / np.max(mean_spectrum) # normalize 0~1
            spectrum_data_downsample = mean_spectrum[::self._spectrum_downsample_rate]
            # normalize 0~1
            spectrum_data_downsample = spectrum_data_downsample / np.max(spectrum_data_downsample)
            spectrum_chart.set_y(spectrum_data_downsample)

            if abnormal_flag:
                max_power_idx = np.where(mean_spectrum == np.max(mean_spectrum))[0][0]
                spectrum_chart.chart_view.vertical_line_x = self._model.get_spectrum_freqs()[
                    max_power_idx]
                spectrum_chart.chart_view.drawForeground(
                    self._vertical_line_painter, self._vertical_line_rectf)
                # TODO: if abnormal_flag = True, get max(mean_spectrum) then mark
            if not abnormal_flag:
                spectrum_chart.chart_view.vertical_line_x = None
                spectrum_chart.chart_view.drawForeground(
                    self._vertical_line_painter, self._vertical_line_rectf)

    def activate_wave_chart(self):
        ...

    def activate_spectrum_chart(self):
        ...
