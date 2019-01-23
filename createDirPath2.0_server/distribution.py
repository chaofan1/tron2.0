#-*- coding: utf-8 -*-
import os
import time
import json
import shutil
import logging
import threadpool
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from aliyun import AliyunOss
from config import log_path_server, outputpath


class Finish(SyntaxWarning):
    pass


class TronDistribute:
    def __init__(self):
        self.pool = threadpool.ThreadPool(8)  # 创建线程池
        # 日志位置
        logging.basicConfig(filename=log_path_server + time.strftime("%Y%m%d") + '.log', level=logging.INFO,
                            format="%(asctime)s - %(levelname)s - %(message)s")

    # 解析php传来的json文件，filePath为json路径
    def argParse(self, filePath, timeStamp):
        self.filePath = filePath
        self.progectName, self.userid, self.timeStamp = os.path.splitext(os.path.basename(filePath))[0].split('_')
        create_time = time.strftime("%Y%m%d", time.localtime(eval(timeStamp)))
        self.outputPath = outputpath % (self.progectName, create_time)  # 存放外包公司目录的位置
        print self.outputPath
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
                        basePath = self.outputPath + os.sep + cp['pack_dir_name'] \
                                   + os.sep + self.progectName + os.sep + fieldName + os.sep + shotNum + os.sep
                        if not os.path.exists(basePath):
                            os.makedirs(basePath)
                        Paths.append(((basePath, material), None))
            # 解析资产，将资产所在路径与资产目标路径放到列表
            for asset in response['assets']:
                for tache in asset['tache']:
                    tache_name = tache['tache_lower_name']
                    # extension_name = tache['extension_name']
                    linux_path = tache['linux_path']
                    for cp in response['company_data']:
                        asset_basepath = self.outputPath + os.sep + cp['pack_dir_name']\
                                         + os.sep + self.progectName + os.sep + "assets" + os.sep + tache_name
                        if not os.path.exists(asset_basepath):
                            os.makedirs(asset_basepath)
                        Paths.append(((asset_basepath, linux_path), None))
            # 解析相关文件，将相关文件所在路径与相关文件目标路径放到列表
            if referencesList:
                for cp in response['company_data']:
                    referencesDir = self.outputPath + os.sep + cp['pack_dir_name'] \
                                    + os.sep + self.progectName + os.sep + "references"
                    if not os.path.exists(referencesDir):
                        os.makedirs(referencesDir)
                    Paths.append(((referencesDir, referencesList), None))
            logging.info('打开文件，解析参数成功' + self.filePath )
            # 将列表放到线程池，去copy文件
            self.putThread('copy', Paths)
        except Exception as e:
            logging.info('打开文件,解析参数出错')
            logging.error(e)

    def putThread(self, task, publicArg=None):
        # 接受到argParse函数传递的大列表，用线程池去拷贝
        if task == 'copy':
            print('---开始拷贝---')
            requests = threadpool.makeRequests(self.copyFile, publicArg, callback=self.result)
            [self.pool.putRequest(req) for req in requests]
            try:
                self.pool.wait()
                os.remove(self.filePath)  # 测试或上线打开，拷贝完，删除json文件
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
    #         logging.error(e)w
    #         return 1, e

    def Deldir(self, dir_time_str):
        dir_time_dic = eval(dir_time_str)
        for dirname, timeStamp in dir_time_dic.items():
            try:
                create_time = time.strftime("%Y%m%d", time.localtime(eval(timeStamp)))
                cpname, proname, user_id = dirname.split('_')
                shutil.rmtree(outputpath % (proname, create_time) + os.sep + dirname)
            except Exception as e:
                logging.info('删除文件出错')
                logging.error(e)

    def result(self, req, res):
        res1, res2 = res
        if res1:
            raise Finish


def transit(Path, dirName):
    print Path + '\t' + dirName
    logging.info('transit:' + Path+'|' + dirName)
    sep = os.sep
    if '.json' in Path:
        with open(Path, 'r') as f:
            response = json.load(f)
        user_name = response['user_name']
        # outuser_name = response['outuser_name']
        cpname = response['company_name']
        email = response['email']
        remark = response['remark']
        create_time = response['create_time']
        create_time = time.strftime("%Y%m%d", time.localtime(eval(create_time)))
        projectName = dirName.split('_')[1]
        outputPath = outputpath % (projectName, create_time)
        tranfilePath = outputPath + sep + dirName
        AliyunOss(tranfilePath, dirName, cpname, email, user_name, remark).uploadFile()
        #os.remove(Path)  # 测试或上线打开，删除json文件
    else:
        AliyunOss(Path, dirName, '', '', '', '').uploadFile()


if __name__ == "__main__":
    TronDistribute().argParse('/Users/user/Desktop/test/tron_test/FUY_93_1537170831.json')
    transit('/Users/user/Desktop/test/tron_test/huanju_1_1537525279.json', 'huanju_FUY_1')



