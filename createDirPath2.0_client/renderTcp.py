import os
import subprocess


def render(data,conn):
    print '...'
    print 'Intall mappings before anything ...'
    cmd_list = ['touch /var/lock/subsys/local','mount -t nfs 192.168.100.99:/export/All /All','mount -t nfs 192.168.100.99:/export/Public /Public','mount -t nfs 192.168.100.100:/export/Post /Post','mount -t nfs 192.168.100.99:/export/Dailies /Dailies','mount -t nfs 192.168.101.100:/vol/ILLUMINAFX /illuminafx','mount -t nfs 192.168.101.100:/vol/Library /Library']
    for cmd in cmd_list:
        try:
            print 'cmd:',cmd
            cmd_handle = subprocess.Popen(cmd, shell=True)
            cmd_handle.wait()
        except Exception as e:
            print e
    print '...'
    print 'Anaylzing incomming info ...'
    filePath = data.split("|")[0].strip().replace("\0",'')
    if filePath.startswith('J:'):
        print 'Convert to linux path ...'
        filePath = filePath.replace("J:","/Post")
    filePath = filePath.strip()
    print filePath
    if os.path.exists(filePath):
        print "File %s looking good, redirect to rVAUS process ..." % filePath
        cmd = 'sudo python /rayvision/rVAUS.py %s ' % filePath
        popen_cmd = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        while True:
            line = popen_cmd.stdout.readline()
            line = line.strip()
            if line == '' and popen_cmd.poll() != None:
                break
            if not line == '':
                print line
                if 'rayvision transmitter init failure' in line:
                    try:
                        conn.send(line)
                    except:
                        pass
                    else:
                        conn.close()
                elif 'upload file interrupt' in line:
                    try:
                        conn.send(line)
                    except:
                        pass
                    else:
                        conn.close()
                elif 'upload file fail ' in line:
                    try:
                        conn.send(line)
                    except:
                        pass
                    else:
                        conn.close()
                elif '[ERROR]' in line:
                    try:
                        conn.send(line)
                    except:
                        pass
                    else:
                        conn.close()
                elif 'Submit sucess, task_id' in line:
                    try:
                        conn.send(line)
                    except:
                        pass
                    else:
                        conn.close()
                else:
                    continue
    else:
        print "%s NOT a regular file or directory!!!" % filePath


'''
upload file progress (/Post/FUY/064/109/Work/baijm/hip/fuy064109_lgt_baijm_QiongCang_workshop/render02/fuy064109_lgt_baijm_yuanBaoMsk_v0102.hip) upload speed: 1504.89KB/S, progress: 99.0475%
upload file done (/Post/FUY/064/109/Work/baijm/hip/fuy064109_lgt_baijm_QiongCang_workshop/render02/fuy064109_lgt_baijm_yuanBaoMsk_v0102.hip)
recv disconnect response from transmit server
upload task success: all files are success
rayvision transmitter exit begin
rayvision transmitter exit end

[ERROR]: The scene path does not exist. Please upload it first

recv disconnect response from transmit server

upload file done (/All/SHH/033/549/Stuff/efx/publish/shh033549_efx_yuchao_tusixiang_master/geo/v01/smoke/smoke1/smoke1.106.bgeo.sc)
upload task success: all files are success
Upload success, start submitting ...
'''