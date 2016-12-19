from __future__ import absolute_import
import sys
import unittest

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget, QDesktopWidget, QStackedLayout
from PyQt5.QtTest import QTest

from market.controllers.main_view_controller import MainWindowController
from market.views.main_view import Ui_MainWindow

from marketGUI.market_app import TestMarketApplication


class GUITestSuite(unittest.TestCase):
    def setUp(self):
        self.app = TestMarketApplication(sys.argv)
        self.window = MainWindowController(app=self.app, ui_location='../../ui/mainwindow.ui')
        # self.app.exec_()

    def tearDown(self):
        # sys.exit()
        pass

    def test_login_generate(self):
        # Test the generate button. Make sure a new user can login once he generated a new key
        self.assertEqual(0, self.window.stackedWidget.currentIndex())
        QTest.mouseClick(self.window.login_generate_pushbutton, Qt.LeftButton)
        QTest.mouseClick(self.window.login_login_pushbutton, Qt.LeftButton)

        # Confirm is the user returned is equal to the user created.
        self.assertEqual(1, self.window.stackedWidget.currentIndex())

        # TODO check if the right file has been saved

        # TODO delete created private and public key files

    #
    # def test_login_remembered(self):
    #     pass
    #
    # def test_login_browse(self):
    #     pass