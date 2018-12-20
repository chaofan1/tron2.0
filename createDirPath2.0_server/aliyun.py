#!/usr/bin/env python
#coding=utf-8
import os
import oss2
import time
import smtplib
import logging
from oss2 import SizedFileAdapter, determine_part_size
from oss2.models import PartInfo
from aliyunsdkcore import client
# from aliyunsdkram.request.v20150501 import CreateUserRequest,CreateAccessKeyRequest,ListUsersRequest,AttachPolicyToUserRequest,CreatePolicyRequest


class AliyunOss():
    def __init__(self,filePath,dirname, cpname, email, user_name, remark):
        logging.basicConfig(filename='/Public/tronPipelineScript/tron2.0/distribute_log/dis_' +
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
        self.cpname = cpname
        self.email = email
        self.user_name = user_name
        self.remark = remark

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
            logging.info('upload file to yun ok')
            self.sendMail()
        except Exception as e:
            logging.info('upload file to yun error')
            logging.error(e)

    def sendMail(self):
        if self.email:
            try:
                smtp_server = 'smtp.yeah.net'
                from_mail = 'tron2018@yeah.net'  # 发送邮箱
                mail_pass = 'liangcy880716'  # 邮箱密码
                mailAdd = self.email  # 外包公司邮箱
                # cc_mail = ['lizhenliang@xxx.com']      # 抄送邮箱
                from_name = self.user_name  # 发送人姓名
                subject = '您有一封来自Tron平台的邮件(请勿回复)'  # 主题
                mail = [
                    "From: %s <%s>" % (from_name, from_mail),
                    str("To: %s" % mailAdd),
                    "Subject: %s" % subject,
                    # "Cc: %s" % ','.join(cc_mail), "utf8"),
                    "",
                    self.user_name + '通知您登录Tron下载最新分发内容.' + self.remark + "(请勿回复此邮件)",
                ]
                msg = '\n'.join(mail)
                s = smtplib.SMTP()
                s.connect(smtp_server, '25')
                s.login(from_mail, mail_pass)
                # s.sendmail(from_mail, to_mail+cc_mail, msg)
                s.sendmail(from_mail, mailAdd, msg)
                s.quit()
                logging.info(u'发送邮件成功' + self.cpname + '|' + mailAdd)
            except Exception as e:
                logging.info('发送邮件失败')
                logging.error(e)
        else:
            logging.info('邮箱为空')

    def download(self, path):
        try:
            self.keylist = []
            for obj in oss2.ObjectIterator(self.bucket, prefix=self.dirname + '/'):
                self.keylist.append(obj.key)
            for ObjectName in self.keylist:
                localDir = '/'.join(ObjectName.split('/')[:-1])
                if not os.path.exists(path + os.sep + localDir):
                    os.makedirs(path + os.sep + localDir)
                # 下载OSS文件到本地文件。如果指定的本地文件存在会覆盖，不存在则新建。
                self.bucket.get_object_to_file(ObjectName, path+os.sep+ObjectName)
        except:
            print('下载失败，请检查网络')



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
