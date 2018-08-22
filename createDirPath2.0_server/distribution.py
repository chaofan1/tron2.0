#-*- coding: utf-8 -*-
import os
import re
import time
import json
import boto3
import shutil
import zipfile
import logging
import smtplib
import platform
import threadpool
from botocore.client import Config
from server_callback import disCallback


class Finish(SyntaxWarning):
    pass


class TronDistribute:
    def __init__(self, command_id):
        self.command_id = command_id
        self.material = 'material'
        self.asset = 'asset'
        self.references = 'references'
        self.compressType = 'zip'  # tar,bztar,gzrar
        self.pool = threadpool.ThreadPool(8)
        self.rpath = os.getcwd()
        if platform.system() == 'Windows':
            self.outputPath = re.search(r'(.*)\tron', self.rpath ).group(1) + '\tron\uploads\Outsource'
            logging.basicConfig(filename=re.search(r'(.*)\tron', self.rpath).group(1) + '\tron\runtime\log\distribute_log\dis_' + time.strftime("%Y%m%d") + '.log', level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        else:
            self.outputPath = re.search(r'(.*)/tron', self.rpath ).group(1) + '/tron/uploads/Outsource'
            logging.basicConfig(filename=re.search(r'(.*)/tron', self.rpath).group(1) + '/tron/runtime/log/distribute_log/dis_' + time.strftime("%Y%m%d") + '.log', level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    def argParse(self, filePath):
        if platform.system() == 'Windows':
            self.filePath = re.search(r'(.*)\tron', self.rpath).group(1) + os.sep + 'tron' + os.sep + filePath
        else:
            self.filePath = re.search(r'(.*)/tron', self.rpath).group(1) + os.sep + 'tron' + os.sep + filePath

        self.progectName, self.userid, self.timeStamp = os.path.splitext(os.path.basename(filePath))[0].split('_')
        try:
            with open(self.filePath, 'r') as f:
                response = json.load(f)
            Paths = []
            # 解析参数
            self.task_ids = response['task_ids']
            self.cnameList = response['company_data']
            fieldList = response['field_data']
            for field in fieldList:
                fieldName = field['field_name']
                shotList = field['shot_data']
                for shot in shotList:
                    shotNum = shot['shot_number']
                    material = shot['material']
                    assetList = shot['asset_data']
                    referencesList = shot['references_data']
                    for cp in self.cnameList:
                        cp = cp['name'] + '_' + self.userid + '_' + self.timeStamp
                        basePath =self.outputPath + os.sep + cp + os.sep + self.progectName + os.sep + fieldName + os.sep + shotNum + os.sep
                        materialDir = basePath + self.material
                        assetDir = basePath + self.asset
                        referencesDir = basePath + self.references

                        os.makedirs(materialDir)
                        os.makedirs(assetDir)
                        os.makedirs(referencesDir)
                        Paths.append(((materialDir, material), None))
                        Paths.append(((assetDir, assetList), None))
                        Paths.append(((referencesDir, referencesList), None))
            logging.info('打开文件，解析参数成功' + self.filePath )
            self.putThread('copy', Paths)
        except Exception as e:
            logging.info('打开文件,解析参数出错')
            logging.error(e)

    def putThread(self, task, publicArg=None):
        if task == 'copy':
            print('---开始拷贝---')
            requests = threadpool.makeRequests(self.copyFile, publicArg, callback=self.result)
            [self.pool.putRequest(req) for req in requests]
            try:
                self.pool.wait()
                self.putThread('pack')
            except Exception as e:
                pass

        elif task == 'pack':
            print('---开始压缩---')
            requests = threadpool.makeRequests(self.packFile, self.cnameList, callback=self.result)
            [self.pool.putRequest(req) for req in requests]
            try:
                self.pool.wait()
                # self.putThread('transit')  用云之后打开
                os.remove(self.filePath)
            except Exception as e:
                pass

        elif task == 'transit':
            print('---开始上传云---')
            requests = threadpool.makeRequests(self.transitYun, self.cnameList, callback=self.result)
            [self.pool.putRequest(req) for req in requests]
            try:
                self.pool.wait()
                os.remove(self.filePath)
            except Exception as e:
                pass

    def copyFile(self, *args):
        try:
            arg, arg2 = args
            if isinstance(arg2, list):
                for path in arg2:
                    basename = os.path.basename(path)
                    if os.path.isdir(path):
                        shutil.copytree(path, arg + os.sep + basename)
                    else:
                        shutil.copyfile(path, arg + os.sep + basename)
            else:
                basename = os.path.basename(arg2)
                if os.path.isdir(arg2):
                    shutil.copytree(arg2, arg + os.sep + basename)
                else:
                    shutil.copyfile(arg2, arg + os.sep + basename)
            logging.info('拷贝文件成功' + str(arg2))
            return 0, None
        except Exception as e:
            logging.info('拷贝出错')
            logging.error(e)
            return 1, e

    def packFile(self, cpName):
        os.chdir(self.outputPath)
        try:
            cpdirPath = cpName['name'] + '_' + self.userid + '_' + self.timeStamp
            fileList = []
            for root, dirs, files in os.walk(cpdirPath):
                for name in files:
                    fileList.append(os.path.join(root, name))

            zf = zipfile.ZipFile(cpdirPath + '.zip', "w", zipfile.ZIP_STORED, allowZip64=True)
            for tar in fileList:
                zf.write(tar)
            zf.close()
            # 压缩成功，删除公司文件夹
            shutil.rmtree(self.outputPath + os.sep + cpName['name'] + '_' + self.userid + '_' + self.timeStamp)
            logging.info(u'压缩文件成功' + cpdirPath )
            self.sendMail(cpName)   # 上线之后放传云函数里
            print '发送邮件成功'
            return 0, None
        except Exception as e:
            logging.info(u'压缩出错')
            logging.error(e)
            return 1, e

    def transitYun(self, cpName):
        try:
            cpdirPath = cpName['name'] + '_' + self.userid + '_' + self.timeStamp + '.zip'
            s3 = boto3.resource('s3', config=Config(signature_version='s3v4'))
            if 'Distribute' not in s3.buckets.all():
                s3.create_bucket(Bucket='Distribute')

            s3.Object("Distribute", cpName + '_' + self.userid + '_' + self.timeStamp).upload_file(cpdirPath)
            # 成功之后删除压缩包
            os.remove(cpdirPath)
            logging.info('上传云成功' + cpdirPath )
            return 0, None
        except Exception as e:
            logging.info('上传云出错')
            logging.error(e)
            return 1, e

        # 设置凭证
        # aws configure
        # AWS Access Key ID: foo
        # AWS Secret Access Key: bar
        # Default region name [us-west-2]: us-west-2
        # Default output format [None]: json

    def sendMail(self, mailInfo):
        if mailInfo:
            try:
                smtp_server = 'smtp.163.com'
                from_mail = '15810448048@163.com'  # 发送邮箱
                mail_pass = '1993323086li'  # 邮箱密码
                mailAdd = mailInfo['email']  # 外包公司邮箱
                # cc_mail = ['lizhenliang@xxx.com']      # 抄送邮箱
                from_name = '聚光绘影'  # 发送人姓名
                subject = '聚光绘影'  # 主题
                mail = [
                    "From: %s <%s>" % (from_name, from_mail),
                    str("To: %s" % mailAdd),
                    "Subject: %s" % subject,
                    # "Cc: %s" % ','.join(cc_mail), "utf8"),
                    "",
                    "分发test",
                ]
                msg = '\n'.join(mail)
                s = smtplib.SMTP()
                s.connect(smtp_server, '25')
                s.login(from_mail, mail_pass)
                # s.sendmail(from_mail, to_mail+cc_mail, msg)
                s.sendmail(from_mail, mailAdd, msg)
                s.quit()
                disCallback([mailAdd['name'], self.task_ids])
                logging.info(u'发送邮件成功' + mailInfo['name'] + '|'+ mailAdd)
                return 0, None
            except Exception as e:
                logging.info('发送邮件失败')
                logging.error(e)
                return 1, e
        else:
            logging.info('邮箱为空')

    def result(self, req, res):
        res1, res2 = res
        if res1:
            raise Finish


if __name__ == "__main__":
    pass


