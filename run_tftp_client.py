import socket
import os
import glob
import ntpath
from tftpy import TftpClient
from threading import Thread

class Client:
    def __init__(self):
        self.resources = None
        self.client = TftpClient(socket.gethostbyname(socket.gethostname()), 50000)
        self.sent_files = []
        self.files = []
        self.failed_to_send = []
        # self.thread = Thread

    def upload(self, local_file_name, remote_file_name=None):
        if not remote_file_name:
            remote_file_name = '/resources/received/' + ntpath.basename(local_file_name)
        try:
            self.client.upload(remote_file_name, local_file_name)
        except:
            print 'Uploading of ', remote_file_name, ' failed.'
            raise
            # TODO add the file to queue of failed uploads

    def download(self, remote_file_name, local_file_name=None):
        if not local_file_name:
            local_file_name = '/resources/received/' + ntpath.basename(remote_file_name)
        try:
            self.client.download(local_file_name, remote_file_name)
        except:
            raise

    def upload_folder(self, path=os.getcwd()+'/resources'):
        self.files = glob.glob(path+'/*.pdf')
        print self.files
        for f in self.files:
            self.upload(f)

if __name__ == '__main__':
    tc = Client()
    # tc.upload('server.pdf', 'downloaded.pdf')
    tc.upload_folder()


