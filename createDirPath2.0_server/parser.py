# !/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# 服务器
#"Project" "HAC" "command_id"
#"Seq" "HAC" "01" "command_id"
#"Shot" "HAC" "01" "001" "command_id"
#"AssetTask" "HAC" "rig" "liangcy" "fileName" "command_id"
#"Pack" "Json路径" "pack_id" "command_id"
#"Transit" "json路径" “公司_项目_主键id”"transit_id"“command_id”
#"Del" "公司_项目_主键id"
# 客户端
# 'Render' '192.168.100.44|/FUY/999/003/Stuff/lgt/publish/fuy999003_lgt_wangcf_yuanBao_master|Render2|command_id'
# "open_dai" "192.168.1.85|/DHG/Dailies/20161214"
# "open_ref" "192.168.1.85|/DHG/Dailies/20161214"
# "open_post" "192.168.1.85|/DHG/Dailies/20161214"
# "YunFolder" "192.168.1.85|/DHG/Dailies/20161214"
# 'download' 'tron_TXT_7|ip'
# 服务器与客户端
# "Excel" "192.168.1.85" "文件路径" "目标路径"
# old "Dailies2" "HAC" "fileName" "192.168.1.85|x:/DHG/Dailies/20161214|dhg01001_prd_liangcy_HFG_v0103|373"
# new "Dailies1" "/FUY/001/001/stuff/cmp" "192.168.1.85|/FUY/001/001/stuff/cmp|ruy001004_cmp_xiecy_weqw_v0101|command_id"
# "Dailies2" "/FUY/001/001/stuff/cmp" "192.168.1.85|/FUY/001/001/stuff/cmp|filename|command_id"
# "Reference" "HAC" "shots"  "192.168.1.85|/RUY/assets|1537848665|5"
# "ShotTask" "HAC" "01" "001" "rig" "liangcy" "fileName" "command_id"
# 剪辑线
# 'clip1' '192.168.100.79|YLSL/009/Work/note/5bdff7943d5b3.xml|YLSL/009/|10|35|27|332'
# 转码 'clip1' 'IP|user_id|path|项目id|场id|xml_id|command_id'
# 追加 'add_xml' 'IP|xml_path|path|项目id|场id|xml_id|command_id'
#              192.168.101.160|TXT/017/Work/note/5bffaf4e5c992.xml|TXT/017/|1|46|22
# 回插 'clip2' 'IP|video_path|img_path|frame|id|command_id'
# 打包 'clip3'  'IP|FUY/001|command_id'


import shutil
import sys, os, re
from createProject import TronProject
from client import clientLink
from server_callback import CallBack
from distribution import TronDistribute,transit
from aliyun import AliyunOss


