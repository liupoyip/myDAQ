import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QTextStream, Qt
from PySide6.QtGui import QPen, QColor, QPalette, QGuiApplication

from models.ModelNIDAQ import NIDAQModel
from views.ni9234_viewmodel import NI9234ViewModel
# import qdarktheme


class App(QApplication):
    def __init__(self, sys_argv=None):
        super(App, self).__init__()
        self.model = NIDAQModel()
        self.view = NI9234ViewModel(self.model)
        self.focusChanged.connect(self.view.on_focus_changed)

        self.view.show()


app = App()
# app.setStyleSheet(qdarktheme.load_stylesheet())
sys.exit(app.exec())
