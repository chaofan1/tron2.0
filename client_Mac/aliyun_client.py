#-*- coding: utf-8 -*-
import oss2
import os
from upload import UploadFile
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class AliyunDownload():
    def __init__(self,dirname):
        self.localPath = UploadFile().select_dir('')
        self.dirname = dirname

    def downLoad(self):
        try:
            self.auth = oss2.Auth('LTAIwpOv4aA4PQUS', '4cDyqy3lXuiSRtqR9xjUYmMdikEFxG')
            self.bucket = oss2.Bucket(self.auth, 'http://oss-cn-shanghai.aliyuncs.com', 'jg-testwww')
            self.keylist = []
            for obj in oss2.ObjectIterator(self.bucket, prefix=self.dirname + '/'):
                self.keylist.append(obj.key)
            for ObjectName in self.keylist:
                localDir = '/'.join(ObjectName.split('/')[:-1])
                if not os.path.exists(self.localPath + os.sep + localDir):
                    os.makedirs(self.localPath + os.sep + localDir)
                # 下载OSS文件到本地文件。如果指定的本地文件存在会覆盖，不存在则新建。
                self.bucket.get_object_to_file(ObjectName, self.localPath+os.sep+ObjectName)
            UploadFile().download_success()
        except:
            print('下载失败，请检查网络')
            UploadFile().download_fail()


if __name__ == '__main__':
    AliyunDownload('').downLoad()

