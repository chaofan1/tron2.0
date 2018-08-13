#!/usr/bin/env python2.6
#-*- coding: utf-8 -*-

# Filename: Ui_Layout.py
# Author: Xiangquan
# Created: 2013/04/24/
# Latest Modified: 2013/04/24/
# Platform: Ubuntu10.04
# Copyright: Illumina ltd, PTD department, 2012

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from Ui_TransferInfo import Ui_TransferInfo

from Ui_LeftArea import Ui_LeftArea
#from Ui_RightArea import Ui_RightArea

from config import Config

class Ui_Layout(object):
    """Main Window Setting .
    Connect Ui_SettingBtns and Set Main Window Parameters.
    """
    def setupUi(self, mainWindow):
        """Set Main Window Parameters ."""
        mainWindow.setObjectName("Converter V002")
        mainWindow.setWindowIcon(QIcon(Config.xIcon))
        mainWindow.setWindowTitle("Converter V002")
        mainWindow.centralwidget = QWidget(mainWindow)
        mainWindow.setCentralWidget(mainWindow.centralwidget)

        #add main contents
        mainWindow.verticalLayout = QVBoxLayout(mainWindow.centralwidget)
        mainWindow.verticalLayout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        mainWindow.verticalLayout.setContentsMargins(0, 0, 0, 0)
        mainWindow.verticalLayout.setSpacing(0)
        self.__setLogoIcon__(mainWindow)
        self.__setSplitterArea__(mainWindow)
        self.setCentralWidget(mainWindow.centralwidget) 
        self.statusbar = QStatusBar(mainWindow.centralwidget)
        self.statusbar.showMessage(Config.winStart)
        mainWindow.verticalLayout.addWidget(self.statusbar)
        self.retranslateUi()
        
    def retranslateUi(self):
        self.setWindowTitle(QApplication.translate('self', 'Tron Converter', None, QApplication.UnicodeUTF8))
        
    def __setLogoIcon__(self, mainWindow):
        """ Setup Logo Icon"""
        hlayout = QHBoxLayout()
        hlayout.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        mainWindow.verticalLayout.addLayout(hlayout)
        
        # Logo Icon
        self.logo = QToolButton(mainWindow)
        self.logo.setIconSize(QSize(1172, 60))
        self.logo.setStyleSheet("background-image:url(%s);background-repeat: repeat-n" % Config.logoBG)
        self.logo.setEnabled(False)
        hlayout.addWidget(self.logo)
        
    def __setSplitterArea__(self, mainWindow):
        """ """
        self.splitter = QSplitter(mainWindow)
        self.splitter.setOrientation(Qt.Horizontal) 
        self.splitter.setHandleWidth(5)
        self.splitter.setStretchFactor(0, 1)
        self.splitter.setStretchFactor(1, 1)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        mainWindow.verticalLayout.addWidget(self.splitter)
        
        #create & add left area
        self.leftArea = Ui_LeftArea(mainWindow)
        self.splitter.addWidget(self.leftArea)
        
#        #create & add right area
#        self.rightArea = Ui_RightArea(mainWindow)
#        self.splitter.addWidget(self.rightArea)
        
        
if __name__ == "__main__":
    Ui_Layout()

    
