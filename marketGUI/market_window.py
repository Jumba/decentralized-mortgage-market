import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget, QDesktopWidget, QStackedLayout

from marketGUI.widgets.login import LoginWidget


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

        # # Install signal handler for ctrl+c events
        # def sigint_handler(*_):
        #     self.close_market()
        #
        # signal.signal(signal.SIGINT, sigint_handler)


        self.stackedLayout = QStackedLayout()

        #
        login = LoginWidget(self)
        login.setupUi(self)

        login.loginButton.clicked.connect(lambda _: login.keyField.setText('aribaa'))

        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)

        self.central_widget.addWidget(login)
        self.central_widget.setCurrentWidget(login)

        self.initUI()
        self.show()

    def initUI(self):
        self.setWindowTitle('Decentralized Market Community')
        self.resize(1300, 700)
        self._center()

    def set_status(self, status=''):
        self.statusBar().showMessage(status)

    def _center(self):
        fg = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        fg.moveCenter(center_point)
        self.move(fg.topLeft())

    def on_tribler_started(self):
        pass

    def close_market(self):
        QApplication.quit()
