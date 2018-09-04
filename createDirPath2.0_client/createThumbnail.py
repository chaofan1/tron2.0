#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
#创建视频的缩略图
# Filename: createThumbnail.py

import cv2
import os


def run(fileName, filePath):  # filename.mov, /FUY/stuff/dmt/mov/filename
    thumbPicName = fileName.split(".")[0] + ".jpg"   # filename.jpg
    if 'mov' in filePath:
        filePath_img = filePath.replace('mov', 'img')
    img_path = os.path.join(filePath_img, thumbPicName)
    video_path = os.path.join(filePath, fileName)
    video = cv2.VideoCapture(video_path)
    count_frame = video.get(cv2.CAP_PROP_FRAME_COUNT)
    if count_frame < 5:
        if video.isOpened():
            rval, frame = video.read()
            cv2.imwrite(img_path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 40])
    else:
        c = 1
        while video.isOpened():
            rval, frame = video.read()
            if c == 5:
                cv2.imwrite(img_path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 40])
                break
            c += 1

    video.release()
    return img_path


if __name__ == '__main__':
    cd = "1.avi", r"C:\Users\wangcf\Desktop\job\job\job_test"
    run(cd[0], cd[1])


