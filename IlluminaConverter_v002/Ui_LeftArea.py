#!/usr/bin/env python2.6
#-*- coding: utf-8 -*-

# Filename: Ui_LeftArea.py
# Author: Xiangquan
# Created: 2013/04/24/
# Latest Modified: 2013/04/24/
# Platform: Ubuntu10.04
# Copyright: Illumina ltd, PTD department, 2012

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from Ui_TransferInfo import Ui_TransferInfo
from Ui_PreviewPainter import Ui_PreviewPainter


class Ui_LeftArea(QFrame):
    def __init__(self, parent = None):
        """ """
        super(Ui_LeftArea, self). __init__(parent)
        
        self.vLayout = QVBoxLayout(self)
        self.vLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        self.__setTransferInfo__()
        self.__setPainter__()
        
    def __setTransferInfo__(self):
        """Connect Ui_TransferInfo Setting ."""
        self.transferInfo = Ui_TransferInfo(self)
        self.vLayout.addWidget(self.transferInfo)
        
    def __setPainter__(self):
        """Connect Ui_PreviewPainter """
        self.painter = Ui_PreviewPainter(self)
        self.vLayout.addWidget(self.painter)
        
        
        
    
