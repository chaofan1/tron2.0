#-*- coding: utf-8 -*-
import os
import re
import time
import json
import shutil
import logging
import smtplib
import platform
import threadpool
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class Finish(SyntaxWarning):
    pass


class TronDistribute:
    def __init__(self):
        self.pool = threadpool.ThreadPool(8)
        self.rpath = os.getcwd()
        # if platform.system() == 'Windows':
        #     self.outputPath = re.search(r'(.*)\tron', self.rpath).group(1) + '\tron\uploads\Outsource'
        #     logging.basicConfig(filename=re.search(r'(.*)\tron', self.rpath).group(1) + '\tron\runtime\log\distribute_log\dis_' + time.strftime("%Y%m%d") + '.log', level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        # else:
        #     self.outputPath = re.search(r'(.*)/tron', self.rpath).group(1) + '/tron/uploads/Outsource'
        #     logging.basicConfig(filename=re.search(r'(.*)/tron', self.rpath).group(1) + '/tron/runtime/log/distribute_log/dis_' + time.strftime("%Y%m%d") + '.log', level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        if platform.system() == 'Windows':
                self.outputPath = '\usr\local\Code\tron\uploads\Projects\Outsource'
                logging.basicConfig(filename='\usr\local\Code\tron\runtime\log\distribute_log\dis_' + time.strftime("%Y%m%d") + '.log', level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        else:
                self.outputPath = '/usr/local/Code/tron/uploads/Projects/Outsource'
                logging.basicConfig(filename='/usr/local/Code/tron/runtime/log/distribute_log/dis_' + time.strftime("%Y%m%d") + '.log', level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    def argParse(self, filePath):
        self.filePath = filePath
        self.progectName, self.userid, self.timeStamp = os.path.splitext(os.path.basename(filePath))[0].split('_')
        try:
            with open(self.filePath, 'r') as f:
                response = json.load(f)
            Paths = []
            # 解析参数
            fieldList = response['field_data']
            referencesList = response['references']
            # 解析素材，将素材所在路径与素材目标路径放到列表
            for field in fieldList:
                fieldName = field['field_name']
                shotList = field['shot_data']
                for shot in shotList:
                    shotNum = shot['shot_number']
                    material = shot['material']
                    for cp in response['company_data']:
                        basePath = self.outputPath + os.sep + cp['dir_name'] + os.sep + cp['pack_dir_name'] \
                                   + os.sep + self.progectName + os.sep + fieldName + os.sep + shotNum + os.sep
                        if not os.path.exists(basePath):
                            os.makedirs(basePath)
                        Paths.append(((basePath, material), None))
            # 解析资产，将资产所在路径与资产目标路径放到列表
            for asset in response['assets']:
                for tache in asset['tache']:
                    tache_name = tache['tache_lower_name']
                    extension_name = tache['extension_name']
                    linux_path = tache['linux_path']
                    for cp in response['company_data']:
                        asset_basepath = self.outputPath + os.sep + cp['dir_name'] + os.sep + cp['pack_dir_name']\
                                         + os.sep + self.progectName + os.sep + "assets" + os.sep + tache_name
                        if not os.path.exists(asset_basepath):
                            os.makedirs(asset_basepath)
                        Paths.append(((asset_basepath, linux_path), None))
            # 解析相关文件，将相关文件所在路径与相关文件目标路径放到列表
            for cp in response['company_data']:
                referencesDir = self.outputPath + os.sep + cp['dir_name'] + os.sep + cp['pack_dir_name'] \
                                + os.sep + self.progectName + os.sep + "references"
                if not os.path.exists(referencesDir):
                    os.makedirs(referencesDir)
                Paths.append(((referencesDir, referencesList), None))

            logging.info('打开文件，解析参数成功' + self.filePath )
            self.putThread('copy', Paths)
        except Exception as e:
            logging.info('打开文件,解析参数出错')
            logging.error(e)

    def putThread(self, task, publicArg=None, transitArg=None):
        # 接受到argParse函数传递的大列表，用线程池去拷贝
        if task == 'copy':
            print('---开始拷贝---')
            requests = threadpool.makeRequests(self.copyFile, publicArg, callback=self.result)
            [self.pool.putRequest(req) for req in requests]
            try:
                self.pool.wait()
                # os.remove(self.filePath) # 测试或上线打开，拷贝完文件，删除json文件
            except Exception as e:
                pass
        # 暂时用不上
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

        # 上传云，publicArg为 parse.py传来的json文件路径
        elif task == 'transit':
            print('---开始上传云---')
            self.transitArg = transitArg
            argslist = []
            with open(publicArg, 'r') as f:
                response = json.load(f)
            self.cpname = response['company_name']
            self.progectName = response['project_name']
            # 外包公司文件路径
            dirPath = self.outputPath + os.sep + self.cpname + os.sep + self.transitArg + os.sep + self.progectName
            # 连接云,判断 公司名/项目 文件夹是否存在
            s = '云对象'
            # 不存在说明第一次给外包公司发包，直接创建 /公司/项目文件夹 进去文件夹，将本地文件上传到该文件夹下
            # 存在说明后增文件，也要按照对应文件夹放好
            if "不存在":
                # 创建 /公司/项目文件夹 进去文件夹
                filePaths = map(lambda x: dirPath + os.sep + x, os.listdir(dirPath))
                for i in filePaths:
                    argslist.append(([i, s], None))
            else:
                all_dir = []
                for root, dirs, files in os.walk(dirPath):
                    for name in files:
                        all_dir.append(os.path.join(root, name))
                for i in all_dir:
                    argslist.append(([0, [i, s]], None))

            requests = threadpool.makeRequests(self.transitYun, argslist, callback=self.result)
            [self.pool.putRequest(req) for req in requests]
            try:
                self.pool.wait()
                # 上传云之后发送邮件
                self.sendMail(self.cpname, response['email'], response['user_name'], response['remark'])
                # 递归删除本地公司下项目文件夹，测试或上线打开
                # shutil.rmtree(self.outputPath + os.sep + self.cpname + os.sep + transitArg)
            except Exception as e:
                pass

    def copyFile(self, *args):
        # X:\BFB\001\001\Stuff\mmv\publish\bfb001001_mmv_wanggang_matchmove\pro
        # X:\BFB\001\Stuff\mmv\publish\bfb001001_mmv_wanggang_matchmove\pro
        # X:\BFB\Stuff\dmt\publish\bfb_dmt_caojj_camp3Ri_master\geo\bfb086026_dmt_caojj_YingDiRiJing_v0104.0129
        # try:
            # arg拷贝的目标路径，arg2被拷贝文件路径，有可能是列表（资产，相关），有可能单独路径（素材）
            # arg, arg2 = args
            # if isinstance(arg2, list):
            #     for path in arg2:
            #         basename = os.path.basename(path)
            #         arg = arg.replace('\\', '/')  # 上线删除
            #         filePath = path.split('\\')  # 上线改为'/'
            #         # 判断是否为资产
            #         if 'assets' in arg and len(filePath) >= 5:
            #             # 是资产且长度大于5，同时第四位是Stuff,并且geo,pro在路径里，说明是某个镜头的未制作完成资产，需要去解析文件
            #             if filePath[4] == 'Stuff' and ('pro' in path or 'geo' in path):
            #                 cpname = arg.split('/')[2]
            #                 # 创建属于某个镜头的单独资产文件夹
            #                 shotassetsPath = self.outputPath + os.sep + cpname + os.sep + self.progectName + os.sep + \
            #                                  filePath[2] + os.sep + filePath[3] + os.sep + 'assets' + os.sep + filePath[
            #                                      5]
            #                 os.makedirs(self.outputPath + os.sep + cpname + os.sep + self.progectName + os.sep +
            #                             filePath[2] + os.sep + filePath[3] + os.sep + 'assets' + os.sep + filePath[5])
            #                 if os.path.isdir(path):
            #                     if os.path.exists(shotassetsPath + os.sep + basename):
            #                         shutil.rmtree(shotassetsPath + os.sep + basename)
            #                     shutil.copytree(path, shotassetsPath)
            #                     # 解析
            #                 else:
            #                     shutil.copyfile(path, shotassetsPath)
            #                     # 解析
            #             else:
            #                 if os.path.isdir(path):
            #                     if os.path.exists(arg + os.sep + basename):
            #                         shutil.rmtree(arg + os.sep + basename)
            #                     shutil.copytree(path, arg + os.sep + basename)
            #                 else:
            #                     shutil.copyfile(path, arg + os.sep + basename)
            #
            #         else:
            #             if os.path.isdir(path):
            #                 if os.path.exists(arg + os.sep + basename):
            #                     shutil.rmtree(arg + os.sep + basename)
            #                 shutil.copytree(path, arg + os.sep + basename)
            #             else:
            #                 shutil.copyfile(path, arg + os.sep + basename)
        try:
            arg, arg2 = args
            if isinstance(arg2, list):
                for path in arg2:
                    basename = os.path.basename(path)
                    if os.path.isdir(path):
                        if os.path.exists(arg + os.sep + basename):
                            shutil.rmtree(arg + os.sep + basename)
                        shutil.copytree(path, arg + os.sep + basename)
                    else:
                        shutil.copyfile(path, arg + os.sep + basename)
            else:
                basename = os.path.basename(arg2)
                if os.path.isdir(arg2):
                    if os.path.exists(arg + os.sep + basename):
                        shutil.rmtree(arg + os.sep + basename)
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

    def transitYun(self, arg1, arg2):
        try:
            # 后增文件
            if arg1 == 0:
                dirname, filename = os.path.split(arg2[0])
                yunPath = self.cpname + dirname.split(self.transitArg)[1]
                # 判断云路径是否存在，不存在创建
                # 拷贝文件 filepath  到创建目录下
            # 第一次上传云c
            else:
                pass
                # print arg1
                # 进去 公司/项目文件夹下
                # 上传文件到1文件夹下
            return 0, None
        except Exception as e:
            logging.info('上传云出错')
            logging.error(e)
            return 1, e

    def sendMail(self, cpname, email, user_name, remark):
        if email:
            try:
                smtp_server = 'smtp.yeah.net'
                from_mail = 'tron2018@yeah.net'  # 发送邮箱
                mail_pass = 'liangcy880716'  # 邮箱密码
                mailAdd = email  # 外包公司邮箱
                # cc_mail = ['lizhenliang@xxx.com']      # 抄送邮箱
                from_name = user_name  # 发送人姓名
                subject = '您有一封来自' + user_name + '的邮件'  # 主题
                mail = [
                    "From: %s <%s>" % (from_name, from_mail),
                    str("To: %s" % mailAdd),
                    "Subject: %s" % subject,
                    # "Cc: %s" % ','.join(cc_mail), "utf8"),
                    "",
                    remark,
                ]
                msg = '\n'.join(mail)
                s = smtplib.SMTP()
                s.connect(smtp_server, '25')
                s.login(from_mail, mail_pass)
                # s.sendmail(from_mail, to_mail+cc_mail, msg)
                s.sendmail(from_mail, mailAdd, msg)
                s.quit()
                logging.info(u'发送邮件成功' + cpname + '|'+ mailAdd)
            except Exception as e:
                logging.info('发送邮件失败')
                logging.error(e)
        else:
            logging.info('邮箱为空')

    def Deldir(self, dirname):
        cpname, proname, user_id = dirname.split('_')
        shutil.rmtree(self.outputPath + os.sep + cpname + os.sep + dirname)

    def result(self, req, res):
        res1, res2 = res
        if res1:
            raise Finish


if __name__ == "__main__":
    pass


