import tftpy
import socket

client = tftpy.TftpClient(socket.gethostbyname(socket.gethostname()), 69)
client.download('server.txt', 'downloaded.txt')