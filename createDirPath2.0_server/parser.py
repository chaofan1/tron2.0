# !/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import shutil,time
import sys, os, logging
from createProject import TronProject
from createFolder import TronFolder
from server_callback import CallBack
# from client import clientLink
from distribution import TronDistribute,transit
from aliyun import AliyunOss
import config
from transit_info import handle_client
logging.basicConfig(filename=config.log_path_server + time.strftime("%Y%m%d") + '.log', level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


def _init_():
    args = sys.argv[1:]
    logging.info(args)
    server_tron = config.All
    server_post = config.Post

    if args[0] == "open_dai":
        handle_client(args[1]+'|open_dai')

    elif args[0] == "Folder":
        handle_client(args[1]+'|Folder')

    elif args[0] == "Ready_render" or args[0] == "Local_render" or args[0] == "Cloud_render":
        handle_client(args[1])

    elif args[0] == "clip1":
        # 修改相应场次的权限
        path = args[1].split('|')[2]
        all_path = server_tron + '/' + path
        os.chmod(all_path, 0777)
        clipData = args[1]+'|clip1'
        handle_client(clipData)

    elif args[0] == "clip2":
        path = args[1].split('|')[1]
        video_dir = os.path.dirname(path)
        all_path = server_tron + '/' + video_dir
        os.chmod(all_path, 0777)
        clipData = args[1]+'|clip2'
        handle_client(clipData)

    elif args[0] == "clip3":
        post_path = server_post + args[1].split('|')[1]
        pack_path = post_path + '/Clip_Pack'
        os.chmod(post_path, 0777)
        if os.path.exists(pack_path):
            shutil.rmtree(pack_path)
            os.mkdir(pack_path, 0755)
        else:
            os.mkdir(pack_path, 0755)
        clipData = args[1]+'|clip3'
        handle_client(clipData)

    elif args[0] == "add_xml":
        # 修改相应场以及场下镜头的权限
        path = args[1].split('|')[2]
        all_path = server_tron + '/' + path
        os.chmod(all_path, 0777)
        ch_li = os.listdir(all_path)
        for i in ch_li:
            os.chmod(all_path+i, 0777)
        clipData = args[1]+'|add_xml'
        handle_client(clipData)

    elif args[0] == "clip_del":     # 'clip_del' '/FUY/001'
        pro_name = os.path.dirname(args[1])
        all_pro = server_tron + pro_name
        all_seq = server_tron + args[1]
        new_path = args[:-3] + '.' + args[-3:]
        new_all_seq = server_tron + new_path
        os.chmod(all_pro,0777)
        os.rename(all_seq,new_all_seq)
        os.chmod(all_pro,0555)
        post_pro = server_post + pro_name
        post_seq = server_post + args[1]
        new_post_seq = server_tron + new_path
        os.chmod(post_pro, 0777)
        os.rename(post_seq, new_post_seq)
        os.chmod(post_pro, 0555)

    elif args[0] == "Project":
        TronProject().CreatePro(args[1].upper())  # createProject.CreatePro("HAC")
        CallBack().callback(args[2])

    elif args[0] == "Dailies1":   # "Dailies1" "/FUY/001/001/Stuff/cmp/" "IP|/FUY/001/001/Stuff/cmp|filename|command_id"
        dai_filename = args[2].split("|")[2]
        TronProject().CreateDai(args[1], dai_filename)
        dailiesData = args[2]+"|Dailies1"
        handle_client(dailiesData)

    elif args[0] == "Dailies2":   # "Dailies1" "/FUY/001/001/Stuff/cmp/" "IP|/FUY/001/001/Stuff/cmp|filename|command_id"
        dai_filename = args[2].split("|")[2]
        TronProject().CreateDai(args[1], dai_filename)
        dailiesData = args[2]+"|Dailies2"
        handle_client(dailiesData)

    elif args[0] == "lgt_dai":   # "lgt_dai" "/FUY/001/001/Stuff/cmp/" "IP|/FUY/001/001/Stuff/cmp|filename|command_id|rate|帧长"
        dai_filename = args[2].split("|")[2]
        TronProject().CreateDai(args[1], dai_filename)
        dailiesData = args[2]+"|lgt_dai"
        handle_client(dailiesData)

    elif args[0] == 'YunFolder':  # "YunFolder" "ip" "filepath|时间戳"  "YunFolder" "192.168.1.33" "/DSN_TXT_8/|1550839953"
        handle_client(args[1] + '|' + args[2] + '|YunFolder')

    elif args[0] == "Del":  # "Del" "{公司_项目_主键id: 时间戳,  公司_项目_主键id: 时间戳}"
        TronDistribute().Deldir(args[1])

    elif args[0] == "Reference":    # "Reference" "HAC" "shots"  "IP|文件夹路径|文件名|sql_data"
        TronProject().CreateRef(args[1].upper(), args[2])
        referencesData = args[3] + "|Reference"
        handle_client(referencesData)

    elif args[0] == "download":  # 'download' 'tron_TXT_7|路径' 'id' 'user_id'
        key, arg2 = args[1].split('|')
        res = AliyunOss('', key, '', '', '', '').download(arg2)
        if res:
            CallBack().callback_download(args[2], args[3])

    elif args[0] == "download_out":  # 'download_out' '[tron_TXT_7, tron_TXT_6]' 'ids' 'user_id' 'ip'
        clipData = args[4] + '|' + args[1] + '|download'
        downloadPath = handle_client(clipData)
        logging.info('download_out path: ' + downloadPath)
        if os.path.exists(downloadPath):
            for fileName in eval(args[1]):
                AliyunOss('', fileName, '', '', '', '').download(downloadPath)
            CallBack().callback_download(args[2], args[3])

    elif args[0] == "Seq":  # createProject.CreateSeq(proName, seqName)
        TronProject().CreateSeq(args[1].upper(), args[2])
        CallBack().callback(args[3])

    elif args[0] == "Shot":   # "Shot" "HAC" "001" "001" "user_name" "command_id"
        # 创建镜头时在all盘创建stuff和work以及prd的文件夹，post盘只创建stuff和work
        TronProject().CreateScene(args[1].upper(), args[2], args[3])
        proPath_all = server_tron + '/' + args[1].upper()
        TronFolder().CreateStuff(proPath_all, args[2], args[3], 'prd', '', args[4])
        all_work = proPath_all + '/' + args[2] + '/' + args[3] + '/Work'
        TronFolder().CreateFolder(all_work, "0555", "")
        post_work = server_post + '/' + args[1].upper()+ '/' + args[2] + '/' + args[3] + '/Work'
        post_stuff = server_post + '/' + args[1].upper()+ '/' + args[2] + '/' + args[3] + '/Stuff'
        TronFolder().CreateFolder(post_work, "0555", "")
        TronFolder().CreateFolder(post_stuff, "0555", "")
        CallBack().callback(args[5])

    elif args[0] == "Pack":  # "Pack" "Json路径" "时间戳" "打包id" "command_id"
        res = TronDistribute().argParse(args[1], args[2])
        if res:
            CallBack().callback_pack(args[3])
            CallBack().callback(args[4])

    elif args[0] == "Transit_out":  # "Transit" "路径" “文件名” "transit_id" 'user_id' “command_id”
        res = transit(args[1], args[2])
        if res:
            CallBack().callback_transit(args[5])
            CallBack().callback_transit_complete(args[3], args[4])

    elif args[0] == "Transit":  # "Transit" "json路径" "transit_id,transit_id1" "user_id" “command_id”
        res = transit(args[1])
        if res:
            CallBack().callback_transit(args[4])
            CallBack().callback_transit_complete(args[2], args[3])

    elif args[0] == "AssetTask":    # "AssetTask" "HAC" "rig" "liangcy" "fileName" "command_id"
        TronProject().CreateAsset(args[1].upper(), args[2], args[3], args[4])
        # CallBack().callback(args[5])
        # args = args[6] + '|' + args[1] + '|' + args[2] + '|' + args[3] + '|' + args[4] + "|AssetTask"
        # handle_client(args)

    elif args[0] == "ShotTask":   # "ShotTask" "HAC" "001" "001" "rig" "liangcy" "fileName" "command_id"
        TronProject().CreateShot(args[1].upper(), args[2], args[3], args[4], args[5], args[6])
        # CallBack().callback(args[7])
        # args = args[8] + '|' + args[1] + '|' + args[2] + '|' + args[3] + '|' + args[4] + '|' + args[5] + '|' + args[6]
        # ShotTaskData = args + "|ShotTask"
        # handle_client(ShotTaskData)


if __name__ == '__main__':
    _init_()
