#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
# Filename: createFolder.py
#创建文件夹


import os,pwd


class TronFolder:

    def __init__(self):
        self.sep = os.sep

    def CreateFolder(self, folderPath, pmt, user):
        if folderPath:
            if not os.path.exists(folderPath):
                parent_Dir = os.path.dirname(folderPath)
                if not os.path.exists(parent_Dir):
                    os.makedirs(parent_Dir)
                parentMode = oct(os.stat(parent_Dir).st_mode)[-3:]
                if parentMode == "555":
                    os.chmod(parent_Dir, 0755)
                try:
                    os.makedirs(folderPath)
                    userID = 11001
                    groupID = 11000
                    if user:
                        userAll = []
                        for userDn in pwd.getpwall():
                            userAll.append(userDn[0])
                        if user in userAll:
                            userID = pwd.getpwnam(user).pw_uid
                            groupID = pwd.getpwnam(user).pw_gid
                    os.chown(folderPath, userID, groupID)
                    if (int(pmt)) == 555:
                        os.chmod(folderPath, 0555)
                        #print "yes chmod %s" %(folderPath)
                    elif (int(pmt)) == 755:
                        os.chmod(folderPath, 0755)
                    elif (int(pmt)) == 775:
                        os.chmod(folderPath, 0775)
                    elif (int(pmt)) == 777:
                        os.chmod(folderPath, 0777)
                    else:
                        os.chmod(folderPath, int(pmt))
                    #print "chmod %s mode %s" %(folderPath,pmt)
                except Exception, e:
                    print str(e)
                if parentMode == "555":
                    os.chmod(parent_Dir, 0555)

    def CreateStuff(self, proPath, seqName, shotName, task, fileName, user):  # proPath:/Tron/FUY
        #taskGroup = 'ani', 'prd', 'cmp', 'art', 'dmt', 'efx', 'lgt', 'mmv', 'mod', 'rig', 'tex', 'prv'
        dirPath = ""
        if len(proPath):
            dirPath += proPath + self.sep
            if len(seqName):
                dirPath += seqName + self.sep
                if len(shotName):
                    dirPath += shotName + self.sep   # 分配镜头任务：/Tron/FUY/001/001/
        stuffPath = dirPath + 'Stuff'    # 分配镜头任务：/Tron/FUY/01/001/Stuff
        if not os.path.exists(stuffPath):
            self.CreateFolder(stuffPath, "0555","")
        if len(task) != 0:
            taskPath = stuffPath + self.sep + task  # 创建项目：/Tron/FUY/Stuff/prd
            self.CreateFolder(taskPath, "0555", "")
            taskPath += self.sep
            userLeader = task+"leader"
            if task == 'prd':
                if len(shotName) == 0:
                    self.CreateFolder((taskPath + "elem"), "0775", userLeader)  # /Tron/FUY/Stuff/prd/elem
                else:
                    self.CreateFolder((taskPath + "audio"), "0775", userLeader)
                    self.CreateFolder((taskPath + 'plates'), "0775", userLeader)
                    prdCache = 'tga', 'dpx', 'exr', 'jpg', 'mov'
                    for i in prdCache:
                        self.CreateFolder((taskPath + "plates" + self.sep + i), "0775", userLeader)
                        fileFolder = stuffPath + self.sep + task + self.sep + "plates" + self.sep+i
                        self.CreateFolder(fileFolder, "0775", user)
            else:
                self.CreateFolder((taskPath + "process"), "0775", userLeader)
                self.CreateFolder((taskPath + "publish"), "0755", userLeader)
            if task == 'cmp':
                if len(shotName) == 0:
                    self.CreateFolder((taskPath + "elem"), "0555", userLeader)  # /Post/FUY/Stuff/cmp/elem
                    self.CreateFolder((taskPath + "elem"+self.sep+"inner"), "0775", userLeader)   # /Post/FUY/Stuff/cmp/elem/inner
                    self.CreateFolder((taskPath + "elem"+self.sep+"vender"), "0775", userLeader)  # /Post/FUY/Stuff/cmp/elem/vender
                else:
                    self.CreateFolder((taskPath + "elem"), "0775", userLeader)
                    self.CreateFolder((taskPath + 'img'), "0775", userLeader)
                    self.CreateFolder((taskPath + "roto"), "0775", userLeader)
            elif task == 'art' or task == 'ani' or task == 'lgt'or task == 'efx':
                self.CreateFolder((taskPath + 'img'), "0775", userLeader)
            if task != "efx" or task != "cmp" or task != "lgt":
                fileFolder = os.path.join(stuffPath, task, "publish")
                if task == "prd":
                   return                            
                else:
                    if len(fileName) != 0:
                        fileFolder += self.sep+fileName
                        if not os.path.exists(fileFolder):
                            self.CreateFolder(fileFolder, "0755", user)
                            self.CreateFolder((fileFolder+self.sep+"pro"), "0755", user)
                            self.CreateFolder((fileFolder+self.sep+"geo"), "0775", user)
                            if task == "efx":
                                self.CreateFolder((fileFolder + self.sep + "img"), "0755", user)
            else:
                taskCache = "publish", "img", "process"
                for cacheD in taskCache:
                    fileFolder = os.path.join(stuffPath, task, cacheD)
                    if len(fileName) != 0:
                        fileFolder += self.sep + fileName
                        if not os.path.exists(fileFolder):
                            self.CreateFolder(fileFolder, "0755", user)

    def CreateWork(self, proPath, seqName, shotName, user, task, fileName):
        dirPath = ""
        if len(proPath):
            dirPath += proPath + self.sep
            if len(seqName):
                dirPath += seqName + self.sep
                if len(shotName):
                    dirPath += shotName + self.sep
        workPath = dirPath + 'Work'
        if not os.path.exists(workPath):
            self.CreateFolder(workPath, "0555", "")
        if not os.path.exists(workPath + self.sep + 'note'):
            self.CreateFolder((workPath + self.sep + 'note'), "0777", "")
            self.CreateFolder((workPath + self.sep + 'taskGroup'), "0555", "baicz")
            self.CreateFolder((workPath + self.sep + 'taskGroup' + self.sep + 'art'), "0775", "majia")
            self.CreateFolder((workPath + self.sep + 'taskGroup' + self.sep + 'ani'), "0775", "dongyun")
            self.CreateFolder((workPath + self.sep + 'taskGroup' + self.sep + 'cmp'), "0775", "wanglb")
            self.CreateFolder((workPath + self.sep + 'taskGroup' + self.sep + 'dmt'), "0775", "wuzj")
            self.CreateFolder((workPath + self.sep + 'taskGroup' + self.sep + 'efx'), "0775", "liujm")
            self.CreateFolder((workPath + self.sep + 'taskGroup' + self.sep + 'lgt'), "0775", "lizq")
            self.CreateFolder((workPath + self.sep + 'taskGroup' + self.sep + 'mmv'), "0775", "qiss")
            self.CreateFolder((workPath + self.sep + 'taskGroup' + self.sep + 'mod'), "0775", "duanzw")
            self.CreateFolder((workPath + self.sep + 'taskGroup' + self.sep + 'prd'), "0775", "zhumy")
            self.CreateFolder((workPath + self.sep + 'taskGroup' + self.sep + 'rig'), "0775", "masb")
            self.CreateFolder((workPath + self.sep + 'taskGroup' + self.sep + 'tex'), "0775", "hanyi")
        if len(user) != 0:
            userWork = workPath+self.sep+user
            # workChild = ""
            if not os.path.exists(userWork):
                self.CreateFolder(userWork, "0755", user)
                workChild = 'fcp', 'nk', 'hip', 'ma', 'ps', 'other'
                # if len(task) != 0:
                #     if task == 'mod' or task == 'rig' or task == 'ani':
                #         workChild = "ma", "other"
                #     elif task == 'art' or task == 'dmt':
                #         workChild = 'ps', 'other'
                #     elif task == 'mmv':
                #         workChild = 'nk', 'ma', 'other'
                #     elif task == 'efx' or task == 'lgt':
                #         workChild = 'hip', 'ma', 'other'
                #     elif task == 'cmp':
                #         workChild = 'nk', 'other'
                #     elif task == 'tex':
                #         workChild = 'ma', 'ps', 'other'
                #     elif task == 'prd':
                #         workChild = 'fcp', 'nk', 'other'
                hfsChild = "cache", "hip", "otl", "pic", "sim"
                for i in workChild:
                    childPath = userWork + self.sep + i
                    self.CreateFolder(childPath, "0755", user)
                    fileE = fileName.replace('master', 'workshop')
                    self.CreateFolder((childPath + "/" + fileE), "0755", user)
                    if i == "hfs":
                        for d in hfsChild:
                            if d == 'hip':
                                dinPath = childPath + self.sep + d
                                self.CreateFolder(dinPath, "0755", user)
                                fileE = fileName.replace('master', 'workshop')
                                self.CreateFolder((dinPath+"/"+fileE), "0755", user)
                            else:
                                dinPath = childPath + self.sep + d
                                self.CreateFolder(dinPath, "0755", user)
