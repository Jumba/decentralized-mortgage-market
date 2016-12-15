import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from market.views.main_view import Ui_MainWindow
from marketGUI.market_app import MarketApplication
from market.api.api import MarketAPI


class BorrowersPortfolioController:
    def __init__(self, mainwindow):
        # self.mainwindow = Ui_MainWindow  # Comment before running
        self.mainwindow = mainwindow  # Uncomment before running


    def setup_view(self):
        pass
