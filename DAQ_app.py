import sys
from PySide6.QtWidgets import QApplication
from model.ModelNIDAQ import NIDAQModel
from views.ni9234_viewmodel import NI9234ViewModel


class App(QApplication):
    def __init__(self, sys_argv=None):
        super(App, self).__init__()
        self.model = NIDAQModel()
        self.main_view = NI9234ViewModel(self.model)
        self.main_view.show()


if __name__ == '__main__':
    app = App()
    sys.exit(app.exec())
