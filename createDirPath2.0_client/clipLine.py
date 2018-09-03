# coding:utf8
import xml.etree.cElementTree as et
from urllib import unquote
import os
from multiprocessing import Manager,Pool
import subprocess
import pymysql
import urllib,urllib2
import time
import re


ip = '127.0.0.1'
user_name = 'root'
passwd = 'Root123'
db_name = 'new_tron'
table_name = 'oa_shot'


def write_sql(info,shot_video_path,shot_image,shot_number):
    # 002、将数据(镜头帧长,范围,缩略图路径......)写入数据库
    try:
        conn = pymysql.connect(ip, user_name, passwd, db_name, charset='utf8', use_unicode=True)
    except:
        print('connect fail')
    else:
        cursor = conn.cursor()

        project_id = info.get('project_id') # 所属项目ID
        field_id = info.get('field_id')  # 场号ID
        clip_frame_length = info.get('clip_frame_length')  # 镜头帧长=剪辑帧长
        frame_range = info.get('frame_range')  # 帧数范围
        material_number = info.get('material_number')  # 素材号
        create_time = info.get('create_time')  # 创建时间
        change_speed_info = info.get('change_speed_info')   # 变速信息
        material_frame_length = info.get('material_frame_length')   # 素材帧长
        time_start = info.get('time_start')  # 开始时间
        duration = info.get('duration')   # 持续时间
        shot_video_path = re.search(r'.*(uploads.*)', shot_video_path).group(1)
        shot_image = re.search(r'.*(uploads.*)', shot_image).group(1)

        width = info.get('width')  # char
        height = info.get('height')

        insert_sql = "insert ignore into oa_shot(project_id,field_id,shot_image,shot_number,shot_name," \
                     "shot_video_path,clip_frame_length,frame_range,change_speed_info,material_number," \
                     "create_time,time_start,duration,material_frame_length,width,height) " \
                     "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(insert_sql, (project_id,field_id,shot_image,shot_number,shot_number,
                                    shot_video_path,clip_frame_length,frame_range,change_speed_info,
                                    material_number,create_time,time_start,duration,
                                    material_frame_length,width,height))
        conn.commit()
        cursor.close()
        conn.close()


def to_php(queue_len,qsize,project_id,field_id,xml_id,task):
    url = 'http://tron.com/clips/set_progress'
    all_task = float(queue_len)
    done = float(queue_len - qsize)
    percentage = int((done / all_task) * 100)
    query_args = {}
    if task == 'clip1' or task == 'add_xml':
        query_args = {'percentage': percentage,'project_id':project_id,'field_id':field_id, 'xml_id':xml_id}
    elif task == 'pack':
        query_args = {'percentage': percentage, 'name': 'pack'}
    encoded_args = urllib.urlencode(query_args)
    print(encoded_args)
    try:
        print('start get')
        a = urllib2.urlopen(url=url,data=encoded_args)
        print(a.read())
    except urllib2.HTTPError, e:
        print e.code
    except urllib2.URLError, e:
        print e.reason
    except Exception as e:
        print(e)


def getter(task_queue,queue_len,xml_id,task):
    try:
        info = task_queue.get(True,1)
        qsize = task_queue.qsize()
    except Exception as e:
        print(e)
    else:
        # 传递百分比给php
        project_id = info['project_id']  # 所属项目ID
        field_id = info['field_id']  # 场号ID
        if qsize>0:
            to_php(queue_len, qsize, project_id, field_id, xml_id,task)

        dirname = info['dirname']
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        # 视频转码
        pathurl = info['pathurl']
        video_name = pathurl.split('/')[-1]
        video_path = os.path.join(dirname,video_name)
        transcode_command = 'ffmpeg -i %s -loglevel -8 -c:v libx264 -y -g 2 -keyint_min 2 %s'%(pathurl,video_path)
        video_su = subprocess.Popen(transcode_command,shell=True)
        video_su.wait()

        # 2、创建缩略图文件夹,截取缩略图
        img_name = video_name.split('.')[0] +'.jpg'
        img_path = os.path.join(dirname,img_name)
        screenshot_command = 'ffmpeg -ss 1 -t 1 -i %s -loglevel -8 -y %s' % (video_path,img_path)
        img_su = subprocess.Popen(screenshot_command, shell=True)
        img_su.wait()

        # 002、写入数据库
        shot_number = info['shot_number']
        write_sql(info,video_path,img_path,shot_number)


