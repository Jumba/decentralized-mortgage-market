from __future__ import absolute_import
import os
import logging
import threading
import unittest

import time

import tftpy

from run_tftp_server import Server
from uuid import UUID
from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from market.controllers.main_window_controller import MainWindowController
from marketGUI.market_app import TestMarketApplication
from mock import MagicMock


class DocumentTransferTestSuite(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server = Server()
        # Server.set_logging(os.path.normpath(os.getcwd() + '/../../logging/'), 'INFO')
        cls.server.start()
        time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    # def setUp(self):
        # self.server = self.__class__.server
        # print type(self.server)

    # def tearDown(self):
        # self.assertTrue(self.server.is_running())
        # self.server.stop()
        # self.assertFalse(self.server.is_running())

    def test_server_construction(self):
        self.assertTrue(isinstance(self.server, Server))
        self.assertTrue(isinstance(self.server.thread, threading.Thread))

    def test_server_running(self):
        self.assertTrue(self.server.is_running())

    def test_server_not_running(self):
        server2 = Server()
        self.assertFalse(server2.is_running())

    def test_logging(self):
        tftpy.log.addHandler = MagicMock()
        logging.FileHandler = MagicMock()
        loglevel1 = tftpy.log.level
        self.assertEqual(loglevel1, 0)
        Server.set_logging(os.getcwd(), 'ERROR')
        loglevel2 = tftpy.log.level
        self.assertEqual(loglevel2, 40)




