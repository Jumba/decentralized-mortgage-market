import tftpy
import os
import threading
import time
import logging


class Server:
    def __init__(self):
        self.server = tftpy.TftpServer(os.getcwd())
        tftpy.setLogLevel('INFO')
        fh = logging.FileHandler(os.getcwd()+'/logging/log_server_'+time.strftime('%d-%m-%Y_%H:%M:%S'))
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        tftpy.log.addHandler(fh)
        try:
            self.thread = threading.Thread(target=self.server_start)
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

    def server_start(self):
        self.server.listen(listenport=50000)

    @staticmethod
    def set_logging(level, filename=None):
        if not file:
            tftpy.log.FileHandler(os.getcwd()+'/logging/'+filename)
        tftpy.setLogLevel(level)


if __name__ == '__main__':
    ts = Server()
    ts.start()
    time.sleep(3)
    ts.stop()
