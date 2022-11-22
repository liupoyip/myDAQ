import os
import json

from .ui_ni9234 import Ui_NI9234
from PySide6.QtWidgets import QWidget, QTableWidget, QMessageBox
from PySide6.QtCore import Slot, QTimer
from PySide6 import QtUiTools

#cfg_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cfg_ni9234.json')
#cfg_file = open(cfg_path)
#default_settings = json.load(cfg_file)


class NI9234Form(QWidget):
    def __init__(self, model=None, controller=None):
        super().__init__()
        self.model = model
        self.controller = controller
        self.ui = Ui_NI9234()
        self.ui.setupUi(self)
        self.set_default_values()

    def set_default_values(self):
        self.ui.TaskName_LineEdit.setText(self.model.default_settings['default_task_name'])

        self.ui.SampleRate_SpinBox.setValue(self.model.default_settings['default_sample_rate'])
        self.ui.SampleRate_SpinBox.setMinimum(self.model.default_settings['min_sample_rate'])
        self.ui.SampleRate_SpinBox.setMaximum(self.model.default_settings['max_sample_rate'])
        self.ui.SampleRate_HorizontalSlider.setValue(
            self.model.default_settings['default_sample_rate'])
        self.ui.SampleRate_HorizontalSlider.setMinimum(
            self.model.default_settings['min_sample_rate'])
        self.ui.SampleRate_HorizontalSlider.setMaximum(
            self.model.default_settings['max_sample_rate'])

        self.ui.FrameDuration_SpinBox.setValue(
            self.model.default_settings['default_frame_duration'])
        self.ui.FrameDuration_SpinBox.setMinimum(self.model.default_settings['min_frame_duration'])
        self.ui.FrameDuration_SpinBox.setMaximum(self.model.default_settings['max_frame_duration'])
        self.ui.FrameDuration_HorizontalSlider.setValue(
            self.model.default_settings['default_frame_duration'])
        self.ui.FrameDuration_HorizontalSlider.setMinimum(
            self.model.default_settings['min_frame_duration'])
        self.ui.FrameDuration_HorizontalSlider.setMaximum(
            self.model.default_settings['max_frame_duration'])

        self.ui.BufferDuration_SpinBox.setValue(self.ui.FrameDuration_SpinBox.value())
        self.ui.BufferDuration_SpinBox.setMinimum(self.ui.FrameDuration_SpinBox.value())
        self.ui.BufferDuration_SpinBox.setMaximum(
            self.model.default_settings['max_buffer_duration'])
        self.ui.BufferDuration_HorizontalSlider.setValue(self.ui.FrameDuration_SpinBox.value())
        self.ui.BufferDuration_HorizontalSlider.setMinimum(self.ui.FrameDuration_SpinBox.value())
        self.ui.BufferDuration_HorizontalSlider.setMaximum(
            self.model.default_settings['max_buffer_duration'])

        self.ui.UpdateInterval_SpinBox.setValue(self.ui.FrameDuration_SpinBox.value())
        self.ui.UpdateInterval_SpinBox.setMinimum(self.ui.FrameDuration_SpinBox.value())
        self.ui.UpdateInterval_SpinBox.setMaximum(
            self.model.default_settings['max_update_interval'])
        self.ui.UpdateInterval_HorizontalSlider.setValue(self.ui.FrameDuration_SpinBox.value())
        self.ui.UpdateInterval_HorizontalSlider.setMinimum(self.ui.FrameDuration_SpinBox.value())
        self.ui.UpdateInterval_HorizontalSlider.setMaximum(
            self.model.default_settings['max_update_interval'])

        self.ui.DownSample_SpinBox.setValue(self.model.default_settings['default_graph_downsample'])
        self.ui.DownSample_SpinBox.setMinimum(self.model.default_settings['min_graph_downsample'])
        self.ui.DownSample_SpinBox.setMaximum(self.model.default_settings['max_graph_downsample'])
        self.ui.DownSample_HorizontalSlider.setValue(
            self.model.default_settings['default_graph_downsample'])
        self.ui.DownSample_HorizontalSlider.setMinimum(
            self.model.default_settings['min_graph_downsample'])
        self.ui.DownSample_HorizontalSlider.setMaximum(
            self.model.default_settings['max_graph_downsample'])

        self.ui.WriteFileType_ComboBox.addItems(self.model.default_settings['write_file_type'])
        self.ui.WriteFile_LineEdit.setText(self.model.default_settings['default_write_file_path'])

        # set initial disable component
        self.ui.Stop_PushButton.setDisabled(True)
        self.ui.Start_PushButton.setDisabled(True)
        self.ui.ClearTask_PushButton.setDisabled(True)

        # connet slot
        self.ui.FrameDuration_SpinBox.valueChanged.connect(self.on_frame_duration_changed)
        self.ui.Start_PushButton.clicked.connect(self.on_start_button_clicked)
        self.ui.Stop_PushButton.clicked.connect(self.on_stop_button_clicked)
        self.ui.CreateTask_PushButton.clicked.connect(self.on_create_task_button_clicked)
        self.ui.ClearTask_PushButton.clicked.connect(self.on_clear_task_button_clicked)

        self.channel_checkbox_list = [
            self.ui.Channel0_CheckBox,
            self.ui.Channel1_CheckBox,
            self.ui.Channel2_CheckBox,
            self.ui.Channel3_CheckBox]
        self.channel_combobox_list = [
            self.ui.Channel0_ComboBox,
            self.ui.Channel1_ComboBox,
            self.ui.Channel2_ComboBox,
            self.ui.Channel3_ComboBox]
        for combox in self.channel_combobox_list:
            combox.addItems(self.model.default_settings["sensor_type"])
            combox.setDisabled(True)
        for checkbox, combox in zip(self.channel_checkbox_list, self.channel_combobox_list):
            checkbox.toggled.connect(combox.setEnabled)

    @Slot(int)
    def on_frame_duration_changed(self, value):
        self.ui.BufferDuration_SpinBox.setMinimum(value)
        self.ui.UpdateInterval_SpinBox.setMinimum(value)

    @Slot()
    def on_create_task_button_clicked(self):
        if self.check_channel_options():
            self.ui.Start_PushButton.setEnabled(True)
            self.ui.ClearTask_PushButton.setEnabled(True)
            self.ui.CreateTask_PushButton.setDisabled(True)
            self.ui.PreparationSetting_Frame.setDisabled(True)
            self.model.sample_rate = self.ui.SampleRate_SpinBox.value()
            self.model.frame_duration = self.ui.FrameDuration_SpinBox.value()
            self.model.buffer_duration = self.ui.BufferDuration_SpinBox.value()
            self.model.update_interval = self.ui.UpdateInterval_SpinBox.value()
            self.model.downsample = self.ui.DownSample_SpinBox.value()
            channels, sensor_types = self.add_channels()
            self.model.channels = channels
            self.model.sensor_types = sensor_types

    @Slot()
    def on_clear_task_button_clicked(self):
        self.ui.PreparationSetting_Frame.setEnabled(True)
        self.ui.CreateTask_PushButton.setEnabled(True)
        self.ui.Start_PushButton.setDisabled(True)
        self.ui.ClearTask_PushButton.setDisabled(True)

    @Slot()
    def on_start_button_clicked(self):
        self.ui.Stop_PushButton.setEnabled(True)
        self.ui.Start_PushButton.setDisabled(True)
        self.ui.Reset_PushButton.setDisabled(True)
        self.ui.ClearTask_PushButton.setDisabled(True)

    @Slot()
    def on_stop_button_clicked(self):
        self.ui.Start_PushButton.setEnabled(True)
        self.ui.ClearTask_PushButton.setEnabled(True)
        self.ui.Reset_PushButton.setEnabled(True)
        self.ui.Stop_PushButton.setDisabled(True)

    def check_channel_options(self):
        error_channels = list()

        if set([checkbox.isChecked() for checkbox in self.channel_checkbox_list]) == {False}:
            QMessageBox.critical(None, "Channel error", "Please select channels!!")
            return False

        for i, (checkbox, combox) in enumerate(zip(self.channel_checkbox_list, self.channel_combobox_list)):
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
        for i, (checkbox, combox) in enumerate(zip(self.channel_checkbox_list, self.channel_combobox_list)):
            if checkbox.isChecked():
                channels.append(i)
                sensor_types.append(combox.currentText)
        return channels, sensor_types
