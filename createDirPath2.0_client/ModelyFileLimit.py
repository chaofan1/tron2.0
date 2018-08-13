import os
import pwd


def modelyFolder(folderPath, userName, FileLimit, inherit):
    if folderPath:
        #print folderPath
        parentDir = os.path.dirname(folderPath)
        parentMode = oct(os.stat(parentDir).st_mode)[-3:]
        if parentMode == "555":
            os.popen("chmod 0775 %s" % parentDir)
        if len(userName) !=0:
            userAll = []
            for userDn in pwd.getpwall():
                userAll.append(userDn[0])
            if userName in userAll:
                userID = pwd.getpwnam(userName).pw_uid
                groupID = pwd.getpwnam(userName).pw_gid
            else:
                userID = 11004
                groupID = 11000
        if inherit == 1 :
            fileLime = int(FileLimit)
            print ('chmod jicheng %s ========> %s:%d %d===========>%d' % (folderPath, userName,userID, groupID, fileLime))
            os.popen('chmod -R 0%d %s'%(fileLime,folderPath))
            os.popen('chown -R %d:%d %s'%(userID,groupID,folderPath))

        elif inherit == 0:
            fileLim = 0 + int(FileLimit)
            print ('chmod %s ========> %s:%d %d===========>%d' % (folderPath,userName, userID, groupID, fileLim))
            os.popen('chmod 0%d %s' % (fileLim, folderPath))
            os.popen('chown %d:%d %s' % (userID, groupID, folderPath))
        if parentMode == "555":
            os.popen('chmod 0555 %s' % parentDir)
