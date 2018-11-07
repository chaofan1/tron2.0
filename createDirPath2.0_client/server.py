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
from render import Render
from clipLine import start_clip
from clipLine2 import Pack,insert
from distribute_download import Download
from clipLine import to_php
from httpUrl import CallBack
from upload import UploadFile


def handle(conn, localIP):
	while True:
		data = conn.recv(1024)
		if not data:
			break
		print('recv data:', data)
		server_name = ''
		outputPath = ''
		data_split = data.strip().split("|")
		sep = os.sep

		if len(data_split) is 1:
			file_path = data.strip()
			if platform.system() == 'Windows':
				server_name = "X:"
				file_path = file_path.replace("/", "\\")
				os.popen('explorer.exe %s' % (server_name + file_path)).close()
				print (server_name + file_path)
			elif platform.system() == 'Linux':
				server_name = "/All"
				os.popen('nautilus %s' % (server_name + file_path)).close()
			elif platform.system() == 'Darwin':
				server_name = "/Volumes/All"
				os.popen('open %s' % (server_name + file_path)).close()

		elif len(data_split) is 2:
			file_path, Uptask = data_split
			if platform.system() == 'Windows':
				if Uptask == 'lgt' or Uptask == 'cmp':
					server_name = "J:"
					file_path = file_path.replace("/", "\\")
					os.popen('explorer.exe %s' % (server_name + file_path)).close()
				else:
					server_name = "X:"
					file_path = file_path.replace("/", "\\")
					os.popen('explorer.exe %s' % (server_name + file_path)).close()
			elif platform.system() == 'Linux':
				if Uptask == 'lgt' or Uptask == 'cmp':
					server_name = "/Post"
					os.popen('nautilus %s' % (server_name + file_path)).close()
				else:
					server_name = "/All"
					os.popen('nautilus %s' % (server_name + file_path)).close()
			elif platform.system() == 'Darwin':
				if Uptask == 'lgt' or Uptask == 'cmp':
					server_name = "/Volumes/Post"
					os.popen('open %s' % (server_name + file_path)).close()
				else:
					server_name = "/Volumes/All"
					os.popen('open %s' % (server_name + file_path)).close()

		elif data.endswith("Render1"):
			file_path, Uptask, command_id = data_split
			if platform.system() == 'Linux':
				server_name = "/Post"
				inPathFile = server_name + sep + file_path[0:14]
				file_name = Render().render_one(inPathFile)
				if os.path.exists(file_name):
					Render().dataTree(file_name, file_path)
			CallBack().render_callback(command_id)

		elif data.endswith("Render2"):
			file_path, Uptask, command_id = data_split
			if platform.system() == 'Linux':
				server_name = "/Post"
				inPathFile = server_name + sep + file_path[0:14]
				file_name = Render().render_all(inPathFile)
				if os.path.exists(file_name):
					Render().dataTree(file_name, file_path)
			CallBack().render_callback(command_id)

		elif data.endswith("Dailies1"):   # /FUY/001/001/stuff/cmp|file_name|command_id|Dailies1
			file_path, file_name, command_id, UpTask = data_split
			if platform.system() == 'Windows':
				server_name = "X:"
				UploadFile().upload_dailies(server_name, file_path, file_name, command_id)
			elif platform.system() == 'Linux':
				server_name = "/All"
				UploadFile().upload_dailies(server_name, file_path, file_name, command_id)
			elif platform.system() == 'Darwin':
				server_name = "/Volumes/All"
				UploadFile().upload_dailies(server_name, file_path, file_name, command_id)

		elif data.endswith("Dailies2"):
			file_path, file_name, command_id, UpTask = data_split
			fileNow = file_name + ".mov"
			# 重构file_path: /FUY/stuff/dmt
			file_path = file_path + '/mov'
			if platform.system() == 'Windows':
				outputPath = "D:/TronDailies/%s" % file_name
				server_name = "X:"
			elif platform.system() == 'Linux':
				outputPath = os.path.join(os.environ['HOME'], '/%s' % file_name)
				server_name = "/All"
			elif platform.system() == 'Darwin':
				break
			fileD = server_name + "/" + file_path + "/" + file_name
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
			# conn.send(file_path + "/" + file_name)

		elif data.endswith("Reference"):
			file_path, file_name, sql_data, UpTask = data_split
			if platform.system() == 'Windows':
				server_name = "L:/References"
				UploadFile().upload_reference(server_name, file_path, file_name, sql_data)
			elif platform.system() == 'Linux':
				server_name = "/library/References"
				UploadFile().upload_reference(server_name, file_path, file_name, sql_data)
			elif platform.system() == 'Darwin':
				server_name = "/Volumes/library/References"
				UploadFile().upload_reference(server_name, file_path, file_name, sql_data)

		elif data.endswith('clip1'):  # 转码
			xml_path, path, project_id, field_id, xml_id, command_id, UpTask = data_split
			xml_path = '/Volumes/All/' + xml_path
			video_path = '/Volumes/All/' + path
			start_clip(xml_path, video_path, project_id, field_id, xml_id, UpTask)
			to_php(1, 0, project_id, field_id, xml_id, UpTask)
			# httpUrl.render_callback(command_id)
			#os.remove(xml_path)
			conn.send(path)
			print('clip1 end')

		elif data.endswith('add_xml'):
			xml_path, path, project_id, field_id, xml_id, command_id, UpTask = data_split
			xml_path = '/Volumes/All/' + xml_path
			video_path = '/Volumes/All/' + path
			start_clip(xml_path, video_path, project_id, field_id, xml_id, UpTask)
			conn.send(path)
			# httpUrl.render_callback(command_id)
			print('add_xml end')

		elif data.endswith('clip2'):   # 回插
			video_path, img_path, frame, data_id, command_id, UpTask = data_split
			insert(video_path, img_path, frame, data_id)
			# httpUrl.render_callback(command_id)
			print('clip2 end')

		elif data.endswith('clip3'):   # 打包
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

		elif data.endswith('download'):   # 分发外包下载
			save_path = Render().render_all('')
			load_path, UpTask = data_split
			Download(save_path, load_path).putThread()
			# httpUrl.render_callback(command_id)

		# 转码 'clip1' 'IP|xml_path|path|项目id|场id|command_id|clip1' 7
		# 回插 'clip2' 'IP|video_path|img_path|frame|width|height|id|command_id|clip2' 8
		# 打包 'clip3'  'IP|FUY/001|xml_path|command_id|clip3'  5

	conn.close()


def myServer():
	localIP = socket.gethostbyname(socket.gethostname())
	# localIP = '127.0.0.1'
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
		if platform.system() == 'Linux':
			p = Process(target=handle, args=(conn, localIP))
			p.start()
			conn.close()
		else:
			handle(conn, localIP)


if __name__ == '__main__':
	myServer()



