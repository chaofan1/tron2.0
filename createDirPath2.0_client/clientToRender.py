import socket
from render_remind import remind


def client(dataTo):
    HOST = "192.168.100.88"
    PORT = 19900
    computerIP, filePath, Utask = dataTo.split('|')
    file_number = ''
    try:
        file_number = filePath.split('_')[0][-9:]
    except:
        pass
    args = filePath+"|"+Utask
    h = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    h.connect((HOST, PORT))
    h.sendall(args)
    remind('send', file_number)
    data = h.recv(1024)
    if 'Submit sucess, task_id' in data:
        remind('True', file_number)
    else:
        remind(data, file_number)
    h.close()


if __name__ == '__main__':
    client('1')
