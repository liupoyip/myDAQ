from .ui_ni9234 import Ui_NI9234
from PySide6.QtWidgets import QWidget, QMessageBox
from PySide6.QtCore import Slot, QTimer


class NI9234View(QWidget, Ui_NI9234):
    def __init__(self, model=None, controller=None):
        super().__init__()
        self._model = model
        self._controller = controller
        self._ui = Ui_NI9234()
        self._ui.setupUi(self)

        # listen for model event signals
        self._ui.TaskName_LineEdit.textChanged.connect(self.on_task_name_changed)
        self._ui.FrameDuration_SpinBox.valueChanged.connect(self.on_frame_duration_changed)
        self._ui.Reset_PushButton.clicked.connect(self.set_default_values)
        self._ui.Start_PushButton.clicked.connect(self.on_start_button_clicked)
        self._ui.Stop_PushButton.clicked.connect(self.on_stop_button_clicked)
        self._ui.CreateTask_PushButton.clicked.connect(self.on_create_task_button_clicked)
        self._ui.ClearTask_PushButton.clicked.connect(self.on_clear_task_button_clicked)

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

        self.set_default_values()

    def set_default_values(self):
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

        self._ui.BufferDuration_SpinBox.setValue(
            self._ui.FrameDuration_SpinBox.value())
        self._ui.BufferDuration_SpinBox.setMinimum(
            self._ui.FrameDuration_SpinBox.value())
        self._ui.BufferDuration_SpinBox.setMaximum(
            self._model._default_settings['max_buffer_duration'])
        self._ui.BufferDuration_HorizontalSlider.setValue(
            self._ui.FrameDuration_SpinBox.value())
        self._ui.BufferDuration_HorizontalSlider.setMinimum(
            self._ui.FrameDuration_SpinBox.value())
        self._ui.BufferDuration_HorizontalSlider.setMaximum(
            self._model._default_settings['max_buffer_duration'])

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

        # set initial disable component
        self._ui.CreateTask_PushButton.setEnabled(True)
        self._ui.Stop_PushButton.setDisabled(True)
        self._ui.Start_PushButton.setDisabled(True)
        self._ui.ClearTask_PushButton.setDisabled(True)
        self._ui.WriteFile_GroupBox.setDisabled(True)

        for checkbox, combox in zip(self._channel_checkbox_list, self._channel_combox_list):
            combox.clear()
            combox.addItems(self._model._default_settings["sensor_type"])
            combox.setDisabled(True)
            checkbox.setChecked(False)

    @Slot(str)
    def on_task_name_changed(self):
        self._controller.change_task_name(self._ui.TaskName_LineEdit.text())

    @Slot(int)
    def on_frame_duration_changed(self, value):
        self._ui.BufferDuration_SpinBox.setMinimum(value)
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
                f'Buffer Duration: {self._ui.BufferDuration_SpinBox.value()} ms\n')

            self._controller.change_sample_rate(self._ui.SampleRate_SpinBox.value())
            self._controller.change_frame_duration(self._ui.FrameDuration_SpinBox.value())
            self._controller.change_buffer_duration(self._ui.BufferDuration_SpinBox.value())
            self._controller.change_update_interval(self._ui.UpdateInterval_SpinBox.value())
            self._controller.change_downsample(self._ui.DownSample_SpinBox.value())
            channels, sensor_types = self.add_channels()
            self._controller.change_channels(channels)
            self._controller.change_sensor_types(sensor_types)
            self._model.create()

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
        self._model.start()

    @Slot()
    def on_stop_button_clicked(self):
        self._ui.Start_PushButton.setEnabled(True)
        self._ui.ClearTask_PushButton.setEnabled(True)
        self._ui.Reset_PushButton.setEnabled(True)
        self._ui.Stop_PushButton.setDisabled(True)
        self._model.stop()

    @Slot()
    def on_write_file_checkbox_toggled(self):
        self._controller.change_write_file_flag(self._ui.WriteFile_CheckBox.isChecked())
        self._model.ready_write_file()

    def check_channel_options(self):
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
