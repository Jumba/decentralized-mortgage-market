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
DEFAULT_HOST_PATH = ''
DEFAULT_PORT = 50000


class Client:
    """
        Create a Client object that uses the tftpy module to connect to a TFTP server.
        Makes it possible to download from or upload to a TFTP server.
        Only accepts .pdf files.
    """
    def __init__(self, host_ip=socket.gethostbyname(socket.gethostname()), port=DEFAULT_PORT):
        self.client = TftpClient(host_ip, port)
        self.files = []
        self.file_search = glob.glob

    def upload(self, local_file_name, remote_file_name=None):
        """
            Uploads a file to the server.
        :param local_file_name: Path of the file locally
        :param remote_file_name: Path where the file will be written to on the server.
        """
        if not remote_file_name:
            remote_file_name = DEFAULT_HOST_PATH + ntpath.basename(local_file_name)
        self.client.upload(remote_file_name, local_file_name)

    def upload_folder(self, path=DEFAULT_CLIENT_PATH, host_path=None):
        """
            :param path: Local path of the folder.
            :param host_path: Path of the folder on the server where files will be written to.
        """
        self.files = self.file_search(path + '/*.pdf')
        for f in self.files:
            if not host_path:
                self.upload(f)
            else:
                self.upload(f, host_path+ntpath.basename(f))

    @staticmethod
    def enable_logging():
        """
            Enables logging for the tftpy module.
        """
        tftpy.setLogLevel('INFO')
        fh = logging.FileHandler(os.getcwd()+'/logging/log_client_'+time.strftime('%d-%m-%Y_%H:%M:%S'))
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        tftpy.log.addHandler(fh)


class TransferQueue:
    """
        Creates a TransferQueue object used for sending files.
        Remembers the files that that have and have not been sent.
    """
    def __init__(self):
        self.jobs = []
        self.failed = []
        self.sent = []

    def add(self, ip_address, host_port, local_files, remote_files):
        """
            Adds a job to the list of files that need to be sent.
           :param ip_address: IP address of the TFTP server.
           :param host_port: Port of on which the server is being hosted.
           :param local_files: File path of the document(s) that need to be sent.
           :param remote_files: Path which the files will be written to on the server.
        """
        self.jobs.append((ip_address, host_port, local_files, remote_files))

    def upload_all(self):
        """
            Uploads all files that have been previously added.
        """
        self.upload_list(self.jobs)

    def retry_failed(self):
        """
            Uploads all files that were not able to be sent.
        """
        failed_jobs = self.failed
        self.failed = []
        self.upload_list(failed_jobs)

    def upload_list(self, jobs):
        """
             Upload files to all hosts one by one, return true and run the response if no problems were found.
             If some files were not able to be sent, return the tuple.
            :param jobs: Tuples of files and their destination
        """
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

