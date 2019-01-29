#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
#创建项目以及项目内各个文件夹
# Filename: createProject.py


import os
from createFolder import TronFolder
import config


class TronProject:
    def __init__(self):
        self.serverName = config.All
        self.postName = config.Post
        self.refName = config.Reference
        self.userID = 11004
        self.groupID = 11000
        self.sep = os.sep

    def CreatePro(self, proName):
        print "create project %s" %(proName)
        projectChild = {"Doc": "0775", "Vender": "0555", "Client": "0555", "References": "0555"}
        proPath = os.path.join(self.serverName, proName)  # /Tron/FUY
        proPost = os.path.join(self.postName, proName)  # /Post/FUY
        refPaths = os.path.join(self.refName, proName)  # /Library/References/FUY
        if not os.path.exists(proPath):
            os.mkdir(proPath)
            os.chown(proPath, self.userID, self.groupID)
            os.chmod(proPath, 0555)
        if not os.path.exists(refPaths):
            os.mkdir(refPaths)
            os.chown(refPaths, self.userID, self.groupID)
            os.chmod(refPaths, 0555)
        if not os.path.exists(proPost):
            os.mkdir(proPost)
            os.chown(proPost, self.userID, self.groupID)
            os.chmod(proPost, 0555)
        projectChiName = projectChild.keys()
        for i in projectChiName:
            folderPath = proPath+os.sep+i
            refFolPath = refPaths
            if i == "Client":
                if not os.path.exists(folderPath):
                    TronFolder().CreateFolder(folderPath, int(projectChild[i]), "prdleader")
                    TronFolder().CreateFolder((folderPath+os.sep+"incoming"), "0775", "prdleader")
                    TronFolder().CreateFolder((folderPath+os.sep+"outgoing"), "0775", "prdleader")
                    TronFolder().CreateFolder((folderPath + os.sep + "delivery"), "0775", "prdleader")
            elif i == "Vender":
                if not os.path.exists(folderPath):
                    TronFolder().CreateFolder(folderPath, int(projectChild[i]), "prdleader")
                    TronFolder().CreateFolder((folderPath+os.sep+"incoming"), "0775", "prdleader")
                    TronFolder().CreateFolder((folderPath+os.sep+"outgoing"), "0775", "prdleader")
            elif i == "References":
                if not os.path.exists(folderPath):
                    TronFolder().CreateFolder(folderPath, int(projectChild[i]), "prdleader")
                    TronFolder().CreateFolder((folderPath+os.sep+"master"), "0775", "prdleader")
                    TronFolder().CreateFolder((folderPath+os.sep+"inner"), "0775", "prdleader")
                    TronFolder().CreateFolder((folderPath + os.sep + "backup"), "0775", "prdleader")
                if os.path.exists(refFolPath):
                    TronFolder().CreateFolder((refFolPath + os.sep + "shots"), "0775", "prdleader")
                    TronFolder().CreateFolder((refFolPath + os.sep + "assets"), "0775", "prdleader")
            else:
                if not os.path.exists(folderPath):
                    if projectChild[i] == "0555":
                        TronFolder().CreateFolder(folderPath, "0555", "zhouyc")
                    elif projectChild[i] == "0775":
                        TronFolder().CreateFolder(folderPath, "0775", "zhouyc")
        TronFolder().CreateStuff(proPath, "", "", "", "", "")
        TronFolder().CreateStuff(proPost, "", "", "", "", "")
        TronFolder().CreateStuff(proPath, "", "", "prd", "", "")
        TronFolder().CreateStuff(proPost, "", "", "cmp", "", "")
        TronFolder().CreateWork(proPath, "", "", "", "", "")
        TronFolder().CreateWork(proPost, "", "", "", "", "")

    def CreateRef(self, proName, type_,):
        refPath = os.path.join(self.refName, proName)    # /Library/References/FUY
        if os.path.exists(refPath):
            if os.path.exists(refPath):
                if type_ == "shots" or type_ == "assets":
                    refPath = os.path.join(refPath, type_)
                    if not os.path.exists(refPath):
                        TronFolder().CreateFolder(refPath, "0777", "")
                    else:
                        os.chmod(refPath, 0777)

    def CreateDai(self, filePath, filename):
        daiPath = self.serverName + filePath + '/img'   # /Tron/FUY/001/001/stuff/cmp/img
        daiPath2 = self.serverName + filePath + '/mov'
        if not os.path.exists(daiPath):
            TronFolder().CreateFolder(daiPath, "0555", "")
        if not os.path.exists(daiPath2):
            TronFolder().CreateFolder(daiPath2, "0555", "")
        dai_file_path = daiPath + '/' + filename
        dai_file_path2 = daiPath2 + '/' + filename
        if not os.path.exists(daiPath):
            TronFolder().CreateFolder(dai_file_path, "0777", "")
        if not os.path.exists(daiPath2):
            TronFolder().CreateFolder(dai_file_path2, "0777", "")

    def CreateSeq(self, proName, seqName):
        dirPath = self.serverName + os.sep + proName  # /Tron/FUY
        dirPost = self.postName + os.sep + proName  # /Post/FUY
        seqPath = os.path.join(dirPath, seqName)  # /Tron/FUY/001
        seqPost = os.path.join(dirPost, seqName)  # /Post/FUY/01
        if not os.path.exists(seqPath):
            TronFolder().CreateFolder(seqPath, "0555", "")
            TronFolder().CreateFolder(seqPost, "0555", "")
            TronFolder().CreateStuff(dirPath, seqName, "", "", "", "")
            TronFolder().CreateStuff(dirPost, seqName, "", "", "", "")
            TronFolder().CreateStuff(dirPath, seqName, "", "prd", "", "")
            TronFolder().CreateWork(dirPath, seqName, "", "", "", "")
            TronFolder().CreateWork(dirPost, seqName, "", "", "", "")

    def CreateScene(self, proName, seqName, shotName):
        shotPath = os.path.join(self.serverName, proName, seqName, shotName)  # /Tron/FUY/01/001
        shotPost = os.path.join(self.postName, proName, seqName, shotName)   # /Post/FUY/01/001
        if not os.path.exists(shotPath):
            TronFolder().CreateFolder(shotPath, "0555", "")
            TronFolder().CreateFolder(shotPost, "0555", "")

    def CreateAsset(self, proName, type_, user, fileName):
        dirPath = os.path.join(self.serverName, proName)    # /Tron/FUY
        dirPost = os.path.join(self.postName, proName)     # /Post/FUY
        if len(fileName) == 0 and len(type_) == 0:
            print "please give me a file"
        else:
            if type_ == "lgt" or type_ == "cmp":
                TronFolder().CreateStuff(dirPost, "", "", type_, fileName, user)
            else:
                TronFolder().CreateStuff(dirPath, "", "", type_, fileName, user)
        if len(user) == 0:
            print "please give me a user"
        else:
            if type_ == "lgt" or type_ == "cmp":
                TronFolder().CreateWork(dirPost, "", "", user, type_, fileName)
            else:
                TronFolder().CreateWork(dirPath, "", "", user, type_, fileName)

    #                    "FUY"      "01"    "001"   "rig" "liangcy" "fileName"
    def CreateShot(self, proName, seqName, shotName, type_, user, fileName):
        dirPath = os.path.join(self.serverName, proName)  # /Tron/FUY
        dirPost = os.path.join(self.postName, proName)   # /Post/FUY
        if len(fileName) == 0 and len(type_) == 0:
            print "please give me a file"
        else:
            if type_ == "lgt" or type_ == "cmp":   # 灯光渲染与合成都在post盘，其他环节都在tron
                TronFolder().CreateStuff(dirPost, seqName, shotName, type_, fileName, user)
            else:
                TronFolder().CreateStuff(dirPath, seqName, shotName, type_, fileName, user)
        if len(user) == 0:
            print "please give me a user"
        else:
            if type_ == "lgt" or type_ == "cmp":
                TronFolder().CreateWork(dirPost, seqName, shotName, user, type_, fileName)
            else:
                TronFolder().CreateWork(dirPath, seqName, shotName, user, type_, fileName)
