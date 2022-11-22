import sys
from PySide6.QtWidgets import QApplication, QMainWindow
#from model.model import Model
#from controllers.main_ctrl import MainController
from views.ni9234_form import NI9234Form


class App(QApplication):
    def __init__(self, sys_argv):
        super(App, self).__init__(sys_argv)
        # self.model = Model()
        # self.main_controller = MainController(self.model)
        # self.main_view = MainView(self.model, self.main_controller)
        self.ni9234_view = NI9234Form()

        self.ni9234_view.show()


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec())
