#from ..model.NIdaqModel import DAQModel
from PySide6.QtCore import QObject, Slot


class NI9234Controller(QObject):
    def __init__(self, model):
        super().__init__()
        self._model = model

    def change_task_name(self, value):
        self._model.task_name = value

    def change_sample_rate(self, value):
        self._model.sample_rate = value

    def change_frame_duration(self, value):
        self._model.frame_duration = value

    def change_buffer_duration(self, value):
        self._model.buffer_duration = value

    def change_update_interval(self, value):
        self._model.update_interval = value

    def change_downsample(self, value):
        self._model.downsample = value

    def change_channels(self, value):
        self._model.channels = value

    def change_sensor_types(self, value):
        self._model.sensor_types = value

    def change_write_file_trig(self, value):
        self._model.write_file_trig = value

    def change_write_file_dir(self, value):
        self._model.write_file_dir = value
