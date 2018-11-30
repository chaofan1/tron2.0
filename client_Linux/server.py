# !/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import shutil
import platform
import socket
from multiprocessing import Process
import createThumbnail
from render import Render, Select
from httpUrl import CallBack
from upload import UploadFile
import config
from aliyun_client import AliyunDownload

def myServer():
	if platform.system() != 'Linux':
		print '这是Linux平台，请使用相应脚本!'
		exit()
	localIP = socket.gethostbyname(socket.gethostname())
	HOST = localIP
	PORT = 29400
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((HOST, PORT))
	print "waiting for connection ......"
	s.listen(5)
	while 1:
		conn, addr = s.accept()
		print "connected form ....", addr
		# 实现并发的三种方式：多进程、多线程、协程
		# 多进程的报错：Mac 10.13 objc[72931]: +[__NSPlaceholderDate initialize] may have been in progress in another thread when fork() was called.
		# QtCore与多进程无法同时使用，会导致程序意外退出；
		# windows的socket无法用多进程，因为无法被序列化；
		# 多线程与协程：虽然可以实现socket的并发，但QT库的UI界面只能在主线程运行，无法并发，想要并发只能用内部的QThread；
		# 所以Mac与windows无法实现socket的并发
		p = Process(target=handle, args=(conn,))
		p.start()
		conn.close()


def handle(conn):
	while True:
		data = conn.recv(1024)
		if not data:
			break
		print('recv data:', data)
		data_split = data.strip().split("|")
		sep = os.sep
		server_all = config.All
		server_post = config.Post
		server_ref = config.Reference
		server_outcompany = config.OutCompany

		if data_split[-1] == "open_dai":
			file_path = data_split
			os.popen('nautilus %s' % (server_all + file_path)).close()

		elif data_split[-1] == "open_ref":
			file_path = data_split
			os.popen('nautilus %s' % (server_ref + file_path)).close()

		elif data_split[-1] == "open_post":
			file_path = data_split
			os.popen('nautilus %s' % (server_post + file_path)).close()

		elif data_split[-1] == "YunFolder":
			file_path ,Uptask = data_split
			os.chmod(server_outcompany + file_path, 0777)
			os.popen('open %s' % (server_outcompany + file_path)).close()

		elif data_split[-1] == "Ready_render1" or data_split[-1] == "Local_render1" or data_split[-1] == "Cloud_render1":
			file_path, Uptask = data_split
			inPathFile = server_post + sep + file_path[0:14]
			file_name = Select().select_one(inPathFile)
			if os.path.exists(file_name):
				Render(file_name, file_path).submit(Uptask)
			# CallBack().render_callback(command_id)

		elif data_split[-1] == "Ready_render2" or data_split[-1] == "Local_render2" or data_split[-1] == "Cloud_render2":
			file_path, Uptask = data_split
			inPathFile = server_post + sep + file_path[0:14]
			file_name = Select().select_dir(inPathFile)
			if os.path.exists(file_name):
				Render(file_name, file_path).submit(Uptask)
			# CallBack().render_callback(command_id)

		elif data_split[-1] == "Dailies1":   # /FUY/001/001/stuff/cmp|file_name|command_id|Dailies1
			file_path, file_name, command_id, UpTask = data_split
			UploadFile().upload_dailies(server_all, file_path, file_name, command_id)

		elif data_split[-1] == "download":  # huanyu_Fuy_1|download
			dirname, UpTask = data_split
			AliyunDownload(dirname).downLoad()

		elif data_split[-1] == "Dailies2":
			file_path, file_name, command_id, UpTask = data_split
			fileNow = file_name + ".mov"
			# 重构file_path: /FUY/stuff/dmt
			file_path = file_path + '/mov'
			outputPath = os.path.join(os.environ['HOME'], '/%s' % file_name)
			fileD = server_all + "/" + file_path + "/" + file_name
			fileAll = fileD + "/" + fileNow
			if os.path.isdir(outputPath):
				shutil.rmtree(outputPath)
			os.popen("python //192.168.100.99/Public/tronPipelineScript/IlluminaConverter_v002/IlluminaConverter_v002.py %s" % fileNow).read()
			# os.popen("python /Volumes/library/tron/IlluminaConverter_v002/IlluminaConverter_v002.py %s" % fileNow).read()
			print outputPath
			if os.path.isdir(outputPath):
				shutil.copytree(outputPath, fileD)
				if os.path.exists(fileAll):
					createThumbnail.run(fileNow, fileD)
					CallBack().dai_callback(command_id, file_path + "/" + file_name, fileNow, UpTask, "")

		elif data_split[-1] =="Reference":
			file_path, file_name, sql_data, UpTask = data_split
			UploadFile().upload_reference(server_ref, file_path, file_name, sql_data)

		elif data_split[-1] == 'ShotTask':   # 提交发布弹框
			# "HAC" "01" "001" "rig" "liangcy" "fileName" "ShotTask"
			projectName,seqName,shotName,type_,userName,fileName,UpTask = data_split
			file_path = projectName + sep + seqName + sep + shotName + sep + 'Stuff' + \
						sep + type_ + sep + 'publish' + sep + fileName
			if type_ == "lgt" or type_ == "cmp":
				os.popen('nautilus %s' % (server_post + file_path)).close()
			else:
				os.popen('nautilus %s' % (server_all + file_path)).close()

	conn.close()


if __name__ == '__main__':
	myServer()



