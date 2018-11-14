# !/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# 转码 'clip1' 'IP|xml_path|path|项目id|场id|xml_id|command_id|clip1'
# 回插 'clip2' 'IP|video_path|img_path|frame|width|height|id|command_id|clip2'
# 打包 'clip3'  'IP|FUY/001|xml_path|command_id|clip3'

import os
import shutil
import platform
import socket
from multiprocessing import Process
import createThumbnail
from render import Render, Select
from clipLine import start_clip
from clipLine2 import Pack, insert
from distribute_download import Download
from clipLine import to_php
from httpUrl import CallBack
from upload import UploadFile


def myServer():
	if platform.system() != 'Darwin':
		print '这是Mac平台，请使用相应脚本！'
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
		handle(conn)


def handle(conn):
	while True:
		data = conn.recv(1024)
		if not data:
			break
		print('recv data:', data)
		data_split = data.strip().split("|")
		sep = os.sep

		if len(data_split) is 1:
			file_path = data.strip()
			server_name = "/Volumes/All"
			os.popen('open %s' % (server_name + file_path)).close()

		elif len(data_split) is 2:
			file_path, Uptask = data_split
			if Uptask == 'lgt' or Uptask == 'cmp':
				server_name = "/Volumes/Post"
				os.popen('open %s' % (server_name + file_path)).close()
			else:
				server_name = "/Volumes/All"
				os.popen('open %s' % (server_name + file_path)).close()

		elif data_split[-1] == "Dailies1":   # /FUY/001/001/stuff/cmp|file_name|command_id|Dailies1
			file_path, file_name, command_id, UpTask = data_split
			server_name = "/Volumes/All"
			UploadFile().upload_dailies(server_name, file_path, file_name, command_id)

		elif data_split[-1] =="Reference":
			file_path, file_name, sql_data, UpTask = data_split
			server_name = "/Volumes/library/References"
			UploadFile().upload_reference(server_name, file_path, file_name, sql_data)

		elif data_split[-1] == 'clip1':  # 转码
			xml_path, path, project_id, field_id, xml_id, command_id, UpTask = data_split
			xml_path = '/Volumes/All/' + xml_path
			video_path = '/Volumes/All/' + path
			start_clip(xml_path, video_path, project_id, field_id, xml_id, UpTask)
			to_php(1, 0, project_id, field_id, xml_id, UpTask)
			conn.send(path)
			print('clip1 end')
			# httpUrl.render_callback(command_id)

		elif data_split[-1] == 'add_xml':
			xml_path, path, project_id, field_id, xml_id, command_id, UpTask = data_split
			xml_path = '/Volumes/All/' + xml_path
			video_path = '/Volumes/All/' + path
			start_clip(xml_path, video_path, project_id, field_id, xml_id, UpTask)
			conn.send(path)
			# httpUrl.render_callback(command_id)
			conn.send(path)
			print('add_xml end')

		elif data_split[-1] == 'clip2':   # 回插
			video_path, img_path, frame, data_id, command_id, UpTask = data_split
			insert(video_path, img_path, frame, data_id)
			# httpUrl.render_callback(command_id)
			print('clip2 end')

		elif data_split[-1] == 'clip3':   # 打包
			pro_scene, xml_path, command_id, UpTask = data_split
			pro_name = pro_scene.strip('/').split('/')[-2]
			user_path = os.environ['HOME']  # /Users/wang
			pack_path = os.path.join(user_path, 'Pack')
			if not os.path.exists(pack_path):
				os.mkdir(pack_path)
			out_path = os.path.join(pack_path, pro_name)  # /Users/wang/Pack/FUY
			pro_scene = '/Volumes/All' + pro_scene
			Pack().pack(pro_scene, xml_path, out_path)
			os.popen('open %s' % out_path).close()
			# httpUrl.render_callback(command_id)
			print('clip3 end')

		elif data_split[-1] == 'download':   # 分发外包下载
			save_path = Select().select_dir('')
			load_path, UpTask = data_split
			Download(save_path, load_path).putThread()
			# httpUrl.render_callback(command_id)

		elif data_split[-1] == 'ShotTask':   # 提交发布弹框
			# "ShotTask" "HAC" "01" "001" "rig" "liangcy" "fileName" "command_id"
			projectName,seqName,shotName,type_,userName,fileName,UpTask = data_split
			file_path = projectName + sep + seqName + sep + shotName + sep + 'Stuff' + \
						sep + type_ + sep + 'publish' + sep + fileName
			if type_ == "lgt" or type_ == "cmp":
				if platform.system() == 'Windows':
					server_name = "J:"
					os.popen('explorer.exe %s' % (server_name + file_path)).close()
					print (server_name + file_path)
				elif platform.system() == 'Linux':
					server_name = "/Post"
					os.popen('nautilus %s' % (server_name + file_path)).close()
				elif platform.system() == 'Darwin':
					server_name = "/Volumes/Post"
					os.popen('open %s' % (server_name + file_path)).close()
			else:
				if platform.system() == 'Windows':
					server_name = "X:"
					os.popen('explorer.exe %s' % (server_name + file_path)).close()
					print (server_name + file_path)
				elif platform.system() == 'Linux':
					server_name = "/All"
					os.popen('nautilus %s' % (server_name + file_path)).close()
				elif platform.system() == 'Darwin':
					server_name = "/Volumes/All"
					os.popen('open %s' % (server_name + file_path)).close()
	conn.close()


if __name__ == '__main__':
	myServer()