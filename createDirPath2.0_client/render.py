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

    def render_one(self,inPathFile):
        filepath = QFileDialog.getOpenFileName(self.mainWindow, 'open file', inPathFile)
        return filepath
        sys.exit(self.app.exec_())

    def render_all(self,inPathFile):
        filepath = QFileDialog.getExistingDirectory(self.mainWindow, 'open file', inPathFile)
        return filepath
        sys.exit(self.app.exec_())

    def dataTree(self, filename, filePath):
        file_size = os.path.getsize(filename)
        file_mtime = os.path.getmtime(filename)
        pro_name = filePath.split('/')[1]
        pro_path = os.getcwd()
        csv_path = os.path.join(pro_path, '%s.csv' % pro_name)
        with open(csv_path, 'a+') as f:
            con_write = filePath, file_size, file_mtime
            con_read = set(f.readlines())
            con_write = str(con_write) + '\n'
            if con_write not in con_read:
                f.write(con_write)
            else:
                Remind().remind_ask()
        self.submit(filename, filePath)

    def submit(self, filename, filePath):
        up_name = filename.split('/')[-1]
        file_number = filePath.split('_')[0][-9:]
        ray_py_file = '/Public/test/RVDeadline/start.py'
        cmd = 'deadlinecommand -SubmitCommandLineJob -executable "/usr/bin/python" -arguments "%s -a -u -s <QUOTE>%s<QUOTE>" -chunksize 1 -pool upload_submit_pool -group upload_submit_group -priority 100 -name "%s" -prop MachineLimit=5' % (
        ray_py_file, filename, up_name)
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