def putter(task_queue,xml_path,project_id,field_id,data,path,task):
    # 1、获取所有需要的信息
    tree = et.ElementTree(file=xml_path)
    number = 1
    time_node = 0
    for i in tree.findall('.//clipitem'):
        info = {}
        try:
            pathurl = i.find('.//pathurl').text
        except Exception as e:
            print(e)
        else:
            if pathurl.endswith('mov'):
                if pathurl.startswith('file://localhost'):
                    pathurl = pathurl.replace('file://localhost', '')
                if os.path.exists(pathurl):
                    start = i.find('start').text
                    end = i.find('end').text
                    width = i.find('.//width').text
                    height = i.find('.//height').text
                    info['width'] = width
                    info['height'] = height
                    material_frame_length = int(end)-int(start)
                    frame_range = start+','+end
                    material_number = ''
                    if '_' in pathurl:
                        material_number = pathurl.split('_')[1]
                    pathurl = unquote(pathurl)
                    # 持续时间
                    rate = i.find('.//timebase').text
                    clip_frame_length = i.find('duration').text   # 镜头帧长=剪辑帧长
                    duration = int(round(float(clip_frame_length) / float(rate)))
                    time_start = time_node
                    time_node += duration
                    info['time_start'] = time_start  # 开始时间
                    info['duration'] = duration   # 持续时间

                    info['pathurl'] = pathurl       # 本地视频地址
                    info['project_id'] = project_id  # 所属项目ID
                    info['field_id'] = field_id     # 场号ID
                    info['clip_frame_length'] = clip_frame_length    # 镜头帧长=剪辑帧长
                    info['frame_range'] = frame_range              # 帧数范围
                    info['material_number'] = material_number  # 素材号
                    info['create_time'] = int(time.time())     # 创建时间
                    info['change_speed_info'] = ''  # 变速信息
                    try:
                        change_speed_info = i.find('.//parameter/value').text
                    except:
                        pass
                    else:
                        info['change_speed_info'] = change_speed_info  # 变速信息
                    info['material_frame_length'] = material_frame_length   # 素材帧长
                    shot_number = str('%03d' % number)
                    dirname = os.path.join(path, shot_number)
                    info['dirname'] = dirname
                    info['shot_number'] = shot_number

                    # 追加xml,根据镜头帧长和帧数范围判断视频是否经过修改,若涉及中间插入,文件夹依次加1,镜头号发生变化,数据库要相应更新
                    if task == 'add_xml' and (clip_frame_length,frame_range) not in data:
                        if os.path.exists(dirname) and os.listdir(dirname):
                            file_li = sorted([i for i in os.listdir(path) if not i.startswith('.')])
                            ind = file_li.index(shot_number)
                            rename_li = file_li[ind:]   # 要重命名的以镜头号为文件夹名的列表
                            # 循环之前连接数据库
                            conn = pymysql.connect(ip, user_name, passwd, db_name, charset='utf8', use_unicode=True)
                            cursor = conn.cursor()

                            for x in range(len(rename_li)):
                                i = rename_li.pop()
                                shot_number_new = '%03d' % (int(i) + 1)
                                dirname_new = os.path.join(path, shot_number_new)  # /Users/shids/Code/tron/uploads/Projects/FUY/001/003
                                dirname_old = os.path.join(path, i)
                                video_img_li = os.listdir(dirname_old)
                                os.rename(dirname_old, dirname_new)  # 为文件夹重命名

                                # 文件夹依次加1以后,要更新的字段:镜头编号shot_number、镜头缩略图地址shot_image、视频路径shot_video_path
                                video_name = [i for i in video_img_li if not i.endswith('jpg')][0]
                                # video_name = m[0].split('/')[-1]
                                img_name = video_name.split('.')[0] + '.jpg'
                                video_path_new_all = os.path.join(dirname_new, video_name) # 新的视频路径
                                img_path_new_all = os.path.join(dirname_new, img_name)     # 新的缩略图路径
                                shot_video_path_new = re.search(r'.*(uploads.*)', video_path_new_all).group(1)
                                shot_image_new = re.search(r'.*(uploads.*)', img_path_new_all).group(1)
                                update_sql = "update oa_shot set shot_number=%s,shot_video_path='%s',shot_image='%s' " \
                                             "where project_id=%s and field_id=%s and shot_number=%s"\
                                             %(shot_number_new,shot_video_path_new,shot_image_new,project_id,field_id,i)
                                try:
                                    cursor.execute(update_sql)
                                    conn.commit()
                                except:
                                    conn.rollback()
                            cursor.close()
                            conn.close()
                        task_queue.put(info)
                    elif task == 'clip1':
                        task_queue.put(info)
                    number += 1

    return task_queue.qsize()


def start_clip(xml_path,path,project_id,field_id,xml_id,task):
    print('start xml')
    if not os.path.exists(path):
        os.makedirs(path)
    queue = Manager().Queue()
    data = set()
    if task == 'add_xml':
        data = select_data(project_id,field_id)
    queue_len = putter(queue,xml_path,project_id,field_id,data,path,task)
    if queue_len:
        pool = Pool(processes=8)
        for i in range(queue_len):
            pool.apply_async(getter, (queue,queue_len,xml_id,task))
        print('queue len:',queue_len)
        pool.close()
        pool.join()
        print('pool join')
    else:
        to_php(1, 0, project_id,field_id,xml_id, task)
        print '没有在xml中获取到任务'


def select_data(project_id,field_id):
    try:
        conn = pymysql.connect(ip, user_name, passwd, db_name, charset='utf8', use_unicode=True)
    except:
        print('connect fail')
    else:
        cursor = conn.cursor()
        select_sql = "select clip_frame_length,frame_range from %s where project_id=%s and field_id=%s" % (table_name, project_id,field_id)
        cursor.execute(select_sql)
        result = set(cursor.fetchall())
        conn.close()
        return result
