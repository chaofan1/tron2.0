# coding:utf8

import sys
import os
import subprocess
from PyQt4.QtGui import *
from remind import Remind
reload(sys)
sys.setdefaultencoding('utf-8')


class Select:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.mainWindow = QMainWindow()

    def select_one(self, inPathFile):
        file_path = QFileDialog.getOpenFileName(self.mainWindow, 'open file', inPathFile).toUtf8()
        return file_path
        sys.exit(self.app.exec_())

    def select_dir(self, inPathFile):
        file_path = QFileDialog.getExistingDirectory(self.mainWindow, 'open file', inPathFile).toUtf8()
        return file_path
        sys.exit(self.app.exec_())


class Render:
    def __init__(self, file_name, file_path):
        self.file_name = file_name
        self.file_path = file_path
        self.ray_py_file = '/Public/test/RVDeadline/start.py'

    def dataTree(self):
        file_size = os.path.getsize(self.file_name)
        file_mtime = os.path.getmtime(self.file_name)
        pro_name = self.file_path.split('/')[1]
        pro_path = os.getcwd()
        csv_path = os.path.join(pro_path, '%s.csv' % pro_name)
        with open(csv_path, 'a+') as f:
            con_write = self.file_path, file_size, file_mtime
            con_read = set(f.readlines())
            con_write = str(con_write) + '\n'
            if con_write not in con_read:
                f.write(con_write)
            else:
                Remind().remind_ask()

    def submit(self, Uptask):
        self.dataTree()
        up_name = self.file_name.split('/')[-1]
        file_number = self.file_path.split('_')[0][-9:]
        if Uptask == 'Ready_render1' or Uptask == 'Ready_render2':
            cmd = 'export PATH=/Public/Support/Thinkbox/Deadline8/bin:$PATH && deadlinecommand -SubmitCommandLineJob -executable "/usr/bin/python" -arguments "%s -r -q <QUOTE>%s<QUOTE>" -chunksize 1 -priority 100 -name "%s" -prop MachineLimit=5' % (
                self.ray_py_file, self.file_name, up_name)
        elif Uptask == 'Local_render1' or Uptask == 'Local_render2':
            cmd = 'export PATH=/Public/Support/Thinkbox/Deadline8/bin:$PATH && deadlinecommand -SubmitCommandLineJob -executable "/usr/bin/python" -arguments "%s -r <QUOTE>%s<QUOTE>" -chunksize 1 -priority 100 -name "%s" -prop MachineLimit=5' % (
                self.ray_py_file, self.file_name, up_name)
        elif Uptask == 'Cloud_render1' or Uptask == 'Cloud_render2':
            cmd = 'export PATH=/Public/Support/Thinkbox/Deadline8/bin:$PATH && deadlinecommand -SubmitCommandLineJob -executable "/usr/bin/python" -arguments "%s -a -u -s <QUOTE>%s<QUOTE>" -chunksize 1 -pool upload_submit_pool -group upload_submit_group -priority 100 -name "%s" -prop MachineLimit=5' % (
                self.ray_py_file, self.file_name, up_name)
        popen_cmd = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        Remind().remind_start(file_number)
        while True:
            line = popen_cmd.stdout.readline()
            line = line.strip()
            if not line == '':
                print line
                if 'successfully' in line:
                    Remind().remind_success(file_number)
                else:
                    Remind().remind_fail(line, file_number)
            if line == '' and popen_cmd.poll() != None:
                break

# cmd = 'export PATH=/Public/Support/Thinkbox/Deadline8/bin:$PATH && deadlinecommand -SubmitCommandLineJob -executable "/usr/bin/python" -arguments "%s -r -q <QUOTE>%s<QUOTE>" -chunksize 1 -priority 100 -name "%s" -prop MachineLimit=5' % (
# cmd = 'export PATH=/Public/Support/Thinkbox/Deadline8/bin:$PATH && deadlinecommand -SubmitCommandLineJob -executable "/usr/bin/python" -arguments "%s -r <QUOTE>%s<QUOTE>" -chunksize 1 -priority 100 -name "%s" -prop MachineLimit=5' % (
# cmd = 'export PATH=/Public/Support/Thinkbox/Deadline8/bin:$PATH && deadlinecommand -SubmitCommandLineJob -executable "/usr/bin/python" -arguments "%s -a -u -s <QUOTE>%s<QUOTE>" -chunksize 1 -pool upload_submit_pool -group upload_submit_group -priority 100 -name "%s" -prop MachineLimit=5' % (
