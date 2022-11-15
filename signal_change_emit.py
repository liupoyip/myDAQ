from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget


class Foo(QWidget):
    valueChanged = Signal(object)

    def __init__(self, parent=None):
        super(Foo, self).__init__(parent)
        self._t = 0

    @property
    def t(self):
        return self._t

    @t.setter
    def t(self, value):
        self._t = value
        self.valueChanged.emit(value)


foo = Foo()
foo.t = 5
