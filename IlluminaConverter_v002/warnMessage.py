#!/usr/bin/env python2.6
#-*- coding: utf-8 -*-

# Filename: warnMessage.py
# Author: XueFeng
# Created: 2012/07/02/ 13:00
# Latest Modified: 2012/07/04/ 13:00
# Platform: Windows7
# Copyright: Illumina ltd, PTD department, 2012

from PyQt4 import QtGui


class WarnMesg(QtGui.QWidget):
    def __init__(self, parent=None):
        super(WarnMesg, self).__init__(parent)
        self.parent = parent
    """
    QtGui.QMessageBox For Pop-up Dialog .
    Dialog prompts user types of warning .
    """
    def warnOneDir(self):
        """Need One Folder Images to Convert ."""
        QtGui.QMessageBox.warning(self.parent, "Warning", self.tr("At Least One Folder To Convert ."))
        
    def warnOutpath(self):
        """Need Select Out Put Path ."""
        QtGui.QMessageBox.warning(self.parent, "Warning", self.tr("Choose Output Path Directory ."))
        
    def warnFile(self):
        """This Folder is Invalid .
        For Example Prefix is Inconsistent or Postfix not jpg/tif/tga ."""
        QtGui.QMessageBox.warning(self.parent, "Warning", self.tr("This Directory is invalid ."))
        
    def warnRepeat(self):
        """New ConvertPath is Repeat ."""
        QtGui.QMessageBox.warning(self.parent, "Warning", self.tr("This Directory is Repeat ."))
        
    def finish(self):
        """Finish Convert Mov ."""
        QtGui.QMessageBox.information(self.parent, "Finish", self.tr("Congratulations!\nThe conversion was completed successfully ."))
        
