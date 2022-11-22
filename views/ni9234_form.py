import os
import json

from .ui_ni9234 import Ui_NI9234
from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Slot, QTimer
from PySide6 import QtUiTools

cfg_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cfg_ui_ni9234.json')
cfg_file = open(cfg_path)
setting_values = json.load(cfg_file)


class NI9234Form(QWidget):
    def __init__(self, model=None, controller=None):
        super().__init__()
        self.model = model
        # self._main_controller = main_controller
        self.ui = Ui_NI9234()
        self.ui.setupUi(self)
        self.set_default_values()

    def set_default_values(self):
        self.ui.TaskName_LineEdit.setText(setting_values['default_task_name'])

        self.ui.SampleRate_SpinBox.setValue(setting_values['default_sample_rate'])
        self.ui.SampleRate_SpinBox.setMinimum(setting_values['min_sample_rate'])
        self.ui.SampleRate_SpinBox.setMaximum(setting_values['max_sample_rate'])
        self.ui.SampleRate_HorizontalSlider.setValue(setting_values['default_sample_rate'])
        self.ui.SampleRate_HorizontalSlider.setMinimum(setting_values['min_sample_rate'])
        self.ui.SampleRate_HorizontalSlider.setMaximum(setting_values['max_sample_rate'])

        self.ui.FrameDuration_SpinBox.setValue(setting_values['default_frame_duration'])
        self.ui.FrameDuration_SpinBox.setMinimum(setting_values['min_frame_duration'])
        self.ui.FrameDuration_SpinBox.setMaximum(setting_values['max_frame_duration'])
        self.ui.FrameDuration_HorizontalSlider.setValue(setting_values['default_frame_duration'])
        self.ui.FrameDuration_HorizontalSlider.setMinimum(setting_values['min_frame_duration'])
        self.ui.FrameDuration_HorizontalSlider.setMaximum(setting_values['max_frame_duration'])

        self.ui.BufferDuration_SpinBox.setValue(self.ui.FrameDuration_SpinBox.value())
        self.ui.BufferDuration_SpinBox.setMinimum(self.ui.FrameDuration_SpinBox.value())
        self.ui.BufferDuration_SpinBox.setMaximum(setting_values['max_buffer_duration'])
        self.ui.BufferDuration_HorizontalSlider.setValue(self.ui.FrameDuration_SpinBox.value())
        self.ui.BufferDuration_HorizontalSlider.setMinimum(self.ui.FrameDuration_SpinBox.value())
        self.ui.BufferDuration_HorizontalSlider.setMaximum(setting_values['max_buffer_duration'])

        self.ui.UpdateInterval_SpinBox.setValue(self.ui.FrameDuration_SpinBox.value())
        self.ui.UpdateInterval_SpinBox.setMinimum(self.ui.FrameDuration_SpinBox.value())
        self.ui.UpdateInterval_SpinBox.setMaximum(setting_values['max_update_interval'])
        self.ui.UpdateInterval_HorizontalSlider.setValue(self.ui.FrameDuration_SpinBox.value())
        self.ui.UpdateInterval_HorizontalSlider.setMinimum(self.ui.FrameDuration_SpinBox.value())
        self.ui.UpdateInterval_HorizontalSlider.setMaximum(setting_values['max_update_interval'])

        self.ui.DownSample_SpinBox.setValue(setting_values['default_graph_downsample'])
        self.ui.DownSample_SpinBox.setMinimum(setting_values['min_graph_downsample'])
        self.ui.DownSample_SpinBox.setMaximum(setting_values['max_graph_downsample'])
        self.ui.DownSample_HorizontalSlider.setValue(setting_values['default_graph_downsample'])
        self.ui.DownSample_HorizontalSlider.setMinimum(setting_values['min_graph_downsample'])
        self.ui.DownSample_HorizontalSlider.setMaximum(setting_values['max_graph_downsample'])

        self.ui.Channel1_ComboBox.addItems(setting_values["sensor_type"])
        self.ui.Channel2_ComboBox.addItems(setting_values["sensor_type"])
        self.ui.Channel3_ComboBox.addItems(setting_values["sensor_type"])
        self.ui.Channel4_ComboBox.addItems(setting_values["sensor_type"])

        self.ui.WriteFileType_ComboBox.addItems(setting_values['write_file_type'])
        self.ui.WriteFile_LineEdit.setText(setting_values['default_write_file_path'])

        # set initial disable component
        self.ui.Stop_PushButton.setDisabled(True)
        self.ui.Start_PushButton.setDisabled(True)
        self.ui.ClearTask_PushButton.setDisabled(True)

        # connet slot
        self.ui.FrameDuration_SpinBox.valueChanged.connect(self.on_frame_duration_changed)
        self.ui.Start_PushButton.released.connect(self.on_start_button_release)
        self.ui.Stop_PushButton.released.connect(self.on_stop_button_release)
        self.ui.CreateTask_PushButton.released.connect(self.on_create_task_button_release)
        self.ui.ClearTask_PushButton.released.connect(self.on_clear_task_button_release)

        # self.ui.
        # connect widgets to controller
        # self.ui.spinBox_amount.valueChanged.connect(self._main_controller.change_amount)
        # self.ui.pushButton_reset.clicked.connect(lambda: self._main_controller.change_amount(0))

    @Slot(int)
    def on_frame_duration_changed(self, value):
        self.ui.BufferDuration_SpinBox.setMinimum(value)
        self.ui.UpdateInterval_SpinBox.setMinimum(value)

    @Slot()
    def on_create_task_button_release(self):
        self.ui.Start_PushButton.setEnabled(True)
        self.ui.ClearTask_PushButton.setEnabled(True)
        self.ui.CreateTask_PushButton.setDisabled(True)
        self.ui.PreparationSetting_Frame.setDisabled(True)

    @Slot()
    def on_clear_task_button_release(self):
        self.ui.PreparationSetting_Frame.setEnabled(True)
        self.ui.CreateTask_PushButton.setEnabled(True)
        self.ui.Start_PushButton.setDisabled(True)
        self.ui.ClearTask_PushButton.setDisabled(True)

    @Slot()
    def on_start_button_release(self):
        self.ui.Stop_PushButton.setEnabled(True)
        self.ui.Start_PushButton.setDisabled(True)
        self.ui.Reset_PushButton.setDisabled(True)
        self.ui.ClearTask_PushButton.setDisabled(True)

    @Slot()
    def on_stop_button_release(self):
        self.ui.Start_PushButton.setEnabled(True)
        self.ui.ClearTask_PushButton.setEnabled(True)
        self.ui.Reset_PushButton.setEnabled(True)
        self.ui.Stop_PushButton.setDisabled(True)
