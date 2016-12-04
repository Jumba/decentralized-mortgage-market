import os
import sys

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from market.views import main_view
from marketGUI.market_app import MarketApplication


class MainWindowController(QStackedWidget, main_view.Ui_StackedWidget):
    def __init__(self, parent=None, app=None):
        super(MainWindowController, self).__init__(parent)
        self.app = app
        self.setupUi(self)
        self.setCurrentIndex(0)


def main():
    app = MarketApplication(sys.argv)
    mainwindow = MainWindowController(app=app)
    mainwindow.show()
    app.exec_()


if __name__ == '__main__':
    main()
