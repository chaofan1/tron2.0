# !/usr/bin/env python2.7
# -*- coding: utf-8 -*-

# 转码 'clip1' 'IP|xml_path|path|项目id|场id|xml_id|command_id|clip1'
# 回插 'clip2' 'IP|video_path|img_path|frame|width|height|id|command_id|clip2'
# 打包 'clip3'  'IP|FUY/001|xml_path|command_id|clip3'

import os
import time
import shutil
import platform
import socket
from createThumbnail import CreateThumbnail
from httpUrl import CallBack
from upload import UploadFile
import config
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def myServer():
    if platform.system() != 'Windows':
        print '这是Windows平台，请使用相应脚本！'
        exit()
    try:
        HOST = socket.gethostbyname(socket.gethostname())
    except:
        print '无法获取本机IP，请联系IT'
        exit()
    PORT = config.port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    print 'Local IP:', HOST,":",PORT
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
        server_all = config.All
        server_post = config.Post
        server_ref = config.Reference
        server_dai = config.Dailies
        server_outcompany = config.OutCompany

        if data_split[-1] == "open_dai":
            try:
                file_path, Uptask = data_split
            except:
                print '参数错误:',data_split
            else:
                file_path = file_path.replace("/", "\\")
                if os.path.exists(server_all+file_path):
                    os.popen('explorer.exe %s' % (server_all + file_path)).close()
                elif os.path.exists(server_dai+file_path):
                    os.popen('explorer.exe %s' % (server_dai + file_path)).close()

        elif data_split[-1] == "Folder":
            try:
                file_path, Uptask = data_split
            except:
                print '参数错误:', data_split
            else:
                file_path = file_path.replace("/", "\\")
                if os.path.exists(server_all+file_path):
                    os.popen('explorer.exe %s' % (server_all + file_path)).close()
                elif os.path.exists(server_dai+file_path):
                    os.popen('explorer.exe %s' % (server_dai + file_path)).close()
                elif os.path.exists(server_post+file_path):
                    os.popen('explorer.exe %s' % (server_post + file_path)).close()
                elif os.path.exists(server_ref+file_path):
                    os.popen('explorer.exe %s' % (server_ref + file_path)).close()

        elif data_split[-1] == "YunFolder":
            try:
                file_path, create_time, Uptask = data_split
            except:
                print '参数错误:', data_split
            else:
                file_path = file_path.replace("/", "\\")
                projectName = file_path.split('_')[1]
                create_time = time.strftime("%Y%m%d",time.localtime(eval(create_time)))
                path = server_outcompany %(projectName,create_time)+ file_path
                print path
                try:
                    if os.path.exists(path):
                        os.popen('explorer.exe %s' % path).close()
                    else:
                        print 'the directory not exit'
                except Exception as e:
                    print e

        elif data_split[-1] == "Dailies1":   # /FUY/001/001/stuff/cmp|file_name|command_id|Dailies1
            try:
                file_path, file_name, command_id, UpTask = data_split
            except:
                print '参数错误:', data_split
            else:
                UploadFile().upload_dailies(server_all, file_path, file_name, command_id, '', '', '')
                conn.send('dailies')

        elif data_split[-1] == "lgt_dai":
            try:
                file_path, file_name, command_id, rate, frame, UpTask = data_split
            except:
                print '参数错误:', data_split
            else:
                UploadFile().upload_dailies(server_all, file_path, file_name, command_id, rate, frame, UpTask)
                conn.send('lgt_dai')

        elif data_split[-1] == "download":   # huanyu_Fuy_1|download
            print 'Do not choose local disk'
            downloadPath = UploadFile().select_dir('')
            if downloadPath == '':
                downloadPath = 'nothing selected'
            elif downloadPath.startswith('L'):
                pathList = downloadPath.split('\\')
                pathList[0] = 'Library'
                downloadPath ='/' + '/'.join(pathList)
            elif downloadPath.startswith('X'):
                pathList = downloadPath.split('\\')
                pathList[0] = 'Tron'
                downloadPath = '/' + '/'.join(pathList)
            elif downloadPath.startswith('J'):
                pathList = downloadPath.split('\\')
                pathList[0] = 'Post'
                downloadPath = '/' + '/'.join(pathList)
            elif downloadPath.startswith('G'):
                pathList = downloadPath.split('\\')
                pathList[0] = 'Illuminafx'
                downloadPath = '/' + '/'.join(pathList)
            elif downloadPath.startswith('W'):
                pathList = downloadPath.split('\\')
                pathList[0] = 'Public'
                downloadPath = '/' + '/'.join(pathList)
            elif downloadPath.startswith('Y'):
                pathList = downloadPath.split('\\')
                pathList[0] = 'Dailies'
                downloadPath = '/' + '/'.join(pathList)
            elif downloadPath.startswith('T'):
                pathList = downloadPath.split('\\')
                pathList[0] = ''
                downloadPath = '/' + '/'.join(pathList)
            print 'downloadPath:', downloadPath
            conn.send(downloadPath)

        elif data_split[-1] == "Dailies2":
            try:
                file_path, file_name, command_id, UpTask = data_split
            except:
                print '参数错误:', data_split
            else:
                fileNow = file_name + ".mov"
                # 重构file_path: /FUY/stuff/dmt
                file_path = file_path + '/mov'
                outputPath = "D:/TronDailies/%s" % file_name
                server_name = server_all
                fileD = server_name + "/" + file_path + "/" + file_name
                fileAll = fileD + "/" + fileNow
                if os.path.isdir(outputPath):
                    shutil.rmtree(outputPath)
                os.popen("python //192.168.100.99/Public/tronPipelineScript/IlluminaConverter_v002/IlluminaConverter_v002.py %s" % fileNow).read()
                print outputPath
                if os.path.isdir(outputPath):
                    file_old = outputPath + '/' + fileNow
                    shutil.copy(file_old, fileAll)
                    if os.path.exists(fileAll):
                        CreateThumbnail().run(fileAll)
                        CallBack().dai_callback(command_id, file_path + "/" + file_name, fileNow, fileAll)
            finally:
                conn.send('dailies2')

        elif data_split[-1] =="Reference":
            try:
                file_path, file_name, sql_data, UpTask = data_split
            except:
                print '参数错误:', data_split
            else:
                UploadFile().upload_reference(server_ref, file_path, file_name, sql_data)
                conn.send('ref')

        elif data_split[-1] == 'ShotTask' or data_split[-1] == 'AssetTask':   # 提交发布弹框
            # "HAC" "01" "001" "rig" "liangcy" "fileName" "ShotTask"
            if data_split[-1] == 'ShotTask':
                try:
                    projectName,seqName,shotName,type_,userName,fileName,UpTask = data_split
                except:
                    print '参数错误:', data_split
                else:
                    file_path = projectName + sep + seqName + sep + shotName + sep + 'Stuff' + sep + type_ + sep + 'publish' + sep + fileName
            # fileList = UploadFile().select_files()
            # for file in fileList:
            # 	shutil.copy(file, file_path)
            else:
                try:
                    projectName, type_, userName, fileName, UpTask = data_split
                except:
                    print '参数错误:', data_split
                else:
                    file_path = projectName + sep + 'Stuff' + sep + type_ + sep + 'publish' + sep + fileName
            if type_ == "lgt" or type_ == "cmp":
                os.popen('explorer.exe %s' % (server_post + sep + file_path)).close()
                print (server_post + file_path)
            else:
                os.popen('explorer.exe %s' % (server_all + sep + file_path)).close()
                print (server_all + file_path)

    conn.close()


if __name__ == '__main__':
    myServer()



