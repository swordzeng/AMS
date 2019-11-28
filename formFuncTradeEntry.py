# -*- coding: utf-8 -*-

import sys 
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_funcTradeEntry(object):
    def initUI(self, Ui_funcTradeEntry):
        mainLayout = QtWidgets.QVBoxLayout()
        #self.verticalLayoutR.setSpacing(0)
        Frame = QtWidgets.QFrame()
        Frame.setStyleSheet('''
            QFrame{border-style:solid;border-width:2;border-color:red;}
            QLabel{border-style:none;}
            ''')
        #self.exitFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        #self.exitFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        frameLayout = QtWidgets.QVBoxLayout(Frame)
        exitBtn = QtWidgets.QPushButton("Exit")
        label = QtWidgets.QLabel('This is 222')
        frameLayout.addWidget(exitBtn)
        frameLayout.addWidget(label)

        hLayout = QtWidgets.QHBoxLayout()
        label11 = QtWidgets.QLabel('111')
        label22 = QtWidgets.QLabel('222')
        hLayout.addWidget(label11)
        hLayout.addWidget(label22)
        frameLayout.addLayout(hLayout)

        frameLayout.addStretch(1)

        label33 = QtWidgets.QLabel('333')
        frameLayout.addWidget(label33)

        mainLayout.addWidget(Frame)
        mainLayout.setContentsMargins(0,0,0,0)
        self.setLayout(mainLayout)
