import os
import ModelyFileLimit


userFolders = os.listdir('/illuminafx')
for userFolder in userFolders:
    if len(userFolder.split(".")) != 2:
        userPath = os.path.join('/illuminafx', userFolder)
        userPost = userPath.replace('/Tron','/Post')
        if userFolder == 'taskGroup':
            ModelyFileLimit.modelyFolder(userPath, 'illuminait', "777", 1)
        elif userFolder == 'note':
            ModelyFileLimit.modelyFolder(userPath, 'illuminait', "777", 1)
        else:
            ModelyFileLimit.modelyFolder(userPath, userFolder, "775", 1)
