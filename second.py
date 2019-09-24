# -*- coding: utf-8 -*-
 
# Form implementation generated from reading ui file 'second.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
 
from PyQt5 import QtCore, QtGui, QtWidgets
 
class Ui_Second(object):
    def initUI(self, Ui_Second):
        mainLayout = QtWidgets.QVBoxLayout()
        #self.verticalLayoutR.setSpacing(0)
        Frame = QtWidgets.QFrame(self)
        Frame.setStyleSheet('''
            QFrame{border-style:solid;border-width:2;border-color:red;;background-color:yellow}
            QLabel{border-style:none;}
            ''')
        #self.exitFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        #self.exitFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        frameLayout = QtWidgets.QVBoxLayout(Frame)
        exitBtn = QtWidgets.QPushButton("Exit", Frame)
        label = QtWidgets.QLabel('This is 222', Frame)
        frameLayout.addWidget(exitBtn)
        frameLayout.addWidget(label)
        mainLayout.addWidget(Frame)
        mainLayout.setContentsMargins(0,0,0,0)
        self.setLayout(mainLayout)
 