#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
# Filename: saveFileWindows.py

import os,shutil,platform
import createThumbnail
import sys
import httpUrl
import cv2
from PyQt4 import QtCore, QtGui



def SelectReference(serverName, filePath, fileName, fileID, UpTask):
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
                httpUrl.toHttpask(fileID, filePath, fileNow, UpTask, "")
            elif fileType == "jpg" or fileType == "jpeg" or fileType == "png" or fileType == "tiff" or fileType == "tga":
                img = cv2.imread(file_copy_path)
                thumbnail_img = serverName + filePath + sep + '.' + fileNow
                cv2.imwrite(thumbnail_img, img, [int(cv2.IMWRITE_JPEG_QUALITY), 40])
                # httpUrl.toHttpask(fileID, filePath, fileNow, UpTask, "")
                QtGui.QMessageBox.information(None, 'INFORMATION', u'提交成功！', QtCore.QString('OK'))
            return filePath+"/"+fileName
        else:
            QtGui.QMessageBox.information(None, 'INFORMATION', u'提交失败，请检查上传文件！', QtCore.QString('OK'))
            return filePath
    else:
        return filePath
    sys.exit(app.exec_())
