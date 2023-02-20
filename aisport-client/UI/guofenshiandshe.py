# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'guofenshiandshe.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(3147, 840)
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(50, 10, 1401, 781))
        self.widget.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"")
        self.widget.setObjectName("widget")
        self.widget_4 = QtWidgets.QWidget(self.widget)
        self.widget_4.setGeometry(QtCore.QRect(1300, 0, 101, 41))
        self.widget_4.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_4)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.suoxiao = QtWidgets.QPushButton(self.widget_4)
        self.suoxiao.setStyleSheet("#suoxiao{\n"
"    border:none;\n"
"}\n"
"#suoxiao:focus{\n"
"    \n"
"    \n"
"    color: rgb(158, 158, 158);\n"
"}")
        self.suoxiao.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/disexpend.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.suoxiao.setIcon(icon)
        self.suoxiao.setObjectName("suoxiao")
        self.horizontalLayout.addWidget(self.suoxiao)
        self.line_2 = QtWidgets.QFrame(self.widget_4)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout.addWidget(self.line_2)
        self.cha = QtWidgets.QPushButton(self.widget_4)
        self.cha.setStyleSheet("#cha{\n"
"    border:none;\n"
"}\n"
"#cha:focus{\n"
"    \n"
"    \n"
"    color: rgb(158, 158, 158);\n"
"}")
        self.cha.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cha.setIcon(icon1)
        self.cha.setObjectName("cha")
        self.horizontalLayout.addWidget(self.cha)
        self.widget_5 = QtWidgets.QWidget(self.widget)
        self.widget_5.setGeometry(QtCore.QRect(1230, 240, 161, 361))
        self.widget_5.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.widget_5.setObjectName("widget_5")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_5)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.openshiping = QtWidgets.QPushButton(self.widget_5)
        self.openshiping.setStyleSheet("#openshiping{\n"
"    border:none;\n"
"}\n"
"#openshiping:focus{\n"
"    \n"
"    \n"
"    color: rgb(158, 158, 158);\n"
"}")
        self.openshiping.setObjectName("openshiping")
        self.verticalLayout.addWidget(self.openshiping)
        self.line_6 = QtWidgets.QFrame(self.widget_5)
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.verticalLayout.addWidget(self.line_6)
        self.openshexiangtou = QtWidgets.QPushButton(self.widget_5)
        self.openshexiangtou.setStyleSheet("#openshexiangtou{\n"
"    border:none;\n"
"}\n"
"#openshexiangtou:focus{\n"
"    \n"
"    \n"
"    color: rgb(158, 158, 158);\n"
"}")
        self.openshexiangtou.setObjectName("openshexiangtou")
        self.verticalLayout.addWidget(self.openshexiangtou)
        self.line_3 = QtWidgets.QFrame(self.widget_5)
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.verticalLayout.addWidget(self.line_3)
        self.openshiandshe = QtWidgets.QPushButton(self.widget_5)
        self.openshiandshe.setStyleSheet("#openshiandshe{\n"
"    border:none;\n"
"}\n"
"#openshiandshe:focus{\n"
"    \n"
"    \n"
"    color: rgb(158, 158, 158);\n"
"}")
        self.openshiandshe.setObjectName("openshiandshe")
        self.verticalLayout.addWidget(self.openshiandshe)
        self.line_5 = QtWidgets.QFrame(self.widget_5)
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.verticalLayout.addWidget(self.line_5)
        self.fanhui = QtWidgets.QPushButton(self.widget_5)
        self.fanhui.setStyleSheet("#fanhui{\n"
"    border:none;\n"
"}\n"
"#fanhui:focus{\n"
"    \n"
"    \n"
"    color: rgb(158, 158, 158);\n"
"}")
        self.fanhui.setObjectName("fanhui")
        self.verticalLayout.addWidget(self.fanhui)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(1250, 140, 72, 15))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(1320, 140, 72, 15))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(440, 10, 191, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setGeometry(QtCore.QRect(10, 10, 1201, 761))
        self.widget_2.setStyleSheet("background-color: rgb(198, 198, 198);")
        self.widget_2.setObjectName("widget_2")
        self.label_5 = QtWidgets.QLabel(self.widget_2)
        self.label_5.setGeometry(QtCore.QRect(2, 1, 771, 761))
        self.label_5.setStyleSheet("background-color: rgb(13, 13, 13);")
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.widget_2)
        self.label_6.setGeometry(QtCore.QRect(770, 1, 431, 761))
        self.label_6.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 3147, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.cha.clicked.connect(MainWindow.close)
        self.suoxiao.clicked.connect(MainWindow.showMinimized)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.openshiping.setText(_translate("MainWindow", "打开视频"))
        self.openshexiangtou.setText(_translate("MainWindow", "打开摄像头"))
        self.openshiandshe.setText(_translate("MainWindow", "合并打开"))
        self.fanhui.setText(_translate("MainWindow", "返回"))
        self.label.setText(_translate("MainWindow", "用户名："))
        self.label_2.setText(_translate("MainWindow", "TextLabel"))

import resource_rc
