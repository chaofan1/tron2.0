#-*- coding: utf-8 -*-
import os
import time
import json
import boto3
import shutil
import zipfile
import logging
import threadpool
from botocore.client import Config
from server_callback import callback


class Finish(SyntaxWarning):
    pass


class TronDistribute:
    def __init__(self, command_id):
        self.command_id = command_id
        self.material = 'material'
        self.asset = 'asset'
        self.references = 'references'
        self.outputPath = '/Users/zhaojiusi/Code/tron/uploads/Outsource'   # 上线更改盘符
        self.compressType = 'zip'  # tar,bztar,gzrar
        self.pool = threadpool.ThreadPool(8)
        logging.basicConfig(filename='./runtime/log/distribute_log/dis_' + time.strftime("%Y%m%d") + '.log', level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    def argParse(self, filePath):
        self.filePath = filePath
        self.progectName, self.userid, self.timeStamp = os.path.splitext(os.path.basename(filePath))[0].split('_')
        try:
            with open(self.filePath, 'r') as f:
                response = json.load(f)
            Paths = []
            # 解析参数
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
                        cp = cp + '_' + self.userid + '_' + self.timeStamp
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
                os.remove(self.filePath) # 测试打开
                callback(self.command_id)  # 云确定之后删掉
                # self.putThread('transit')
            except Exception as e:
                pass

        elif task == 'transit':
            print('---开始上传云---')
            requests = threadpool.makeRequests(self.transitYun, self.cnameList, callback=self.result)
            [self.pool.putRequest(req) for req in requests]
            try:
                self.pool.wait()
                callback(self.command_id)
            except Exception as e:
                pass

    def copyFile(self, *args):
        try:
            arg, arg2 = args
            if isinstance(arg2, list):
                for path in arg2:
                    print('dir')
                    print(path)
                    basename = os.path.basename(path)
                    if os.path.isdir(path):
                        shutil.copytree(path, arg + os.sep + basename)
                    else:
                        shutil.copyfile(path, arg + os.sep + basename)
            else:
                print(arg2)
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
            cpdirPath = cpName + '_' + self.userid + '_' + self.timeStamp
            fileList = []
            for root, dirs, files in os.walk(cpdirPath):
                for name in files:
                    fileList.append(os.path.join(root, name))

            zf = zipfile.ZipFile(cpdirPath + '.zip', "w", zipfile.ZIP_STORED, allowZip64=True)
            for tar in fileList:
                zf.write(tar)
            zf.close()
            # 压缩成功，删除公司文件夹
            shutil.rmtree(self.outputPath + os.sep + cpName + '_' + self.userid + '_' + self.timeStamp)
            logging.info(u'压缩文件成功' + cpdirPath )
            return 0, None
        except Exception as e:
            logging.info(u'压缩出错')
            logging.error(e)
            return 1, e

    def transitYun(self, cpName):
        try:
            cpdirPath = cpName + '_' + self.userid + '_' + self.timeStamp + '.zip'
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
    def result(self, req, res):
        res1, res2 = res
        if res1:
            raise Finish


if __name__ == "__main__":
    pass


