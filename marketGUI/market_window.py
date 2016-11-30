import signal
import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget, QVBoxLayout

from marketGUI.widgets.login import LoginPage
from marketGUI.widgets.profile import ProfilePage

class MarketWindow(QMainWindow):
    resize_event = pyqtSignal()
    escape_pressed = pyqtSignal()
    received_search_completions = pyqtSignal(object)

    def on_exception(self, *exc_info):
        print exc_info
        self.close_market()

    def __init__(self):
        QMainWindow.__init__(self)

        sys.excepthook = self.on_exception

        # Install signal handler for ctrl+c events
        def sigint_handler(*_):
            self.close_market()

        self.stackedWidget = QStackedWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.stackedWidget)
        self.setLayout(layout)
        profile = ProfilePage()
        #profile.initialize(self)

        login = LoginPage()
        #login.initialize(self)

        li = self.stackedWidget.addWidget(login)
        pi = self.stackedWidget.addWidget(profile)



        self.stackedWidget.setCurrentIndex(0)


        signal.signal(signal.SIGINT, sigint_handler)

        self.show()


    def on_tribler_started(self):
        pass

    def close_market(self):
        QApplication.quit()
