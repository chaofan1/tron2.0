#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import shutil
import platform
import subprocess
import cv2
import pymysql
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from createThumbnail import CreateThumbnail
from httpUrl import CallBack
import config
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class UploadFile:
    def __init__(self):
        self.sep = os.sep
        self.plat = platform.system()
        self.app = QApplication(sys.argv)
        self.mainWindow = QMainWindow()
        self.inPathFile = ''
        self.fileOld = ''

    def select_one(self, inPathFile):
        self.fileOld = QFileDialog.getOpenFileName(self.mainWindow, 'open file', inPathFile).toUtf8()

    def select_dir(self, inPathFile):
        file_path = QFileDialog.getExistingDirectory(self.mainWindow, 'select your dir', inPathFile).toUtf8()
        return str(file_path)
        sys.exit(self.app.exec_())

    def download_success(self):
        QMessageBox.information(None, 'INFORMATION', u'下载成功！')
        return
        sys.exit(self.app.exec_())

    def download_fail(self):
        QMessageBox.information(None, 'INFORMATION', u'下载失败！')
        return
        sys.exit(self.app.exec_())

    def upload_dailies(self, server_name, file_path, file_name, command_id, rate, frame, task):
        self.select_one('')
        if self.fileOld:
            fileType = str(self.fileOld.split(".")[-1]).lower()
            fileNow = file_name + "." + fileType
            clip_video_callbackpath = ''
            # 重构filePath: /FUY/Stuff/dmt
            filePath = ''
            if fileType == "mov" or fileType == "avi" or fileType == "mp4":
                filePath = file_path + '/mov'
            elif fileType == "jpg" or fileType == "jpeg" or fileType == "png" or fileType == "tiff" or fileType == "tga":
                filePath = file_path + '/img'
                fileNow = file_name + ".jpg"
                # if task:
                #     clip_video_dirpath = server_name + file_path + '/mov' + self.sep + file_name
                #     if not os.path.exists(clip_video_dirpath):
                #         os.makedirs(clip_video_dirpath)
                #     clip_video_abspath = clip_video_dirpath + self.sep + file_name + '.mov'
                #     clip_video_callbackpath = file_path + '/mov' + self.sep + file_name + self.sep + file_name + '.mov'
                #     ffmpeg = config.ffmpeg
                #     command = '%s -loop 1 -i %s -r %s -loglevel -8 -y -g 2 -keyint_min 2 -vframes %s %s' % (ffmpeg, self.fileOld, rate, frame, clip_video_abspath)
                #     video_su = subprocess.Popen(command, shell=True)
                #     video_su.wait()
            file_copy_path = server_name + filePath + self.sep + file_name  # /Volumes/All/FUY/Stuff/dmt/mov/filename
            file_abspath = file_copy_path + self.sep + fileNow
            print file_copy_path
            try:
                if not os.path.exists(file_copy_path):
                    os.mkdir(file_copy_path)
                    print 'mkdir'
                shutil.copy(self.fileOld, file_abspath)
            except Exception as e:
                print(e)
            if task:
                clip_video_dirpath = server_name + file_path + '/mov' + self.sep + file_name
                if not os.path.exists(clip_video_dirpath):
                    os.makedirs(clip_video_dirpath)
                clip_video_abspath = clip_video_dirpath + self.sep + file_name + '.mov'
                clip_video_callbackpath = file_path + '/mov' + self.sep + file_name + self.sep + file_name + '.mov'
                ffmpeg = config.ffmpeg
                command = '%s -loop 1 -i %s -r %s -loglevel -8 -y -g 2 -keyint_min 2 -vframes %s %s' % (ffmpeg, file_abspath, rate, frame, clip_video_abspath)
                video_su = subprocess.Popen(command, shell=True)
                video_su.wait()
            if os.path.exists(file_abspath):
                if fileType == "mov" or fileType == "avi" or fileType == "mp4":
                    CreateThumbnail().run(file_abspath)
                    CallBack().dai_callback(command_id, filePath + "/" + file_name, fileNow, clip_video_callbackpath)
                    QMessageBox.information(None, 'INFORMATION', u'提交成功！')
                elif fileType == "jpg" or fileType == "jpeg" or fileType == "png" or fileType == "tiff" or fileType == "tga":
                    img = cv2.imread(file_abspath)
                    thumbnail_img = file_copy_path + self.sep + '.' + fileNow
                    cv2.imwrite(thumbnail_img, img, [int(cv2.IMWRITE_JPEG_QUALITY), 40])
                    CallBack().dai_callback(command_id, filePath + "/" + file_name, fileNow, clip_video_callbackpath)
                    QMessageBox.information(None, 'INFORMATION', u'提交成功！')
                return  # /FUY/001/001/Stuff/cmp/mov/filename
            else:
                QMessageBox.information(None, 'INFORMATION', u'提交失败，请检查上传文件及权限！')
                return
        else:
            return
        sys.exit(app.exec_())

    def upload_reference(self, server_name, file_path, file_name, sql_data):
        self.select_one('')
        if self.fileOld:
            fileType = str(self.fileOld.split(".")[-1]).lower()
            if fileType == "jpg" or fileType == "jpeg" or fileType == "png" or fileType == "tiff" or fileType == "tga":
                fileType = "jpg"
            file_copy_path = server_name + file_path + self.sep + file_name + "." + fileType
            try:
                shutil.copy(self.fileOld, file_copy_path)
                print file_copy_path
            except Exception as e:
                print e
            fileNow = file_name + "." + fileType
            if os.path.exists(file_copy_path):
                if fileType == "mov" or fileType == "avi" or fileType == "mp4":
                    CreateThumbnail().run(file_copy_path)
                    file_type = 1
                    thumbnail = '.' + file_name + ".jpg"  # 缩略图路径
                    self.insert_data(sql_data, file_type, thumbnail, fileType)
                    QMessageBox.information(None, 'INFORMATION', u'提交成功！')
                elif fileType == "jpg" or fileType == "jpeg" or fileType == "png" or fileType == "tiff" or fileType == "tga":
                    img = cv2.imread(file_copy_path)
                    thumbnail_img = server_name + file_path + self.sep + '.' + fileNow
                    cv2.imwrite(thumbnail_img, img, [int(cv2.IMWRITE_JPEG_QUALITY), 40])
                    file_type = 2
                    thumbnail = '.' + fileNow
                    self.insert_data(sql_data, file_type, thumbnail, fileType)
                    QMessageBox.information(None, 'INFORMATION', u'提交成功！')
                return
            else:
                QMessageBox.information(None, 'INFORMATION', u'提交失败，请检查上传文件！')
                return
        else:
            return
        sys.exit(self.app.exec_())

    def insert_data(self, sql_data, file_type, thumbnail, fileType):
        # {"file_name":"1538217282",     string
        # "resource_type":"2",
        # "project_id":1,
        # "field_id":33,
        # "resource_id":176,
        # "tache_info":"21,16,18,14,26", string
        # "path":"\/FUY\/shots",         string
        # "directory":"shots",           string
        # "user_id":1,
        # "create_year":"2018",
        # "create_time":1538217282}

        ip = config.ip
        user_name = config.user_name
        passwd = config.passwd
        db_name = config.db_name

        sql_data = eval(sql_data)
        file_name = sql_data.get('file_name') + '.' + fileType
        resource_type = int(sql_data.get('resource_type'))
        project_id = int(sql_data.get('project_id'))
        field_id = int(sql_data.get('field_id'))
        resource_id = int(sql_data.get('resource_id'))
        tache_info = sql_data.get('tache_info')
        path = sql_data.get('path')
        directory = sql_data.get('directory')
        user_id = int(sql_data.get('user_id'))
        create_year = int(sql_data.get('create_year'))
        create_time = int(sql_data.get('create_time'))

        submit_status = 2

        try:
            conn = pymysql.connect(ip, user_name, passwd, db_name, charset='utf8', use_unicode=True)
        except:
            print('connect fail')
        else:
            cursor = conn.cursor()
            insert_sql = "insert ignore into oa_references(file_name,resource_type,project_id,field_id,resource_id," \
                         "tache_info,path,directory,user_id,create_year,create_time,thumbnail,submit_status, file_type) " \
                         "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(insert_sql, (file_name, resource_type, project_id, field_id, resource_id,
                                        tache_info, path, directory, user_id, create_year, create_time,
                                        thumbnail, submit_status, file_type))
            conn.commit()
            cursor.close()
            conn.close()
            print 'succes sql'


if __name__ == '__main__':
    UploadFile().upload_reference('','','','')
    # UploadFile().select_one('')
