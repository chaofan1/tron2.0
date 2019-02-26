import SocketServer
import client
import config
import socket

host = config.server_ip
port = config.server_port


def handle_client(args):
	if args:
		client_ = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		client_.connect((host, port))
		client_.sendall(args)
		client_.close()


class MyTCPHandler(SocketServer.BaseRequestHandler):
	def handle(self):
		while True:
			data = self.request.recv(1024)
			if not data:
				# print "client %s is dead!" % self.client_address[0]
				break
			client.clientLink(data)


if __name__ == "__main__":
	server = SocketServer.ThreadingTCPServer((host,port),MyTCPHandler)
	server.serve_forever()
