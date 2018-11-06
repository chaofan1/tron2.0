import socket
from remind import Remind


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
    Remind().remind_start(file_number)
    data = h.recv(1024)
    if 'Submit sucess, task_id' in data:
        Remind().remind_success(file_number)
        # remind('True', file_number)
    else:
        Remind().remind_fail(data, file_number)
        # remind(data, file_number)
    h.close()


if __name__ == '__main__':
    client('1')
