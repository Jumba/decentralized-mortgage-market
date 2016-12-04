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
        self.setNavigaiton()
        # self.
        # for i in range(1, 9):

    def setNavigaiton(self):
        self.next_1.clicked.connect(self.switchScreens)
        self.next_2.clicked.connect(self.switchScreens)
        self.next_3.clicked.connect(self.switchScreens)
        self.next_4.clicked.connect(self.switchScreens)
        self.next_5.clicked.connect(self.switchScreens)
        self.next_6.clicked.connect(self.switchScreens)
        self.next_7.clicked.connect(self.switchScreens)
        self.next_8.clicked.connect(self.switchScreens)

    def switchScreens(self):
        # print 'next'
        current = self.currentIndex()
        print current
        self.setCurrentIndex((current + 1) % 8)



def main():
    app = MarketApplication(sys.argv)
    mainwindow = MainWindowController(app=app)
    mainwindow.show()
    app.exec_()


if __name__ == '__main__':
    main()
