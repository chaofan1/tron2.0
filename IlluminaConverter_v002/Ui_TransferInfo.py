#!/usr/bin/env python2.6
#-*- coding: utf-8 -*-

# Filename: Ui_TransferInfo.py
# Author: XueFeng, Xiangquan
# Created: 2012/07/02/ 13:00
# Latest Modified: 2013/01/08/ 13:00
# Platform: Windows7
# Copyright: Illumina ltd, PTD department, 2012


from PyQt4.QtGui import *
from PyQt4.QtCore import *

from customComboGrp import CustomComboGrp
from customDirLineEdit import CustomDirLineEdit
from config import Config

class Ui_TransferInfo(QFrame):
    """
    Create UI and Main Function.
    """
    def __init__(self, parent = None):
        """Initialize Buttons and PushDown Buttons."""
        super(Ui_TransferInfo, self).__init__(parent)
        
        self.setObjectName("Converter Widget")
        
        self.vboxLayout = QVBoxLayout(self)
        self.vboxLayout.setContentsMargins(5, 2, 5, 2)
        self.vboxLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        self.setCombos()
        self.setInputElems()
        self.setTimecodeInput()
        #self.setOutputElems()
        
    def setCombos(self):
        """ """
        self.comboHLayout = QHBoxLayout()
        self.comboHLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.vboxLayout.addLayout(self.comboHLayout)
        # Resolution ComboBox
        self.resCombo = CustomComboGrp('icon', Config.resolutionIcon, QSize(28, 28), QSize(100, 24), self)
        self.resCombo.resize(140, 28)
        self.resCombo.addItem("HD")
        self.resCombo.addItem("Original")
        self.resCombo.addItem("Half")
        self.resCombo.setStyleSheet('color:rgb(220,220,220)')
        self.comboHLayout.addWidget(self.resCombo)
        
        # Frame ComboBox
        self.fpsCombo = CustomComboGrp('icon', Config.frameIcon, QSize(28, 28), QSize(100, 24), self)
        self.fpsCombo.addItem("24")
        self.fpsCombo.addItem("25")
        self.fpsCombo.addItem("30")
        self.fpsCombo.setStyleSheet('color:rgb(220,220,220)')
        self.comboHLayout.addWidget(self.fpsCombo)
        
        #Opacity
        self.maskOpc = CustomComboGrp('icon', Config.maskIcon, QSize(28, 28), QSize(100, 24), self)
        self.maskOpc.addItem('Full Mask')
        self.maskOpc.addItem('Half Mask')
        self.maskOpc.addItem('No Mask')
        self.maskOpc.setStyleSheet('color:rgb(220,220,220)')
        self.comboHLayout.addWidget(self.maskOpc)
        
        #Quality or vcodec
        self.vcodec = CustomComboGrp('icon', Config.videoIcon, QSize(28, 28), QSize(100, 24), self)
        self.vcodec.addItem('h264')
        self.vcodec.addItem('mjpeg')
        self.vcodec.addItem('lossless')
        self.vcodec.setStyleSheet('color:rgb(220,220,220)')
        self.comboHLayout.addWidget(self.vcodec)
        
        #Double inputs checkbox
        self.doubleInput = QCheckBox(' Left/Right Imgs', self)
        self.doubleInput.setStyleSheet('color:rgb(220,220,220)')
        self.doubleInput.setCheckState(Config.doubleInput)
        self.doubleInput.setTristate(False)
        self.comboHLayout.addWidget(self.doubleInput)
        
        #Draw Slate
        self.drawSlate = QCheckBox(' Draw Slate', self)
        self.drawSlate.setStyleSheet('color:rgb(220,220,220)')
        self.drawSlate.setCheckState(Config.drawSlate)
        self.drawSlate.setTristate(False)
        self.comboHLayout.addWidget(self.drawSlate)
        
        #Draw Watermark
        self.drawWatermark = QCheckBox(' Draw Watermark', self)
        self.drawWatermark.setCheckState(Config.drawWatermark)
        self.drawWatermark.setTristate(True)
        self.drawWatermark.setStyleSheet('color:rgb(220,220,220)')
        self.comboHLayout.addWidget(self.drawWatermark)
        
        #Run
        self.run  = QPushButton('runBtn', self)
        self.run.setFixedSize(QSize(56, 28))
        self.run.setStyleSheet('color:rgb(247,148,30)')
        self.comboHLayout.addWidget(self.run)
        

    def setInputElems(self):
        """ """
        self.inputVLayout = QVBoxLayout()
        self.inputVLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.vboxLayout.addLayout(self.inputVLayout)
        
        self.input = CustomDirLineEdit(Config.outputIcon, QSize(28, 28), QSize(700, 28), 'input', self)
        self.input.setText('Input Path')
        self.input.setStyleSheet('color:rgb(220,220,220)')
        self.inputVLayout.addWidget(self.input)
        
        self.input2 = CustomDirLineEdit(Config.outputIcon, QSize(28, 28), QSize(700, 28), 'input', self)
        self.input2.setText('Input Path 2')
        self.input2.setStyleSheet('color:rgb(220,220,220)')
        self.inputVLayout.addWidget(self.input2)

        self.input2.setEnabled(False)
        
    def setTimecodeInput(self):
        """ """
        self.tcHLayout = QHBoxLayout()
        self.tcHLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.vboxLayout.addLayout(self.tcHLayout)
        
        self.dpxtc = CustomDirLineEdit(Config.outputIcon, QSize(28, 28), QSize(700, 28), 'dpx', self)
        self.dpxtc.setText('DPX Path')
        self.dpxtc.setStyleSheet('color:rgb(220,220,220)')
        self.tcHLayout.addWidget(self.dpxtc)
'''
    def setOutputElems(self):
        """ """

        self.outputHLayout = QHBoxLayout()
        self.outputHLayout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.vboxLayout.addLayout(self.outputHLayout)

        self.output =  CustomDirLineEdit(Config.outputIcon, QSize(28, 28), QSize(700, 28), 'output', self)
        self.output.setText('Output Path')
        self.outputHLayout.addWidget(self.output)
'''