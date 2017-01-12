from __future__ import absolute_import
import os
import logging
import threading
import unittest
import time
import tftpy
from run_tftp_server import Server
from run_tftp_client import Client
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

    def setUp(self):
        self.client = Client()
        self.tftp_client = self.client.client
        # self.client_mock = MagicMock()
        # self.client.client = self.client_mock

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

    def test_set_logging(self):
        tftpy.log.addHandler = MagicMock()
        logging.FileHandler = MagicMock()
        tftpy.setLogLevel(0)
        self.assertEqual(tftpy.log.level, 0)
        Server.set_logging(os.getcwd(), 'ERROR')
        self.assertEqual(tftpy.log.level, 40)
        tftpy.setLogLevel(0)

    def test_client_construction(self):
        self.assertEqual(self.client.files, [])
        self.assertTrue(isinstance(self.client, Client))

    def test_client_upload_custom_remote_path(self):
        mock = MagicMock()
        self.tftp_client.upload = mock
        self.client.upload('file1.pdf', 'file2.pdf')
        mock.assert_called_once_with('file2.pdf', 'file1.pdf')

    def test_client_upload_default_remote_path(self):
        mock = MagicMock()
        self.tftp_client.upload = mock
        self.client.upload('file1.pdf')
        mock.assert_called_once_with('/home/arthur/Documents/git/mockchain-market/'
                                     'test/market/resources/received/file1.pdf', 'file1.pdf')

    def test_client_upload_folder_default_path(self):
        mock = MagicMock()
        self.client.file_search = lambda x: ['/home/arthur/Documents/git/mockchain-market'
                                             '/resources/received/file1.pdf']
        self.client.upload = mock
        self.client.upload_folder()
        mock.assert_called_once_with('/home/arthur/Documents/git/mockchain-market/resources/'
                                     'received/file1.pdf')

    def test_client_upload_folder_custom_path(self):
        mock = MagicMock()
        self.client.file_search = lambda x: ['/home/arthur/Documents/git/mockchain-market'
                                             '/resources/received/file1.pdf']
        self.client.upload = mock
        self.client.upload_folder(host_path='/received/')
        mock.assert_called_once_with('/home/arthur/Documents/git/mockchain-market/resources/received/file1.pdf',
                                     '/received/file1.pdf')

    def test_enable_logging(self):
        tftpy.log.addHandler = MagicMock()
        logging.FileHandler = MagicMock()
        tftpy.setLogLevel(0)
        self.assertEqual(tftpy.log.level, 0)
        self.client.enable_logging()
        self.assertEqual(tftpy.log.level, 20)
        tftpy.setLogLevel(0)

