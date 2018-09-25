#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import os, shutil, platform
import createThumbnail
import httpUrl
import cv2
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys


def SelectDailies(serverName, filePath, fileName, command_id, UpTask):
    sep = os.sep
    plat = platform.system()
    if plat == 'Linux' or plat == 'Darwin':
        inPathFile = os.environ['HOME']
    elif plat == 'Windows':
        inPathFile = "D:/"

    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    (fileOld, ext) = QFileDialog.getOpenFileNameAndFilter(mainWindow, QString('update a Dailies'), inPathFile,
                                                          '*.* \n*.mov \n*.mp4 \n*.avi \n*.jpg *.jpeg \n%.png \n*.tiff \n*.tga *.dpx \n*.*',
                                                          options=QFileDialog.ReadOnly)
    if fileOld:
        fileType = str(fileOld.split(".")[-1])
        fileNow = fileName + "." + fileType

        # 重构filePath: /FUY/stuff/dmt
        if fileType == "mov" or fileType == "avi" or fileType == "mp4":
            filePath = os.path.join(filePath, 'mov')
        elif fileType == "jpg" or fileType == "jpeg" or fileType == "png" or fileType == "tiff" or fileType == "tga":
            filePath = os.path.join(filePath, 'img')

        file_copy_path = serverName + filePath + sep + fileName  # /Volumes/UPLOADS/FUY/stuff/dmt/mov/filename
        if not os.path.exists(file_copy_path):
            os.makedirs(file_copy_path)
        file_abspath = file_copy_path + sep + fileNow
        shutil.copy(fileOld, file_abspath)
        if os.path.exists(file_abspath):
            if fileType == "mov" or fileType == "avi" or fileType == "mp4":
                createThumbnail.run(fileNow, file_copy_path)
                httpUrl.toHttpask(command_id, filePath+"/"+fileName, fileNow, UpTask, "")
                QMessageBox.information(None, 'INFORMATION', u'提交成功！', QString('OK'))
            elif fileType == "jpg" or fileType == "jpeg" or fileType == "png" or fileType == "tiff" or fileType == "tga":
                img = cv2.imread(file_abspath)
                thumbnail_img = file_copy_path + sep + '.' + fileNow
                cv2.imwrite(thumbnail_img, img, [int(cv2.IMWRITE_JPEG_QUALITY), 1])
                httpUrl.toHttpask(command_id, filePath+"/"+fileName, fileNow, UpTask, "")
                QMessageBox.information(None, 'INFORMATION', u'提交成功！', QString('OK'))
            return filePath+"/"+fileName
        else:
            QMessageBox.information(None, 'INFORMATION', u'提交失败，请检查上传文件！', QString('OK'))
            return filePath
    else:
        return filePath
    sys.exit(app.exec_())
