import tftpy
import os
import threading
import time
import logging

DEFAULT_PORT = 50000


class Server:
    def __init__(self, port=DEFAULT_PORT):
        self.server = tftpy.TftpServer(os.getcwd())
        self.port = port
        try:
            self.thread = threading.Thread(target=self.server_listen)
        except:
            tftpy.log.error('The socket was not properly closed after the last run. '
                            'Please kill the process or try again in a couple of minutes.'
                            'Process id can be found by using the \'lsof -i UDP\' command '
                            'to find the right PID then followed by \'kill PID\' ')
            raise

    def stop(self):
        if self.server.is_running:
            self.server.stop()

    def start(self):
        self.thread.start()

    def server_listen(self):
        self.server.listen(listenport=self.port)

    @staticmethod
    def set_logging(write_path, level):
        tftpy.setLogLevel(level)
        fh = logging.FileHandler(write_path+'log_server_'+time.strftime('%d-%m-%Y_%H:%M:%S'))
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        tftpy.log.addHandler(fh)

if __name__ == '__main__':
    ts = Server()
    ts.set_logging(os.getcwd()+'/logging/')
    ts.start()
