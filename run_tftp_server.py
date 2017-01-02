import tftpy
import os

server = tftpy.TftpServer(os.getcwd())
server.listen()
