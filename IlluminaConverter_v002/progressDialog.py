#!/usr/bin/env python2.6
#-*- coding: utf-8 -*-

# Filename: progressDialog.py
# Author: XueFeng
# Created: 2012/07/02/ 13:00
# Latest Modified: 2012/07/04/ 13:00
# Platform: Ubuntu10.04
# Copyright: Illumina ltd, PTD department, 2012

from PyQt4 import QtCore, QtGui


class ProgressDialog(QtGui.QProgressDialog):
    """Progress Dialog Class."""
    def __init__(self, parent=None):
        """Initialize Progress Dialog Parameters ."""
        super(ProgressDialog, self).__init__(parent)
        self.children()[3].hide()       #hide the cancel button
        self.setFixedSize(QtCore.QSize(500, 80))
        self.setAutoClose(True)
        self.setWindowTitle("Waiting")
        self.setLabelText('Converting')
        self.setRange(0, 0)
        self.setMinimumDuration(1)
        
