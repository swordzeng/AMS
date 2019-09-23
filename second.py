# -*- coding: utf-8 -*-
 
# Form implementation generated from reading ui file 'second.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
 
from PyQt5 import QtCore, QtGui, QtWidgets
 
class Ui_Second(object):
    def initUI(self, Ui_Second):
        
        hLayout = QtWidgets.QHBoxLayout()
        label = QtWidgets.QLabel('This is form 2222')
        hLayout.addWidget(label)
        frame = QtWidgets.QFrame()
        hLayout.addWidget(frame)
        hLayout.setContentsMargins(0, 0, 0, 0) 
 
        self.setLayout(hLayout)
 