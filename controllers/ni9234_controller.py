#from ..model.NIdaqModel import DAQModel
from PySide6.QtCore import QObject, Slot


class NI9234Controller(QObject):
    def __init__(self, model):
        super().__init__()
        self._model = model

    @Slot(int)
    def change_sample_rate(self, value):
        self._model.sample_rate = value

    @Slot(int)
    def change_frame_duration(self, value):
        self._model.frame_duration = value

    @Slot(int)
    def change_buffer_duration(self, value):
        self._model.buffer_duration = value

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
    def sensor_types(self, value):
        self._model.sensor_types = value
