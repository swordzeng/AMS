# -*- coding: utf-8 -*-
 
# Form implementation generated from reading ui file 'first.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!
 
from PyQt5 import QtCore, QtGui, QtWidgets
 
 
class Ui_First(object):
    def initUI(self, Ui_First):
        
        self.resize(800, 600)
        hLayout = QtWidgets.QHBoxLayout(Ui_First)
        
        label = QtWidgets.QLabel('This is form 1')
        hLayout.addWidget(label)