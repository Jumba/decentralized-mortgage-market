import tftpy
import os
import threading
import time
import logging

DEFAULT_PORT = 50000


class Server:
    """
        Create a Server object that uses the tftpy module to host a TFTP server
    """
    def __init__(self, port=DEFAULT_PORT):
        self.server = tftpy.TftpServer(os.getcwd())
        self.port = port
        self.thread = threading.Thread(target=self.server_listen)

    def stop(self, now=False):
        """
            Stops the server and frees the socket.
            :param now: False by default, will wait for processes to end before shutting down.
            True if the server needs to be killed immediately.
        """
        self.server.stop(now)

    def start(self):
        """
            Starts the thread which will initiate the server.
        """
        self.thread.start()

    def server_listen(self):
        """
            Start listening to the given port. Will initiate the endless loop and wait for any events.

            If the method returns a thread error then the socket was not closed properly the last run.
            The socket can be free by manually killing the process.
            Process id can be found by using the \'lsof -i UDP\' command
            to find the right PID then followed by \'kill PID\'
        """
        self.server.listen(listenport=self.port)

    def is_running(self):
        """
            Checks if the server is currently active.

        :return: True if the server is running, False if the server is not.
        """
        return self.server.is_running.is_set()

    @staticmethod
    def set_logging(write_path, level):
        """
            Sets the logging level and adds a FileHandler object to write the logging to file.
        :param write_path: The path where the file should be written.
        :param level: Desired level of logging.
        """
        tftpy.setLogLevel(level)
        fh = logging.FileHandler(write_path+'log_server_'+time.strftime('%d-%m-%Y_%H:%M:%S'))
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        tftpy.log.addHandler(fh)
