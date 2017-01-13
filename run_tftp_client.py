import socket
import os
import glob
import ntpath
import tftpy
from tftpy import TftpClient
from threading import Thread
import time
import logging

DEFAULT_CLIENT_PATH = os.getcwd()+'/resources/documents/'
DEFAULT_HOST_PATH = os.getcwd()+'/resources/received/'
DEFAULT_PORT = 50000


class Client:
    def __init__(self, host_ip=socket.gethostbyname(socket.gethostname()), port=DEFAULT_PORT):
        self.client = TftpClient(host_ip, port)
        self.files = []
        self.file_search = glob.glob

    def upload(self, local_file_name, remote_file_name=None):
        if not remote_file_name:
            remote_file_name = DEFAULT_HOST_PATH + ntpath.basename(local_file_name)
        self.client.upload(remote_file_name, local_file_name)

    def upload_folder(self, path=DEFAULT_CLIENT_PATH, host_path=None):
        self.files = self.file_search(path + '/*.pdf')
        for f in self.files:
            if not host_path:
                self.upload(f)
            else:
                self.upload(f, host_path+ntpath.basename(f))

    @staticmethod
    def enable_logging():
        tftpy.setLogLevel('INFO')
        fh = logging.FileHandler(os.getcwd()+'/logging/log_client_'+time.strftime('%d-%m-%Y_%H:%M:%S'))
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        tftpy.log.addHandler(fh)


class TransferQueue:
    def __init__(self):
        self.jobs = []
        self.failed = []
        self.sent = []

    def add(self, ip_address, host_port, local_files, remote_files):
        self.jobs.append((ip_address, host_port, local_files, remote_files))

    def upload_all(self):
        self.upload_list(self.jobs)

    def retry_failed(self):
        self.upload_list(self.failed)

    def upload_list(self, jobs):
        # Upload files to all hosts one by one, return true and run the response if no problems were found.
        # If some files were not able to be sent, return the tuple.
        for job in jobs:
            ip_address, host_port, local_files, remote_files = job
            try:
                client = Client(ip_address, host_port)
                if os.path.isdir(local_files):
                    client.upload_folder(local_files, remote_files)
                    self.sent.append(job)
                else:
                    client.upload(local_files, remote_files)
                self.sent.append(job)
            except tftpy.TftpException as e:
                self.failed.append(job)
                print e.message
        if self.failed:
            return False
        else:
            return True

