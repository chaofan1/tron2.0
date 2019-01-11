#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# 创建视频的缩略图

import cv2
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def run(video_path):
    video_path_split = video_path.split('\\')
    fileName = video_path_split[-1]
    filePath = '\\'.join(video_path_split[0:-1])
    thumbPicName = fileName.split(".")[0] + ".jpg"
    img_path = filePath+"/."+thumbPicName    # /Volumes/All/FUY/stuff/dmt/mov/filename/.filename.jpg
    print 'video_path', video_path
    print 'img_path', img_path
    video = cv2.VideoCapture(video_path)
    if video.isOpened():
        rval, frame = video.read()
        cv2.imwrite(img_path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 40])
        print 'create thm'
    else:
        print 'Fail to open!'
    video.release()
    return img_path
