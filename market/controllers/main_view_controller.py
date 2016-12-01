import sys
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import run_gui, profile_controller
from market.views import main_screen
from market.api.api import MarketAPI
from marketGUI.market_app import MarketApplication


class MainController(QStackedWidget, main_screen.Ui_StackedWidget):
    def __init__(self, parent=None, app=None):
        super(MainController, self).__init__(parent)
        self.setupUi(self)
        self.app = app
        self.loginButton.clicked.connect(self.switchbitch)
       # self.profile_controller = profile_controller.ProfileController()

    def switchbitch(self):
        self.setCurrentIndex(1)



def main():
    app = MarketApplication(sys.argv)
    form = MainController(app=app)
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
