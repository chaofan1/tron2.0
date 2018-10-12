#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
# Filename: saveFileWindows.py

import os,shutil,platform
import createThumbnail
import sys
import httpUrl
import cv2
from PyQt4 import QtCore, QtGui
import pymysql


def SelectReference(serverName, filePath, fileName, sql_data):
    sep = os.sep
    if platform.system() == 'Linux' or platform.system() == 'Darwin':
        inPathFile = os.environ['HOME']
    else:
        inPathFile = "D:/"
    app = QtGui.QApplication(sys.argv)
    mainWindow = QtGui.QMainWindow()
    (seqname, ext) = QtGui.QFileDialog.getOpenFileNameAndFilter(mainWindow,
                    QtCore.QString('update a reference'), inPathFile,
                    '*.* \n*.mov \n*.mp4 \n*.avi \n*.jpg *.jpeg \n%.png \n*.tiff \n*.tga \n*.dpx \n.mp3 \n.wav \n*.*',
                    options=QtGui.QFileDialog.ReadOnly)
    fileOld = (seqname.__str__())

    if fileOld:
        fileType = fileOld.split(".")[-1]
        file_copy_path = serverName + filePath + sep + fileName + "." + fileType
        shutil.copy(fileOld, file_copy_path)
        print file_copy_path
        fileNow = fileName + "." + fileType
        if os.path.exists(file_copy_path):
            if fileType == "mov" or fileType == "avi" or fileType == "mp4":
                createThumbnail.run(fileNow, (serverName+filePath))
                # httpUrl.toHttpask(fileID, filePath, fileNow, UpTask, "")
                file_type = 1
                thumbnail = '.' + fileName + ".jpg"  # 缩略图路径
                print thumbnail
                insert_data(sql_data, file_type, thumbnail, fileType)
                QtGui.QMessageBox.information(None, 'INFORMATION', u'提交成功！', QtCore.QString('OK'))
            elif fileType == "jpg" or fileType == "jpeg" or fileType == "png" or fileType == "tiff" or fileType == "tga":
                img = cv2.imread(file_copy_path)
                thumbnail_img = serverName + filePath + sep + '.' + fileNow
                cv2.imwrite(thumbnail_img, img, [int(cv2.IMWRITE_JPEG_QUALITY), 40])
                # httpUrl.toHttpask(fileID, filePath, fileNow, UpTask, "")
                file_type = 2
                thumbnail = '.' + fileNow
                print thumbnail
                insert_data(sql_data, file_type, thumbnail, fileType)
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

    ip = '192.168.1.117'
    user_name = 'root'
    passwd = '123456'
    db_name = 'new_tron'
    table_name = 'oa_references'

    sql_data = eval(sql_data)
    file_name = sql_data.get('file_name')+'.'+fileType
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
        cursor.execute(insert_sql, (file_name,resource_type,project_id,field_id,resource_id,
                                    tache_info,path,directory,user_id,create_year,create_time,
                                    thumbnail,submit_status, file_type))
        conn.commit()
        cursor.close()
        conn.close()


if __name__ == '__main__':
    sql_data = '{"file_name":"1538217282","resource_type":"2","project_id":1,"field_id":33,' \
               '"resource_id":176,"tache_info":"21,16,18,14,26",' \
               '"path":"\/FUY\/shots","directory":"shots","user_id":1,"create_year":"2018",' \
               '"create_time":1538217282}'
    insert_data(sql_data)

