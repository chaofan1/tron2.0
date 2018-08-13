#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
#创建视频的缩略图
# Filename: createThumbnail.py

import cv2


def run(fileName, filePath):
    thumbPicName = fileName.split(".")[0] + ".jpg"
    a = filePath.split('/')[:-2]
    a.append('img')
    filePath_img = '/'.join(a)
    img_path = filePath_img + '/' + thumbPicName
    video = cv2.VideoCapture(filePath+"/"+fileName)
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


