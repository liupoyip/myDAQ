import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QTextStream, Qt
from model.ModelNIDAQ import NIDAQModel
from views.ni9234_viewmodel import NI9234ViewModel
from PySide6.QtGui import QPen, QColor, QPalette, QGuiApplication
import qdarktheme


class App(QApplication):
    def __init__(self, sys_argv=None):
        super(App, self).__init__()
        self.model = NIDAQModel()
        self.main_view = NI9234ViewModel(self.model)
        self.main_view.show()


app = App()
app.setStyleSheet(qdarktheme.load_stylesheet())
sys.exit(app.exec())
