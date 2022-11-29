#from ..model.NIdaqModel import DAQModel
from PySide6.QtCore import QObject, Slot
import numpy.typing as npt


class NI9234Controller(QObject):
    def __init__(self, model):
        super().__init__()
        self._model = model

    @Slot(str)
    def change_task_name(self, value):
        self._model.task_name = value

    @Slot(int)
    def change_sample_rate(self, value):
        self._model.sample_rate = value

    @Slot(int)
    def change_frame_duration(self, value):
        self._model.frame_duration = value

    @Slot(int)
    def change_buffer_rate(self, value):
        self._model.buffer_rate = value
        self._model.buffer_duration = self._model.frame_duration

    @Slot(int)
    def change_update_interval(self, value):
        self._model.update_interval = value

    @Slot(int)
    def change_downsample(self, value):
        self._model.downsample = value

    @Slot(list)
    def change_channels(self, value):
        self._model.channels = value

    @Slot(list)
    def change_sensor_types(self, value):
        self._model.sensor_types = value

    @Slot(bool)
    def change_write_file_flag(self, value):
        self._model.write_file_flag = value

    @Slot(str)
    def change_write_file_dir(self, value):
        self._model.write_file_dir = value

    @Slot()
    def read_wave_data_buffer(self) -> npt.NDArray:
        return self._model._wave_data_buffer
