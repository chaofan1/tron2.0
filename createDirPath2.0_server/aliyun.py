#!/usr/bin/env python
#coding=utf-8
import re
import os,sys
import oss2
import time
import logging
from oss2 import SizedFileAdapter, determine_part_size
from oss2.models import PartInfo
from aliyunsdkcore import client
# from aliyunsdkram.request.v20150501 import CreateUserRequest,CreateAccessKeyRequest,ListUsersRequest,AttachPolicyToUserRequest,CreatePolicyRequest


class AliyunOss():
    def __init__(self,filePath,dirname):
        logging.basicConfig(filename='/Users/user/Desktop/test/distribute_log/dis_' +
                                     time.strftime("%Y%m%d") + '.log', level=logging.INFO,
                            format="%(asctime)s - %(levelname)s - %(message)s")

        # 管理验证
        self.clt = client.AcsClient('LTAIwpOv4aA4PQUS', '4cDyqy3lXuiSRtqR9xjUYmMdikEFxG', 'cn-hangzhou')
        # oss验证
        auth = oss2.Auth('LTAIwpOv4aA4PQUS', '4cDyqy3lXuiSRtqR9xjUYmMdikEFxG')
        self.bucket = oss2.Bucket(auth, 'http://oss-cn-shanghai.aliyuncs.com', 'jg-testwww')
        self.filePath = filePath
        self.dirname = dirname
        self.sep = os.sep

    # def userExit(self):
    #     request = ListUsersRequest.ListUsersRequest()
    #     result = self.clt.get_response(request)
    #
    #     if result[0] == 200:
    #         res = result[2]
    #         userList = re.findall(r'<UserName>(.*?)</UserName>', res)
    #         if self.userName not in userList:
    #             self.createUser()
    #         else:
    #             pass
    #         self.uploadFile()
    #         logging.info('userList ok')
    #     else:
    #         logging.info('userList error')
    #
    # def createUser(self):
    #     request = CreateUserRequest.CreateUserRequest()
    #     request.set_UserName(self.userName)
    #     if self.email:
    #         request.set_Email(self.email)
    #     # 发起请求，并得到response
    #     result = self.clt.get_response(request)
    #
    #     if result[0] == 200:
    #         logging.info('create yun user ok')
    #         self.createAccess()
    #     else:
    #         logging.info('create yun user error')
    #         print '创建用户失败'
    #
    # def createAccess(self):
    #     request = CreateAccessKeyRequest.CreateAccessKeyRequest()
    #     request.set_UserName(self.userName)
    #     result = self.clt.get_response(request)
    #     print result
    #     if result[0] == 200:
    #         logging.info('create userAccess ok')
    #     else:
    #         logging.info('create userAccess error')

    def file_name(self):
        try:
            L = []
            for root, dirs, files in os.walk(self.filePath):
                for file in files:
                    L.append(os.path.join(root, file))
            logging.info('get uploadFiles ok')
            return L

        except Exception as e:
            logging.info('get uploadFiles error')
            logging.error(e)

    def uploadFile(self):
        filelist = self.file_name()
        try:
            for file in filelist:
                key = self.dirname + file.split(self.dirname)[1]
                total_size = os.path.getsize(file)
                # determine_part_size方法用来确定分片大小。
                part_size = determine_part_size(total_size, preferred_size=100 * 1024)

                # 初始化分片。
                upload_id = self.bucket.init_multipart_upload(key).upload_id
                parts = []

                # 逐个上传分片。
                with open(file, 'rb') as fileobj:
                    part_number = 1
                    offset = 0
                    while offset < total_size:
                        num_to_upload = min(part_size, total_size - offset)
                        # SizedFileAdapter(fileobj, size)方法会生成一个新的文件对象，重新计算起始追加位置。
                        result = self.bucket.upload_part(key, upload_id, part_number,
                                                         SizedFileAdapter(fileobj, num_to_upload))
                        parts.append(PartInfo(part_number, result.etag))
                        offset += num_to_upload
                        part_number += 1

                # 完成分片上传。
                self.bucket.complete_multipart_upload(key, upload_id, parts)
        except Exception as e:
            logging.info('upload file to yun error')
            logging.error(e)

    # def createPolicy(self):
    #     request = CreatePolicyRequest.CreatePolicyRequest()
    #     policy = '{"Version": "1","Statement": [{"Effect": "Allow","Action": ["oss:GetObject", "oss:GetObjectAcl"],"Resource": ["acs:oss:*:*:jg-testwww/'+self.dirname+'/*"]}, {"Effect": "Allow","Action": ["oss:ListObjects","oss:ListObjectsAcl"],"Resource": ["acs:oss:*:*:jg-testwww"],"Condition": {"StringLike": {"oss:Delimiter": "/","oss:Prefix":["", "'+self.dirname+'/*"]}}}, {"Effect": "Allow","Action": ["oss:ListBuckets", "oss:ListBucketsAcl"],"Resource": ["acs:oss:*:*:*"],"Condition": {"StringLike": {"oss:Delimiter": "/","oss:Prefix": ["", "jg-testwww/*"]}}}]}'
    #     policyParams = {"PolicyName": self.userName, "PolicyDocument": policy, "Description": self.userName}
    #     request.set_query_params(policyParams)
    #     result = self.clt.get_response(request)
    #     if result[0] == 200:
    #         logging.info('create policy ok')
    #         self.attachToUser()
    #     else:
    #         logging.info('create policy error')
    #
    # def attachToUser(self):
    #     request = AttachPolicyToUserRequest.AttachPolicyToUserRequest()
    #     attParams = {'PolicyName': self.userName, 'UserName': self.userName, 'PolicyType': 'Custom'}
    #     request.set_query_params(attParams)
    #     result = self.clt.get_response(request)
    #     if result[0] == 200:
    #         logging.info('attach policy to user ok')
    #     else:
    #         logging.info('attach policy to user error')
