# !/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import time
import platform
import socket
import config
from clipLine import start_clip
from clipLine2 import Pack, insert
from clipLine import to_php
from upload import UploadFile
from httpUrl import CallBack
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def myServer():
    # if platform.system() != 'Darwin':
    #     print '这是Mac平台，请使用相应脚本!'
    #     exit()
    try:
        HOST = socket.gethostbyname(socket.gethostname())
    except:
        print '无法获取本机IP，请联系IT'
        exit()
    PORT = config.port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    print 'localIP:', HOST,":",PORT
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
        sep = '/'
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
                if os.path.exists(server_all+file_path):
                    os.popen('open %s' % (server_all + file_path)).close()
                elif os.path.exists(server_dai+file_path):
                    os.popen('open %s' % (server_dai + file_path)).close()

        elif data_split[-1] == "Folder":
            try:
                file_path, Uptask = data_split
            except:
                print '参数错误:', data_split
            else:
                if os.path.exists(server_all+file_path):
                    os.popen('open %s' % (server_all + file_path)).close()
                elif os.path.exists(server_dai+file_path):
                    os.popen('open %s' % (server_dai + file_path)).close()
                elif os.path.exists(server_post + file_path):
                    os.popen('open %s' % (server_post + file_path)).close()
                elif os.path.exists(server_ref + file_path):
                    os.popen('open %s' % (server_ref + file_path)).close()
        # elif data_split[-1] == "open_ref":
        # 	file_path, Uptask = data_split
        # 	os.popen('open %s' % (server_ref + file_path)).close()
        #
        # elif data_split[-1] == "open_post":
        # 	file_path, Uptask = data_split
        # 	os.popen('open %s' % (server_post + file_path)).close()

        elif data_split[-1] == "YunFolder":
            try:
                file_path, create_time, Uptask = data_split
            except:
                print '参数错误:', data_split
            else:
                projectName = file_path.split('_')[1]
                print create_time
                create_time = time.strftime("%Y%m%d", time.localtime(eval(create_time)))
                path = server_outcompany % (projectName, create_time) + file_path
                print path
                try:
                    if os.path.exists(path):
                        os.popen('open %s' % path).close()
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
            finally:
                conn.send('dailies')

        elif data_split[-1] == "lgt_dai":
            try:
                file_path, file_name, command_id, rate, frame, UpTask = data_split
            except:
                print '参数错误:', data_split
            else:
                UploadFile().upload_dailies(server_all, file_path, file_name, command_id, rate, frame, UpTask)
            finally:
                conn.send('lgt_dai')

        elif data_split[-1] == "download":  # huanyu_Fuy_1|download
            print 'Do not choose local disk'
            downloadPath = UploadFile().select_dir('')
            if downloadPath == '':
                downloadPath = 'nothing selected'
            elif downloadPath.startswith('/Volumes/All/'):
                downloadPath = downloadPath.split('/Volumes')[1].replace('All', 'Tron')
            elif downloadPath.startswith('/Volumes/Tron/'):
                downloadPath = downloadPath.split('/Volumes/Tron')[1]
            else:
                downloadPath = downloadPath.split('/Volumes')[1]
            print 'downloadPath:', downloadPath
            conn.send(downloadPath)

        elif data_split[-1] =="Reference":
            try:
                file_path, file_name, sql_data, UpTask = data_split
            except:
                print '参数错误:', data_split
            else:
                UploadFile().upload_reference(server_ref, file_path, file_name, sql_data)
            finally:
                conn.send('ref')

        elif data_split[-1] == 'clip1':  # 转码
            try:
                xml_path, path, project_id, field_id, xml_id, command_id, UpTask = data_split
            except:
                print '参数错误:', data_split
            else:
                xml_path = server_all + sep + xml_path
                video_path = server_all + sep + path
                start_clip(xml_path, video_path, project_id, field_id, xml_id, UpTask)
                # to_php(1, 0, project_id, field_id, xml_id, UpTask)
                conn.send(path)
                print('clip1 end')
                CallBack().common_callback(command_id)

        elif data_split[-1] == 'add_xml':
            try:
                xml_path, path, project_id, field_id, xml_id, command_id, UpTask = data_split
            except:
                print '参数错误:', data_split
            else:
                xml_path = server_all + sep + xml_path
                video_path = server_all + sep + path
                start_clip(xml_path, video_path, project_id, field_id, xml_id, UpTask)
                conn.send(path)
                # to_php(1, 0, project_id, field_id, xml_id, UpTask)
                CallBack().common_callback(command_id)
                print('add_xml end')

        elif data_split[-1] == 'clip2':   # 回插
            try:
                video_path, img_path, frame, command_id, UpTask = data_split
            except:
                print '参数错误:', data_split
            else:
                video_path = server_all + sep + video_path
                img_path = server_all + sep + img_path
                insert(video_path, img_path, frame)
                CallBack().common_callback(command_id)
                print('clip2 end')
            finally:
                conn.send('path')

        elif data_split[-1] == 'clip3':   # 打包
            try:
                pro_scene, command_id, UpTask = data_split
            except:
                print '参数错误:', data_split
            else:
                pro_path = server_all+pro_scene
                pack_path = server_post + pro_scene + '/Clip_Pack'
                Pack().pack(pro_path, pack_path)
                os.popen('open %s' % pack_path).close()
                CallBack().common_callback(command_id)
                print('clip3 end')

        elif data_split[-1] == 'ShotTask' or data_split[-1] == 'AssetTask':  # 提交发布弹框
            # "HAC" "01" "001" "rig" "liangcy" "fileName" "ShotTask"
            if data_split[-1] == 'ShotTask':
                try:
                    projectName, seqName, shotName, type_, userName, fileName, UpTask = data_split
                    file_path = projectName + sep + seqName + sep + shotName + sep + 'Stuff' + sep + type_ + sep + 'publish' + sep + fileName
                except:
                    print '参数错误:', data_split
                else:
                    if type_ == "lgt" or type_ == "cmp":
                        os.popen('open %s' % (server_post + sep + file_path)).close()
                    else:
                        os.popen('open %s' % (server_all + sep + file_path)).close()
            else:
                try:
                    projectName, type_, userName, fileName, UpTask = data_split
                    file_path = projectName + sep + 'Stuff' + sep + type_ + sep + 'publish' + sep + fileName
                except:
                    print '参数错误:', data_split
                else:
                    if type_ == "lgt" or type_ == "cmp":
                        os.popen('open %s' % (server_post + sep + file_path)).close()
                    else:
                        os.popen('open %s' % (server_all + sep + file_path)).close()

    conn.close()


if __name__ == '__main__':
    myServer()
