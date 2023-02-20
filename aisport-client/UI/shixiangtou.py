# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'shexiangtou.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(976, 654)
        self.widget_2 = QtWidgets.QWidget(Form)
        self.widget_2.setGeometry(QtCore.QRect(0, 0, 981, 651))
        self.widget_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.widget_2.setObjectName("widget_2")
        self.widget = QtWidgets.QWidget(self.widget_2)
        self.widget.setGeometry(QtCore.QRect(10, 140, 141, 351))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.shexiangtouBT = QtWidgets.QPushButton(self.widget)
        self.shexiangtouBT.setObjectName("shexiangtouBT")
        self.verticalLayout.addWidget(self.shexiangtouBT)
        self.tuichuBT = QtWidgets.QPushButton(self.widget)
        self.tuichuBT.setStyleSheet("")
        self.tuichuBT.setObjectName("tuichuBT")
        self.verticalLayout.addWidget(self.tuichuBT)
        self.tuichuBT_2 = QtWidgets.QPushButton(self.widget)
        self.tuichuBT_2.setStyleSheet("")
        self.tuichuBT_2.setObjectName("tuichuBT_2")
        self.verticalLayout.addWidget(self.tuichuBT_2)
        self.label = QtWidgets.QLabel(self.widget_2)
        self.label.setGeometry(QtCore.QRect(150, -10, 821, 661))
        self.label.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.widget_2)
        self.label_2.setGeometry(QtCore.QRect(0, 40, 61, 16))
        self.label_2.setObjectName("label_2")
        self.yonghuminglb = QtWidgets.QLabel(self.widget_2)
        self.yonghuminglb.setGeometry(QtCore.QRect(70, 40, 72, 15))
        self.yonghuminglb.setText("")
        self.yonghuminglb.setObjectName("yonghuminglb")
        self.label_3 = QtWidgets.QLabel(self.widget_2)
        self.label_3.setGeometry(QtCore.QRect(380, 20, 131, 31))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.widget_2)
        self.label_4.setGeometry(QtCore.QRect(540, 20, 131, 31))
        self.label_4.setObjectName("label_4")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.shexiangtouBT.setText(_translate("Form", "打开摄像头"))
        self.tuichuBT.setText(_translate("Form", "退出"))
        self.tuichuBT_2.setText(_translate("Form", "保存数据"))
        self.label_2.setText(_translate("Form", "用户名："))
        self.label_3.setText(_translate("Form", "当前运动项目为："))
        self.label_4.setText(_translate("Form", "TextLabel"))

import resource_rc
