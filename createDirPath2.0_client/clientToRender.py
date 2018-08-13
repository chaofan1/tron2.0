import socket
from render_progress import consumer
import os


def produce(c,filePath, Utask):
    c.send(None)

    HOST = "192.168.100.88"
    PORT = 19900
    args = filePath+"|"+Utask
    h = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    h.connect((HOST, PORT))
    h.sendall(args)

    for chunk in iter(lambda:h.recv(1024),b''):
        print(chunk)
        c.send(chunk)

    h.close()


def client(dataTo):
    if len(dataTo) == 0:
        print "not good in the loop"
    computerIP, filePath, Utask = dataTo.split('|')
    sep = os.sep
    filename = filePath.split(sep)[-1]
    c = consumer(filename)
    produce(c,filePath, Utask)
    return 'True'


if __name__ == '__main__':
    client('1')