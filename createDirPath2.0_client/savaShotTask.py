#-*- coding: utf-8 -*-
import os, shutil, platform
import sys
from PyQt4 import QtCore, QtGui

def SelectShotTask(serverName, filePath, fileName):
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

    # sep = os.sep
    # if platform.system() == 'Linux' or platform.system() == 'Darwin':
    #     inPathFile = os.environ['HOME']
    # else:
    #     inPathFile = "D:/"
    # app = QtGui.QApplication(sys.argv)
    # mainWindow = QtGui.QMainWindow()
    # (seqname, ext) = QtGui.QFileDialog.getOpenFileNameAndFilter(mainWindow,
    #                 QtCore.QString('update a reference'), inPathFile,
    #                 options=QtGui.QFileDialog.ReadOnly)
    # fileOld = (seqname.__str__())
    # print fileOld
    #
    # if fileOld:
    #     fileType = fileOld.split(".")[-1]
    #     file_copy_path = serverName + filePath + sep + fileName + "." + fileType
    #     if not os.path.exists(file_copy_path):
    #         shutil.copy(fileOld, file_copy_path)
    #         QtGui.QMessageBox.information(None, 'INFORMATION', u'提交成功！', QtCore.QString('OK'))
    #     else:
    #         QtGui.QMessageBox.information(None, 'INFORMATION', u'提交失败！', QtCore.QString('OK'))
    #
    # else:
    #     return
    # sys.exit(app.exec_())

SelectShotTask('D:\\','360','test')
