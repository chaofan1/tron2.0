#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
# 服务器
#"Project" "HAC" "command_id"
#"Seq" "HAC" "01" "command_id"
#"Shot" "HAC" "01" "001" "command_id"
#"AssetTask" "HAC" "rig" "liangcy" "fileName" "command_id"
#"ShotTask" "HAC" "01" "001" "rig" "liangcy" "fileName" "command_id"
# 客户端
#'Render' '192.168.100.44|/FUY/999/003/Stuff/lgt/publish/fuy999003_lgt_wangcf_yuanBao_master|Render2|command_id'
#"Folder" "192.168.1.85|/DHG/Dailies/20161214"
# 服务器与客户端
#old "Dailies2" "HAC" "fileName" "192.168.1.85|x:/DHG/Dailies/20161214|dhg01001_prd_liangcy_HFG_v0103|373"
#new "Dailies1" "/FUY/001/001/stuff/cmp" "192.168.1.85|FUY/001/001/stuff/cmp|filename|command_id"
#    "Dailies2" "/FUY/001/001/stuff/cmp" "192.168.1.85|FUY/001/001/stuff/cmp|filename|command_id"
#"Reference" "HAC" "shots"  "192.168.1.85|x:/DHG/References/inner/fileName|373"
# 剪辑线
#'clip1' '127.0.0.1|HZG/001/work/note/2aa.xml|FUY/001/|7|60|20|44'
#转码 'clip1' 'IP|user_id|path|项目id|场id|xml_id|command_id'
#追加 'add_xml' 'IP|xml_path|path|项目id|场id|xml_id|command_id'
#回插 'clip2' 'IP|video_path|img_path|time|rate|id|command_id'
#打包 'clip3'  'IP|FUY/001|xml_path|command_id'


import sys,os
from createProject import TronProject
from client import clientLink
from server_callback import callback
from distribution import TronDistribute, delCloud


def _init_():
	args = sys.argv[1:]
	print args
	if len(args) > 8:
		print 'error: please check your create project'
	elif len(args) == 2:
		if args[0] == "Folder":
			clientLink(args[1])
		elif args[0] == "Render":
			clientLink(args[1])
		elif args[0] == "clip1":
			# 修改相应场次的权限
			path = args[1].split('|')[2]
			all_path = '/Tron' + '/' + path
			os.chmod(all_path, 0777)
			clipData = args[1]+'|clip1'
			clientLink(clipData)
		elif args[0] == "clip2":
			clipData = args[1]+'|clip2'
			clientLink(clipData)
		elif args[0] == "clip3":
			clipData = args[1]+'|clip3'
			clientLink(clipData)
		elif args[0] == "add_xml":
			# 修改相应场以及场下镜头的权限
			path = args[1].split('|')[2]
			all_path = '/Tron'+'/'+path
			os.chmod(all_path, 0777)
			ch_li = os.listdir(all_path)
			for i in ch_li:
				os.chmod(all_path+i, 0777)
			clipData = args[1]+'|add_xml'
			clientLink(clipData)
		elif args[0] == "download":
			clipData = args[1]+'|download'
			clientLink(clipData)
		elif args[0] == "DelCloud":
			delCloud(args[1])
	elif len(args) == 3:
		if args[0] == "Project":
			TronProject().CreatePro(args[1])  # createProject.CreatePro("Project","HAC","command_id")
			callback(args[2])
		elif args[0] == "Dailies1":  # "Dailies1" "FUY/001/001/stuff/cmp/" "IP|FUY/001/001/stuff/cmp|filename|command_id"
			TronProject().CreateDai(args[1])
			dailiesData = args[2]+"|Dailies1"
			clientLink(dailiesData)
		elif args[0] == "Dailies2":  # "Dailies2" "FUY/001/001/stuff/cmp/" "IP|FUY/001/001/stuff/cmp|filename|command_id"
			TronProject().CreateDai(args[1])
			dailiesData = args[2]+"|Dailies2"
			clientLink(dailiesData)
		elif args[0] == "Pack":
			TronDistribute(args[2]).argParse(args[1])
	elif len(args) == 4:
		if args[0] == "Reference":    # "Reference" "HAC" "shots"  "192.168.1.85|x:/DHG/References/inner/fileName|373"
			TronProject().CreateRef(args[1], args[2])
			referencesData = args[3] + "|Reference"
			clientLink(referencesData)
		elif args[0] == "Seq":  # createProject.CreateSeq("Seq","HAC","01","command_id")
			TronProject().CreateSeq(args[1], args[2])
			callback(args[3])
	elif len(args) == 5:
		if args[0] == "Shot":   # "Shot" "HAC" "001" "001" "command_id"
			TronProject().CreateScene(args[1], args[2], args[3])
			callback(args[4])
	elif len(args) == 6:
		if args[0] == "AssetTask":    # "AssetTask" "HAC" "rig" "liangcy" "fileName" "command_id"
			TronProject().CreateAsset(args[1], args[2], args[3], args[4])
			callback(args[5])
	elif len(args) == 8:
		if args[0] == "ShotTask":   # "ShotTask" "HAC" "01" "001" "rig" "liangcy" "fileName" "command_id"
			TronProject().CreateShot(args[1], args[2], args[3], args[4], args[5], args[6])
			callback(args[7])


if __name__ == '__main__':
	_init_()
