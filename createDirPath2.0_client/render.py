# coding:utf8

import sys
import os
import subprocess
from PyQt4.QtGui import *
from remind import Remind


class Render:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.mainWindow = QMainWindow()

    def render_one(self, inPathFile):
        file_path = QFileDialog.getOpenFileName(self.mainWindow, 'open file', inPathFile)
        return file_path
        sys.exit(self.app.exec_())

    def render_all(self, inPathFile):
        file_path = QFileDialog.getExistingDirectory(self.mainWindow, 'open file', inPathFile)
        return file_path
        sys.exit(self.app.exec_())

    def dataTree(self, file_name, file_path):
        file_size = os.path.getsize(file_name)
        file_mtime = os.path.getmtime(file_name)
        pro_name = file_path.split('/')[1]
        pro_path = os.getcwd()
        csv_path = os.path.join(pro_path, '%s.csv' % pro_name)
        with open(csv_path, 'a+') as f:
            con_write = file_path, file_size, file_mtime
            con_read = set(f.readlines())
            con_write = str(con_write) + '\n'
            if con_write not in con_read:
                f.write(con_write)
            else:
                Remind().remind_ask()
        self.submit(file_name, file_path)

    def submit(self, file_name, file_path):
        up_name = file_name.split('/')[-1]
        file_number = file_path.split('_')[0][-9:]
        ray_py_file = '/Public/test/RVDeadline/start.py'
        cmd = 'deadlinecommand -SubmitCommandLineJob -executable "/usr/bin/python" -arguments "%s -a -u -s <QUOTE>%s<QUOTE>" -chunksize 1 -pool upload_submit_pool -group upload_submit_group -priority 100 -name "%s" -prop MachineLimit=5' % (
        ray_py_file, file_name, up_name)
        popen_cmd = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        Remind().remind_start(file_number)
        popen_cmd.wait()
        while True:
            line = popen_cmd.stdout.readline()
            line = line.strip()
            if not line == '':
                print line
                if 'The job was submitted successfully' in line:
                    Remind().remind_success(file_number)
                else:
                    Remind().remind_fail(line, file_number)
            if line == '' and popen_cmd.poll() != None:
                break


if __name__ == '__main__':
    p = Render().render_all('')
    print p
    p2 = Render().render_one('')
    print p2
