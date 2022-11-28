import sys
from PySide6.QtWidgets import QApplication
from model.ModelNIDAQ import NIDAQModel
from controllers.ni9234_crtl import NI9234Controller
from views.ni9234_view import NI9234View


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        self.model = NIDAQModel()
        self.main_controller = NI9234Controller(self.model)
        self.main_view = NI9234View(self.model, self.main_controller)
        self.main_view.show()


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec())
