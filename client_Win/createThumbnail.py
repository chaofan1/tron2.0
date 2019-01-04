#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# 创建视频的缩略图

import cv2

class CreateThumbnail:
    pass

def run(fileName, filePath):  # filename.mov, /Volumes/All/FUY/stuff/dmt/mov/filename
    thumbPicName = fileName.split(".")[0] + ".jpg"   # filename.jpg
    img_path = filePath+"/."+thumbPicName    # /Volumes/All/FUY/stuff/dmt/mov/filename/.filename.jpg
    video_path = filePath+"/"+fileName
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


if __name__ == '__main__':
    cd = "dhf001004_ani_lixue_wet_v0101.mp4", r"C:\Users\Public\Videos\Sample Videos"
    run(cd[0], cd[1])