def _init_():
	args = sys.argv[1:]
	print args
	if len(args) == 2:
		if args[0] == "open_dai":
			clientLink(args[1]+'|open_dai')
		elif args[0] == "open_ref":
			clientLink(args[1]+'|open_ref')
		elif args[0] == "open_post":
			clientLink(args[1]+'|open_post')
		elif args[0] == "Ready_render" or args[0] == "Local_render" or args[0] == "Cloud_render":
			clientLink(args[1])
		elif args[0] == "clip1":
			# 修改相应场次的权限
			path = args[1].split('|')[2]
			all_path = '/Tron' + '/' + path
			os.chmod(all_path, 0777)
			clipData = args[1]+'|clip1'
			clientLink(clipData)
		elif args[0] == "clip2":
			path = args[1].split('|')[1]
			video_dir = os.path.dirname(path)
			all_path = '/Tron' + '/' + video_dir
			os.chmod(all_path, 0777)
			clipData = args[1]+'|clip2'
			clientLink(clipData)
		elif args[0] == "clip3":
			post_path = '/Post/' + args[1].split('|')[1]
			pack_path = post_path + '/Clip_Pack'
			os.chmod(post_path, 0777)
			if os.path.exists(pack_path):
				shutil.rmtree(pack_path)
			else:
				os.mkdir(pack_path, 0755)
			clipData = args[1]+'|clip3'
			clientLink(clipData)
		elif args[0] == "add_xml":
			# 修改相应场以及场下镜头的权限
			path = args[1].split('|')[2]
			all_path = '/Tron/'+path
			os.chmod(all_path, 0777)
			ch_li = os.listdir(all_path)
			for i in ch_li:
				os.chmod(all_path+i, 0777)
			clipData = args[1]+'|add_xml'
			clientLink(clipData)
	elif len(args) == 3:
		if args[0] == "Project":
			TronProject().CreatePro(args[1].upper())  # createProject.CreatePro("HAC")
			CallBack().callback(args[2])
		elif args[0] == "Dailies1":  # "Dailies1" "/FUY/001/001/Stuff/cmp/" "IP|/FUY/001/001/Stuff/cmp|filename|command_id"
			TronProject().CreateDai(args[1])
			dailiesData = args[2]+"|Dailies1"
			clientLink(dailiesData)
		elif args[0] == 'YunFolder':
			clientLink(args[1] + '|'+ args[2] + '|YunFolder')
		elif args[0] == "Dailies2":  # "Dailies2" "/FUY/001/001/Stuff/cmp/" "IP|/FUY/001/001/Stuff/cmp|filename|command_id"
			TronProject().CreateDai(args[1])
			dailiesData = args[2]+"|Dailies2"
			clientLink(dailiesData)
		elif args[0] == "Del":  # "Del" "公司_项目_主键id" "时间戳"
			TronDistribute().Deldir(args[1], args[2])
	elif len(args) == 4:
		if args[0] == "Reference":    # "Reference" "HAC" "shots"  "192.168.1.85|x:/DHG/References/inner/fileName|373"
			TronProject().CreateRef(args[1].upper(), args[2])
			referencesData = args[3] + "|Reference"
			clientLink(referencesData)
		elif args[0] == "download":  # 'download' 'tron_TXT_7|ip' 'id' 'user_id'
			key, arg2 = args[1].split('|')
			downloadPath = arg2
			res = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
			if res.match(arg2):
				clipData = arg2 + '|' + key + '|download'
				downloadPath = clientLink(clipData)
			AliyunOss('', key, '', '', '', '').download(downloadPath)
			CallBack().callback_download(args[2], args[3])
		elif args[0] == "Seq":  # createProject.CreateSeq(proName, seqName)
			TronProject().CreateSeq(args[1].upper(), args[2])
			CallBack().callback(args[3])
	elif len(args) == 5:
		if args[0] == "Shot":   # "Shot" "HAC" "001" "001" "command_id"
			TronProject().CreateScene(args[1].upper(), args[2], args[3])
			CallBack().callback(args[4])
		elif args[0] == "Transit":  # "Transit" "json路径" “公司_项目_主键id” "transit_id" “command_id”
			transit(args[1], args[2])
			CallBack().callback_transit(args[4])
			CallBack().callback(args[3])
		elif args[0] == "Pack":  # "Pack" "Json路径" "时间戳" "打包id" "command_id"
			TronDistribute().argParse(args[1], args[2])
			CallBack().callback_pack(args[3])
			CallBack().callback(args[4])
	elif len(args) == 6:
		if args[0] == "AssetTask":    # "AssetTask" "HAC" "rig" "liangcy" "fileName" "command_id"
			TronProject().CreateAsset(args[1].upper(), args[2], args[3], args[4])
			CallBack().callback(args[5])
	elif len(args) == 9:
		if args[0] == "ShotTask":   # "ShotTask" "HAC" "01" "001" "rig" "liangcy" "fileName" "command_id" "ip"
			TronProject().CreateShot(args[1].upper(), args[2], args[3], args[4], args[5], args[6])
			args = args[8] + '|' + args[1] + '|' + args[2] + '|' + args[3] + '|' + args[4] + '|' + args[5] + '|' + args[6]
			ShotTaskData = args + "|ShotTask"
			clientLink(ShotTaskData)
			CallBack().callback(args[7])


if __name__ == '__main__':
	_init_()
