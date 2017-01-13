from __future__ import absolute_import
import os
import logging
import threading
import unittest
import time
import tftpy

import run_tftp_client
from run_tftp_server import Server
from run_tftp_client import Client, TransferQueue
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
        self.queue = TransferQueue()
        self.document_path_client = os.path.normpath(os.getcwd()+'/../../resources/documents/')
        self.document_path_host = os.path.normpath(os.getcwd()+'/../../resources/')
        # self.client_mock = MagicMock()
        # self.client.client = self.client_mock

    # def tearDown(self):
        # self.assertTrue(self.server.is_running())
        # self.server.stop()
        # self.assertFalse(self.server.is_running())

    def throw(self, exception):
        raise exception()

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
        mock.assert_called_once_with(os.getcwd()+'/resources/received/file1.pdf', 'file1.pdf')

    def test_client_upload_folder_default_path(self):
        mock = MagicMock()
        self.client.file_search = lambda x: [os.getcwd()+'/resources/received/file1.pdf']
        self.client.upload = mock
        self.client.upload_folder()
        mock.assert_called_once_with(os.getcwd()+'/resources/received/file1.pdf')

    def test_client_upload_folder_custom_path(self):
        mock = MagicMock()
        self.client.file_search = lambda x: [os.path.normpath(os.getcwd()+'/resources/received/file1.pdf')]
        self.client.upload = mock
        self.client.upload_folder(host_path='/received/')
        mock.assert_called_once_with(os.path.normpath(os.getcwd()+'/resources/received/file1.pdf'),
                                     '/received/file1.pdf')

    def test_enable_logging(self):
        tftpy.log.addHandler = MagicMock()
        logging.FileHandler = MagicMock()
        tftpy.setLogLevel(0)
        self.assertEqual(tftpy.log.level, 0)
        self.client.enable_logging()
        self.assertEqual(tftpy.log.level, 20)
        tftpy.setLogLevel(0)

    def test_queue_construction(self):
        self.assertEqual(self.queue.jobs, [])
        self.assertEqual(self.queue.failed, [])
        self.assertEqual(self.queue.sent, [])
        self.assertTrue(isinstance(self.queue, TransferQueue))

    def test_queue_add(self):
        self.assertEqual(self.queue.jobs, [])
        self.queue.add('127.0.0.1', 69, run_tftp_client.DEFAULT_CLIENT_PATH, run_tftp_client.DEFAULT_HOST_PATH)
        self.assertEqual(self.queue.jobs, [('127.0.0.1', 69, run_tftp_client.DEFAULT_CLIENT_PATH,
                                            run_tftp_client.DEFAULT_HOST_PATH)])

    def test_queue_upload_all(self):
        mock = MagicMock()
        self.queue.upload_list = mock
        self.queue.add('127.0.0.1', 79, run_tftp_client.DEFAULT_CLIENT_PATH, run_tftp_client.DEFAULT_HOST_PATH)
        self.queue.upload_all()
        mock.assert_called_once_with(self.queue.jobs)

    def test_queue_retry_failed(self):
        mock = MagicMock()
        self.queue.upload_list = mock
        self.queue.failed.append(('127.0.0.1', 89, run_tftp_client.DEFAULT_CLIENT_PATH,
                                  run_tftp_client.DEFAULT_HOST_PATH))
        self.queue.retry_failed()
        mock.assert_called_once_with(self.queue.failed)

    def test_upload_list_success(self):
        mock1 = MagicMock()
        mock2 = MagicMock()
        Client.upload = mock1
        Client.upload_folder = mock2
        self.queue.add('127.0.0.1', 99, self.document_path_client, self.document_path_host)
        self.queue.add('127.0.1.1', 101, self.document_path_client+'/file.pdf',
                       self.document_path_host+'/file.pdf')
        self.assertEqual(self.queue.jobs, [('127.0.0.1', 99, self.document_path_client, self.document_path_host),
                                           ('127.0.1.1', 101,self.document_path_client+'/file.pdf',
                                            self.document_path_host+'/file.pdf')])
        self.assertTrue(self.queue.upload_list(self.queue.jobs))
        mock1.assert_called_once_with(self.document_path_client+'/file.pdf', self.document_path_host+'/file.pdf')
        mock2.assert_called_once_with(self.document_path_client, self.document_path_host)
        self.assertEqual(self.queue.failed, [])

    def test_upload_list_fail(self):
        Client.upload_folder = lambda x, y, z: self.throw(tftpy.TftpException)
        self.queue.add('127.0.0.1', 99, self.document_path_client, self.document_path_host)
        self.assertEqual(self.queue.jobs, [('127.0.0.1', 99, self.document_path_client, self.document_path_host)])
        self.assertFalse(self.queue.upload_list(self.queue.jobs))
        self.assertEqual(self.queue.failed, [('127.0.0.1', 99, self.document_path_client, self.document_path_host)])
        self.assertEqual(self.queue.sent, [])
