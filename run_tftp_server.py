import tftpy
import os
import threading


class TftpServer:
    def __init__(self):
        self.server = tftpy.TftpServer(os.getcwd())
        self.server_thread = threading.Thread(target=self.server_start)

    def stop(self):
        if self.server.is_running:
            self.server.stop()

    def start(self):
        self.server_thread.start()

    def server_start(self):
        self.server.listen(listenport=6969)


if __name__ == '__main__':
    ts = TftpServer()
    ts.start()
