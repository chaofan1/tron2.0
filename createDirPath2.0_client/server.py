#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-

#转码 'clip1' 'IP|xml_path|path|项目id|场id|xml_id|command_id|clip1' 7
#回插 'clip2' 'IP|video_path|img_path|frame|width|height|id|command_id|clip2' 8
#打包 'clip3'  'IP|FUY/001|xml_path|command_id|clip3'  5

import os, shutil, socket, httpUrl, platform
from multiprocessing import Process
import saveReferenceWindows
import saveDailiesWindows
import saveDailiesMac
import saveReferenceMac
import createThumbnail
import render_one
import render_all
import render_remind
import clientToRender
from clipLine import start_clip
from clipLine2 import BackInsert,Pack


def handle(conn,localIP):
	while 1:
		data = conn.recv(1024)
		if not data:
			break
		print('recv data:',data)
		serverName = ''
		outputPath = ''

		data_split = data.strip().split("|")
		if len(data_split) is 1:
			filePath = data.strip()
			if platform.system() == 'Windows':
				serverName = "X:"
				filePath = filePath.replace("/", "\\")
				os.popen('explorer.exe %s' % (serverName + filePath)).close()
				print (serverName + filePath)
			elif platform.system() == 'Linux':
				serverName = "/All"
				os.popen('nautilus %s' % (serverName + filePath)).close()
			elif platform.system() == 'Darwin':
				serverName = "/Volumes/All"
				os.popen('open %s' % (serverName + filePath)).close()
		elif len(data_split) is 2:
			filePath, Uptask = data_split
			if platform.system() == 'Windows':
				if Uptask == 'lgt' or Uptask == 'cmp':
					serverName = "J:"
					filePath = filePath.replace("/", "\\")
					os.popen('explorer.exe %s' % (serverName + filePath)).close()
				# elif Uptask == 'References':
				# 	serverName = "L:\References"
				# 	filePath = filePath.replace("/", "\\")
				# 	os.popen('explorer.exe %s' % (serverName + filePath)).read()
				else:
					serverName = "X:"
					filePath = filePath.replace("/", "\\")
					os.popen('explorer.exe %s' % (serverName + filePath)).close()
			elif platform.system() == 'Linux':
				if Uptask == 'lgt' or Uptask == 'cmp':
					serverName = "/Post"
					os.popen('nautilus %s' % (serverName + filePath)).close()
				# elif Uptask == 'Referencer':
				# 	serverName = "/Library/References"
				# 	os.popen('nautilus %s' % (serverName + filePath)).close()
				else:
					serverName = "/All"
					os.popen('nautilus %s' % (serverName + filePath)).close()
			elif platform.system() == 'Darwin':
				if Uptask == 'lgt' or Uptask == 'cmp':
					serverName = "/Volumes/Post"
					os.popen('open %s' % (serverName + filePath)).close()
				# elif Uptask == 'References':
				# 	serverName = "/Volumes/Library/References"
				# 	os.popen('open %s' % (serverName + filePath)).close()
				else:
					serverName = "/Volumes/All"
					os.popen('open %s' % (serverName + filePath)).close()

		elif data.endswith("Render1"):
			filePath, Uptask, command_id = data_split
			if platform.system() == 'Windows':
				inPathFile = os.path.join('J:', filePath[0:14])
				filename = render_one.render_one(inPathFile).replace("/",'\\')
				if os.path.exists(filename):
					dataTree(filename, filePath, localIP)
			elif platform.system() == 'Linux':
				serverName = "/Post"
				inPathFile = os.path.join(serverName, filePath[0:14])
				filename = render_one.render_one(inPathFile)
				if os.path.exists(filename):
					# dataTo = localIP + "|" + filename + "|Render"
					# datadd = clientToRender.client(dataTo)
					# render_remind.remind(datadd)
					dataTree(filename, filePath, localIP)
			httpUrl.render_callback(command_id)

		elif data.endswith("Render2"):
			filePath, Uptask, command_id = data_split
			if platform.system() == 'Windows':
				inPathFile = os.path.join('J:', filePath[0:14])
				filename = render_all.render_all(inPathFile).replace("/", '\\')
				if os.path.exists(filename):
					dataTree(filename, filePath, localIP)
			elif platform.system() == 'Linux':
				serverName = "/Post"
				inPathFile = os.path.join(serverName, filePath[0:14])
				filename = render_all.render_all(inPathFile)
				if os.path.exists(filename):
					dataTree(filename, filePath, localIP)
			httpUrl.render_callback(command_id)

		elif data.endswith("Dailies1"):   # FUY/001/001/stuff/cmp|filename|command_id|Dailies1
			filePath, fileName, command_id, UpTask = data_split
			print filePath, fileName, command_id, UpTask
			if platform.system() == 'Windows':
				serverName = "X:"
				fileOld = saveDailiesWindows.SelectDailiesWin(serverName, filePath, fileName, command_id, UpTask)
				conn.send(fileOld)
			elif platform.system() == 'Linux':
				serverName = "/All"
				fileOld = saveDailiesWindows.SelectDailiesWin(serverName, filePath, fileName, command_id, UpTask)
				conn.send(fileOld)
			elif platform.system() == 'Darwin':
				serverName = "/Volumes/All"
				fileOld = saveDailiesMac.SelectDailiesWin(serverName, filePath, fileName, command_id, UpTask)
				conn.send(fileOld)

		elif data.endswith("Dailies2"):
			filePath, fileName, command_id, UpTask = data_split
			print filePath, fileName, command_id, UpTask
			fileNow = fileName + ".mov"
			# 重构filePath: /FUY/stuff/dmt
			filePath = filePath + '/mov'
			if platform.system() == 'Windows':
				outputPath = "D:/TronDailies/%s" % fileName
				serverName = "X:"
			elif platform.system() == 'Linux':
				outputPath = os.path.join(os.environ['HOME'], '/%s' % fileName)
				serverName = "/All"
			elif platform.system() == 'Darwin':
				break
			fileD = serverName + filePath + "/" + fileName
			fileAll = fileD + "/" + fileNow
			if os.path.isdir(outputPath):
				shutil.rmtree(outputPath)
			os.popen("python //192.168.100.99/Public/tronPipelineScript/IlluminaConverter_v002/IlluminaConverter_v002.py %s" % fileNow).read()
			print (outputPath + "/")
			if os.path.isdir(outputPath + "/"):
				shutil.copytree(outputPath, fileD)
				if os.path.exists(fileAll):
					createThumbnail.run(fileNow, fileD)
					httpUrl.toHttpask(command_id, filePath + "/" + fileName, fileNow, UpTask, "")
			conn.send(filePath + "/" + fileName)

		elif data.endswith("Reference"):
			filePath, fileName, command_id, UpTask = data_split
			print filePath, fileName, command_id, UpTask
			if platform.system() == 'Windows':
				serverName = "L:/References"
				fileOld = saveReferenceWindows.SelectReferenceWin(serverName, filePath, fileName, command_id,UpTask)
			elif platform.system() == 'Linux':
				serverName = "/library/References"
				fileOld = saveReferenceWindows.SelectReferenceWin(serverName, filePath, fileName, command_id,UpTask)
			elif platform.system() == 'Darwin':
				serverName = "/Volumes/library/References"
				fileOld = saveReferenceMac.SelectReferenceWin(serverName, filePath, fileName, command_id, UpTask)

		elif data.endswith('clip1'):  # 转码
			xml_path, path, project_id, field_id, xml_id,command_id,UpTask = data_split
			start_clip(xml_path, path, project_id, field_id,xml_id,UpTask)
			# httpUrl.render_callback(command_id)
			print('end')

		elif data.endswith('add_xml'):
			xml_path, path, project_id, field_id, xml_id,command_id,UpTask = data_split
			start_clip(xml_path, path, project_id, field_id,xml_id,UpTask)
			# httpUrl.render_callback(command_id)
			print('end')

		elif data.endswith('clip2'):   # 回插
			video_path,img_path,frame,data_id,command_id,UpTask = data_split
			BackInsert().insert(video_path,img_path,frame,data_id)
			# httpUrl.render_callback(command_id)

		elif data.endswith('clip3'):   # 打包
			pro_scene, xml_path, command_id,UpTask = data_split
			pro_name = pro_scene.strip('/').split('/')[-2]
			user_path = os.environ['HOME']  # /Users/wang
			pack_path = os.path.join(user_path,'Pack')
			if not os.path.exists(pack_path):
				os.mkdir(pack_path)
			out_path = os.path.join(pack_path,pro_name)  # /Users/wang/Pack/FUY
			Pack().pack(pro_scene, xml_path, out_path)
			os.popen('open %s' % out_path).close()
			# httpUrl.render_callback(command_id)


		# 转码 'clip1' 'IP|xml_path|path|项目id|场id|command_id|clip1' 7
		# 回插 'clip2' 'IP|video_path|img_path|frame|width|height|id|command_id|clip2' 8
		# 打包 'clip3'  'IP|FUY/001|xml_path|command_id|clip3'  5

	conn.close()


