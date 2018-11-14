#!/usr/bin/env python
#coding=utf-8
import re
import os,sys
import oss2
from oss2 import SizedFileAdapter, determine_part_size
from oss2.models import PartInfo
from aliyunsdkcore import client
from aliyunsdkram.request.v20150501 import CreateUserRequest,CreateAccessKeyRequest,ListUsersRequest


class AliyunOss():
    def __init__(self, userName, phone, filePath, email=None):
        self.clt = client.AcsClient('LTAIwpOv4aA4PQUS', '4cDyqy3lXuiSRtqR9xjUYmMdikEFxG', 'cn-hangzhou')
        auth = oss2.Auth('LTAIwpOv4aA4PQUS', '4cDyqy3lXuiSRtqR9xjUYmMdikEFxG')
        self.bucket = oss2.Bucket(auth, 'http://oss-cn-shanghai.aliyuncs.com', 'jg-testwww')
        self.filePath = filePath
        self.key = os.path.basename(self.filePath)
        self.userName = userName
        self.phone = phone
        self.email = email
        self.sep = os.sep

    def userExit(self):
        request = ListUsersRequest.ListUsersRequest()
        result = self.clt.get_response(request)
        if result[0] == 200:
            res = result[2]
            userList = re.findall(r'<UserName>(.*?)</UserName>', res)
            if self.userName not in userList:
                self.createUser()
            else:
                self.uploadFile()
        else:
            print '获取用户列表失败'

    def createUser(self):
        request = CreateUserRequest.CreateUserRequest()
        request.set_UserName(self.userName)
        if self.phone:
            request.set_accept_format(self.phone)
        if self.email:
            request.set_Email(self.email)
        # 发起请求，并得到response
        result = self.clt.get_response(request)
        if result[0] == 200:
            self.createAccess()
        else:
            print '创建用户失败'

    def createAccess(self):
        request = CreateAccessKeyRequest.CreateAccessKeyRequest()
        request.set_UserName(self.userName)
        result = self.clt.get_response(request)
        if result[0] == 200:
            pass
        else:
            print '创建用户ack失败'

    def uploadFile(self):
        total_size = os.path.getsize(self.filePath)
        # determine_part_size方法用来确定分片大小。
        part_size = determine_part_size(total_size, preferred_size=100 * 1024)

        # 初始化分片。
        upload_id = self.bucket.init_multipart_upload(key).upload_id
        parts = []

        # 逐个上传分片。
        with open(self.filePath, 'rb') as fileobj:
            part_number = 1
            offset = 0
            while offset < total_size:
                num_to_upload = min(part_size, total_size - offset)
                # SizedFileAdapter(fileobj, size)方法会生成一个新的文件对象，重新计算起始追加位置。
                result = self.bucket.upload_part(self.key, upload_id, part_number, SizedFileAdapter(fileobj, num_to_upload))
                parts.append(PartInfo(part_number, result.etag))
                offset += num_to_upload
                part_number += 1

        # 完成分片上传。
        self.bucket.complete_multipart_upload(self.key, upload_id, parts)

    # 展示进度
    def percentage(self,consumed_bytes, total_bytes):
            if total_bytes:
                rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
                print rate
                # print('\r{0}% '.format(rate), end='')
                # sys.stdout.flush()

    def downLoad(self, userId, userKey, ObjectName, localPath):
        auth = oss2.Auth(userId, userKey)
        bucket = oss2.Bucket(auth, 'http://oss-cn-shanghai.aliyuncs.com', 'jg-testwww')
        # 请将oss2.defaults.connection_pool_size设成大于或等于线程数，并将part_size参数设成大于或等于oss2.defaults.multiget_part_size。
        oss2.resumable_download(bucket, ObjectName, localPath+self.sep+ObjectName,
                                store=oss2.ResumableDownloadStore(root='/tmp'),
                                multiget_threshold=20 * 1024 * 1024,
                                part_size=10 * 1024 * 1024,
                                num_threads=3,
                                progress_callback=self.percentage)
