#-*- coding: utf-8 -*-
import os
import re
import time
import json
import shutil
# import zipfile
import logging
import smtplib
import platform
import threadpool
# from server_callback import disCallback
from server_callback import callback
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class Finish(SyntaxWarning):
    pass


class TronDistribute:
    def __init__(self, command_id):
        self.command_id = command_id
        # self.material = 'material'
        # self.asset = 'asset'
        # self.references = 'references'
        # self.compressType = 'zip'  # tar,bztar,gzrar
        self.pool = threadpool.ThreadPool(8)
        self.rpath = os.getcwd()
        if platform.system() == 'Windows':
            self.outputPath = re.search(r'(.*)\tron', self.rpath).group(1) + '\tron\uploads\Outsource'
            logging.basicConfig(filename=re.search(r'(.*)\tron', self.rpath).group(1) + '\tron\runtime\log\distribute_log\dis_' + time.strftime("%Y%m%d") + '.log', level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        else:
            self.outputPath = re.search(r'(.*)/tron', self.rpath).group(1) + '/tron/uploads/Outsource'
            logging.basicConfig(filename=re.search(r'(.*)/tron', self.rpath).group(1) + '/tron/runtime/log/distribute_log/dis_' + time.strftime("%Y%m%d") + '.log', level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    def argParse(self, filePath):
        self.filePath = filePath
        self.progectName, self.userid, self.timeStamp = os.path.splitext(os.path.basename(filePath))[0].split('_')
        try:
            with open(self.filePath, 'r') as f:
                response = json.load(f)
            Paths = []
            # 解析参数
            # self.task_ids = response['task_ids']
            self.cpname = response['company_data']['dir_name']
            self.email = response['company_data']['email']
            self.user_name = response['user_name']
            self.describe = response['describe']

            fieldList = response['field_data']
            referencesList = response['references']
            for field in fieldList:
                fieldName = field['field_name']
                shotList = field['shot_data']
                for shot in shotList:
                    shotNum = shot['shot_number']
                    material = shot['material']
                    basePath = self.outputPath + os.sep + self.cpname + os.sep + self.progectName + \
                               os.sep + fieldName + os.sep + shotNum + os.sep
                    os.makedirs(basePath)
                    Paths.append(((basePath, material), None))
            for asset in response['assets']:
                for tache in asset['taches']:
                    tache_name = tache['tache_tolower_name']
                    extension_name = tache['extension_name']
                    linux_path = tache['linux_path']
                    asset_basepath = self.outputPath + os.sep + self.cpname + os.sep + self.progectName + os.sep + \
                       "assets" + os.sep + tache_name
                    if not os.path.exists(asset_basepath):
                        os.makedirs(asset_basepath)
                    Paths.append(((asset_basepath, linux_path), None))

            referencesDir = self.outputPath + os.sep + self.cpname + os.sep + self.progectName + \
                            os.sep + "references"
            os.makedirs(referencesDir)
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
                # os.remove(self.filePath)
                self.putThread('transit')
            except Exception as e:
                pass

        # elif task == 'pack':
        #     print('---开始压缩---')
        #     requests = threadpool.makeRequests(self.packFile, callback=self.result)
        #     [self.pool.putRequest(req) for req in requests]
        #     try:
        #         self.pool.wait()
        #         # self.putThread('transit')  用云之后打开
        #         os.remove(self.filePath)
        #     except Exception as e:
        #         pass

        elif task == 'transit':
            print('---开始上传云---')
            cpdirPath = self.outputPath + os.sep + self.cpname + os.sep + self.progectName
            # 连接腾讯云   判断腾讯云是否有 公司+项目文件夹
                # 云代码
            if '不存在': #没有创建,并上传
                # 云创建代码
                all_dir = map(lambda x: cpdirPath + os.sep + x, os.listdir(cpdirPath))
                requests = threadpool.makeRequests(self.transitYun, all_dir, callback=self.result)
                [self.pool.putRequest(req) for req in requests]
                try:
                    self.pool.wait()
                    self.sendMail(self.cpname, self.email)
                    # shutil.rmtree(self.outputPath + os.sep + self.cpname + os.sep + self.progectName)
                except Exception as e:
                    pass
            else:
                all_dir = []
                for root, dirs, files in os.walk(cpdirPath):
                    for name in files:
                        all_dir.append(os.path.join(root, name))
                requests = threadpool.makeRequests(self.transitYunone, all_dir, callback=self.result)
                [self.pool.putRequest(req) for req in requests]
                try:
                    self.pool.wait()
                    self.sendMail(self.cpname, self.email)
                    # shutil.rmtree(self.outputPath + os.sep + self.cpname + os.sep + self.progectName)
                except Exception as e:
                    pass

    def copyFile(self, *args):
        #X:\BFB\001\001\Stuff\mmv\publish\bfb001001_mmv_wanggang_matchmove\pro
        #X:\BFB\Stuff\dmt\publish\bfb_dmt_caojj_camp3Ri_master\geo\bfb086026_dmt_caojj_YingDiRiJing_v0104.0129
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

    # def packFile(self):
    #     os.chdir(self.outputPath)
    #     try:
    #         cpdirPath = self.cpname + '_' + self.userid + '_' + self.timeStamp
    #         fileList = []
    #         for root, dirs, files in os.walk(cpdirPath):
    #             for name in files:
    #                 fileList.append(os.path.join(root, name))
    #
    #         zf = zipfile.ZipFile(cpdirPath + '.zip', "w", zipfile.ZIP_STORED, allowZip64=True)
    #         for tar in fileList:
    #             zf.write(tar, tar.lstrip(cpdirPath + os.sep))
    #         zf.close()
    #         # 压缩成功，删除公司文件夹
    #         shutil.rmtree(self.outputPath + os.sep + cpName['name'] + os.sep + cpName['name'] + '_' + self.userid + '_' + self.timeStamp)
    #         logging.info(u'压缩文件成功' + cpdirPath )
    #         self.sendMail(cpName)   # 上线之后放传云函数里
    #         return 0, None
    #     except Exception as e:
    #         logging.info(u'压缩出错')
    #         logging.error(e)
    #         return 1, e

    def transitYun(self, filepath):
        try:
            # 进入云公司+项目文件夹下   self.cpname + os.sep + self.progectName
                #上传资料到云代码

            return 0, None
        except Exception as e:
            logging.info('上传云出错')
            logging.error(e)
            return 1, e

    def transitYunone(self, filepath):
        try:
            dirname, filename = os.path.split(filepath)
            yunPath = self.cpname + dirname.split(self.cpname)[1]
            # 判断云路径是否存在，不存在创建
                #拷贝文件 filepath  到创建目录下
            return 0, None
        except Exception as e:
            logging.info('上传云出错')
            logging.error(e)
            return 1, e

    def sendMail(self, name, email):
        if email:
            try:
                smtp_server = 'smtp.163.com'
                from_mail = '15810448048@163.com' # 发送邮箱
                mail_pass = '086023li'  # 邮箱密码
                mailAdd = email  # 外包公司邮箱
                # cc_mail = ['lizhenliang@xxx.com']      # 抄送邮箱
                from_name = self.user_name  # 发送人姓名
                subject = '您有一封来自' + self.user_name + '的邮件'  # 主题
                mail = [
                    "From: %s <%s>" % (from_name, from_mail),
                    str("To: %s" % mailAdd),
                    "Subject: %s" % subject,
                    # "Cc: %s" % ','.join(cc_mail), "utf8"),
                    "",
                    self.describe,
                ]
                msg = '\n'.join(mail)
                s = smtplib.SMTP()
                s.connect(smtp_server, '25')
                s.login(from_mail, mail_pass)
                # s.sendmail(from_mail, to_mail+cc_mail, msg)
                s.sendmail(from_mail, mailAdd, msg)
                s.quit()
                logging.info(u'发送邮件成功' + name + '|'+ mailAdd)
            except Exception as e:
                logging.info('发送邮件失败')
                logging.error(e)
        else:
            logging.info('邮箱为空')
        callback(self.command_id)

    def result(self, req, res):
        res1, res2 = res
        if res1:
            raise Finish


if __name__ == "__main__":
    pass