def dataTree(filename, filePath, localIP):
	file_size = os.path.getsize(filename)
	file_mtime = os.path.getmtime(filename)
	pro_name = filePath.split('/')[1]
	pro_path = os.getcwd()
	csv_path = os.path.join(pro_path,'%s.csv'%pro_name)
	with open(csv_path, 'a+') as f:
		con_write = filePath, file_size, file_mtime
		con_read = set(f.readlines())
		con_write = str(con_write) + '\n'
		dataTo = localIP + "|" + filename + "|Render"
		if con_write not in con_read:
			f.write(con_write)
			datadd = clientToRender.client(dataTo)
			render_remind.remind(datadd)
		else:
			render_remind.ask()
			datadd = clientToRender.client(dataTo)
			render_remind.remind(datadd)


def myServer():
	# localIP = socket.gethostbyname(socket.gethostname())
	localIP = '127.0.0.1'
	HOST = localIP
	PORT = 29400
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	s.bind((HOST, PORT))
	print "waiting for connection ......"
	s.listen(10)
	while 1:
		conn, addr = s.accept()
		print "connected form ....", addr
		if platform.system() != 'Windows':
			p = Process(target=handle, args=(conn, localIP))
			p.start()
			conn.close()
		else:
			handle(conn, localIP)


if __name__ == '__main__':
	myServer()



