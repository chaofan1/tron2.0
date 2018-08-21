#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-

import socket
from threading import Thread
import renderTcp
from Queue import Queue

# host = "192.168.100.88"
host = socket.gethostbyname(socket.gethostname())
port = 19900
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((host, port))
server.listen(5)


class ThreadPoolManger():
    def __init__(self, thread_num):
        self.work_queue = Queue()
        self.thread_num = thread_num
        self.__init_threading_pool(self.thread_num)

    def __init_threading_pool(self, thread_num):
        for i in range(thread_num):
            thread = ThreadManger(self.work_queue)
            thread.start()

    def add_job(self, func, *args):
        self.work_queue.put((func, args))


class ThreadManger(Thread):
    def __init__(self, work_queue):
        Thread.__init__(self)
        self.work_queue = work_queue
        # self.daemon = True

    def run(self):
        while True:
            target, args = self.work_queue.get()
            target(*args)
            self.work_queue.task_done()


# 创建一个有4个线程的线程池
thread_pool = ThreadPoolManger(4)


def handle_request(*args):
    conn_socket,addr = args
    print '-------------------'
    print 'connect from %s:%s'%(addr[0],addr[1])
    try:
        data = conn_socket.recv(1024).strip()
    except:
        pass
    else:
        if data:
            print 'Incomming string:', data
            renderTcp.render(data, conn_socket)
        conn_socket.close()
        print "client %s:%s is close!" % (addr[0],addr[1])
        print '-------------------'


while True:
    conn_socket, addr = server.accept()
    thread_pool.add_job(handle_request, *(conn_socket, addr))


