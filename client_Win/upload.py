#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os
import shutil
import platform
import sys
import cv2
import pymysql
from PyQt4 import QtCore, QtGui
import createThumbnail
from httpUrl import CallBack


class UploadFile:
    def __init__(self):
        self.sep = os.sep
        self.plat = platform.system()
        self.inPathFile = ''
        self.fileOld = ''
        self.app = QtGui.QApplication(sys.argv)
        self.mainWindow = QtGui.QMainWindow()
        self.select_file()

    def select_file(self):
        (fileOld, ext) = QtGui.QFileDialog.getOpenFileNameAndFilter(self.mainWindow,
                                                                    QtCore.QString('update a Dailies'),
                                                                    self.inPathFile,
                                                                    '*.* \n*.mov \n*.mp4 \n*.avi \n*.jpg *.jpeg \n%.png \n*.tiff \n*.tga *.dpx \n*.*',
                                                                    options=QtGui.QFileDialog.ReadOnly)
        self.fileOld = fileOld.__str__()

    def upload_dailies(self, server_name, file_path, file_name, command_id):
        if self.fileOld:
            print self.fileOld
            fileType = str(self.fileOld.split(".")[-1])
            fileNow = file_name + "." + fileType

            # 重构filePath: /FUY/stuff/dmt
            filePath = ''
            if fileType == "mov" or fileType == "avi" or fileType == "mp4":
                filePath = os.path.join(file_path, 'mov')
            elif fileType == "jpg" or fileType == "jpeg" or fileType == "png" or fileType == "tiff" or fileType == "tga":
                filePath = os.path.join(file_path, 'img')

            file_copy_path = server_name + filePath + self.sep + file_name  # /Volumes/All/FUY/stuff/dmt/mov/filename
            file_abspath = ''
            try:
                if not os.path.exists(file_copy_path):
                    os.makedirs(file_copy_path)
                file_abspath = file_copy_path + self.sep + fileNow
                shutil.copy(self.fileOld, file_abspath)
            except Exception as e:
                print(e)
            if os.path.exists(file_abspath):
                if fileType == "mov" or fileType == "avi" or fileType == "mp4":
                    createThumbnail.run(fileNow, file_copy_path)
                    CallBack().dai_callback(command_id, filePath + "/" + file_name, fileNow, "")
                    QtGui.QMessageBox.information(None, 'INFORMATION', u'提交成功！', QtCore.QString('OK'))
                elif fileType == "jpg" or fileType == "jpeg" or fileType == "png" or fileType == "tiff" or fileType == "tga":
                    img = cv2.imread(file_abspath)
                    thumbnail_img = file_copy_path + self.sep + '.' + fileNow
                    cv2.imwrite(thumbnail_img, img, [int(cv2.IMWRITE_JPEG_QUALITY), 1])
                    CallBack().dai_callback(command_id, filePath + "/" + file_name, fileNow, "")
                    QtGui.QMessageBox.information(None, 'INFORMATION', u'提交成功！', QtCore.QString('OK'))
                return filePath + "/" + file_name  # /FUY/001/001/stuff/cmp/mov/filename
            else:
                QtGui.QMessageBox.information(None, 'INFORMATION', u'提交失败，请检查上传文件！', QtCore.QString('OK'))
                return filePath
        else:
            return file_path
        sys.exit(app.exec_())

    def upload_reference(self, server_name, file_path, file_name, sql_data):
        if self.fileOld:
            fileType = self.fileOld.split(".")[-1]
            file_copy_path = server_name + file_path + self.sep + file_name + "." + fileType
            shutil.copy(self.fileOld, file_copy_path)
            print file_copy_path
            fileNow = file_name + "." + fileType
            if os.path.exists(file_copy_path):
                if fileType == "mov" or fileType == "avi" or fileType == "mp4":
                    createThumbnail.run(fileNow, (server_name + file_path))
                    file_type = 1
                    thumbnail = '.' + file_name + ".jpg"  # 缩略图路径
                    print thumbnail
                    self.insert_data(sql_data, file_type, thumbnail, fileType)
                    QtGui.QMessageBox.information(None, 'INFORMATION', u'提交成功！', QtCore.QString('OK'))
                elif fileType == "jpg" or fileType == "jpeg" or fileType == "png" or fileType == "tiff" or fileType == "tga":
                    img = cv2.imread(file_copy_path)
                    thumbnail_img = server_name + file_path + self.sep + '.' + fileNow
                    cv2.imwrite(thumbnail_img, img, [int(cv2.IMWRITE_JPEG_QUALITY), 40])
                    file_type = 2
                    thumbnail = '.' + fileNow
                    print thumbnail
                    self.insert_data(sql_data, file_type, thumbnail, fileType)
                    QtGui.QMessageBox.information(None, 'INFORMATION', u'提交成功！', QtCore.QString('OK'))
                return
            else:
                QtGui.QMessageBox.information(None, 'INFORMATION', u'提交失败，请检查上传文件！', QtCore.QString('OK'))
                return
        else:
            return
        sys.exit(app.exec_())

    def insert_data(sql_data, file_type, thumbnail, fileType):
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

        ip = '192.168.100.49'
        user_name = 'root'
        passwd = 'king9188YJQ@'
        db_name = 'new_tron'
        table_name = 'oa_references'

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


if __name__ == '__main__':
    UploadFile().upload_dailies('','','','')