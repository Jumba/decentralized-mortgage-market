import tftpy
import os
import threading


class Server:
    def __init__(self):
        self.server = tftpy.TftpServer(os.getcwd())
        self.thread = threading.Thread(target=self.server_start)

    def stop(self):
        if self.server.is_running:
            self.server.stop()

    def start(self):
        self.thread.start()

    def server_start(self):
        self.server.listen(listenport=50000)


if __name__ == '__main__':
    ts = Server()
    ts.start()
