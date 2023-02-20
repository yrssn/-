# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1484, 796)
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(70, 90, 501, 481))
        self.label.setStyleSheet("background-image: url(:/images/images/724.png);\n"
"border-top-left-radius:30px;\n"
"border-bottom-left-radius:30px;")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(570, 90, 441, 481))
        self.label_2.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"border-top-right-radius:30px;\n"
"border-bottom-right-radius:30px;")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(670, 160, 215, 50))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("#pushButton{\n"
"    border:none;\n"
"}\n"
"#pushButton:focus{\n"
"    color: rgb(186, 186, 186);\n"
"}")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.line = QtWidgets.QFrame(self.widget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("#pushButton_2{\n"
"    border:none;\n"
"}\n"
"#pushButton_2:focus{\n"
"    color: rgb(186, 186, 186);\n"
"}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setGeometry(QtCore.QRect(580, 220, 381, 341))
        self.widget_2.setObjectName("widget_2")
        self.lineEdit = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit.setGeometry(QtCore.QRect(20, 50, 341, 61))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("border:1px solid rgb(0,0,0);\n"
"border-radius:8px;")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 140, 341, 61))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet("border:1px solid rgb(0,0,0);\n"
"border-radius:8px;")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.dengluBT = QtWidgets.QPushButton(self.widget_2)
        self.dengluBT.setGeometry(QtCore.QRect(20, 260, 341, 51))
        self.dengluBT.setStyleSheet("#dengluBT{\n"
"    background-color: rgb(0, 0, 0);\n"
"    color: rgb(255, 255, 255);\n"
"    border:3px solid rgb(0,0,0);\n"
"    border-radius:8px;\n"
"}\n"
"#dengluBT:hover{\n"
"    background-color: rgb(255, 255, 255);\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"#dengluBT:pressed{\n"
"    padding-top:5px;\n"
"    padding-left:5px;\n"
"}")
        self.dengluBT.setObjectName("dengluBT")
        self.checkBox = QtWidgets.QCheckBox(self.widget_2)
        self.checkBox.setGeometry(QtCore.QRect(20, 220, 81, 16))
        self.checkBox.setObjectName("checkBox")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(930, 110, 41, 31))
        self.pushButton_4.setStyleSheet("border:none;")
        self.pushButton_4.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_4.setIcon(icon)
        self.pushButton_4.setObjectName("pushButton_4")
        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.widget_3.setGeometry(QtCore.QRect(580, 210, 381, 341))
        self.widget_3.setObjectName("widget_3")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.widget_3)
        self.lineEdit_6.setGeometry(QtCore.QRect(20, 40, 341, 61))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEdit_6.setFont(font)
        self.lineEdit_6.setStyleSheet("border:1px solid rgb(0,0,0);\n"
"border-radius:8px;")
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.widget_3)
        self.lineEdit_7.setGeometry(QtCore.QRect(20, 120, 341, 61))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEdit_7.setFont(font)
        self.lineEdit_7.setStyleSheet("border:1px solid rgb(0,0,0);\n"
"border-radius:8px;")
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.lineEdit_8 = QtWidgets.QLineEdit(self.widget_3)
        self.lineEdit_8.setGeometry(QtCore.QRect(20, 200, 341, 61))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.lineEdit_8.setFont(font)
        self.lineEdit_8.setStyleSheet("border:1px solid rgb(0,0,0);\n"
"border-radius:8px;")
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.regestBT = QtWidgets.QPushButton(self.widget_3)
        self.regestBT.setGeometry(QtCore.QRect(20, 280, 341, 51))
        self.regestBT.setStyleSheet("#regestBT{\n"
"    background-color: rgb(0, 0, 0);\n"
"    color: rgb(255, 255, 255);\n"
"    border:3px solid rgb(0,0,0);\n"
"    border-radius:8px;\n"
"}\n"
"#regestBT:hover{\n"
"    background-color: rgb(255, 255, 255);\n"
"    color: rgb(0, 0, 0);\n"
"}\n"
"#regestBT:pressed{\n"
"    padding-top:5px;\n"
"    padding-left:5px;\n"
"}")
        self.regestBT.setObjectName("regestBT")
        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(880, 110, 41, 31))
        self.pushButton_5.setStyleSheet("border:none;")
        self.pushButton_5.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/disexpend.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_5.setIcon(icon1)
        self.pushButton_5.setObjectName("pushButton_5")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.pushButton_4.clicked.connect(MainWindow.close)
        self.pushButton_5.clicked.connect(MainWindow.showMinimized)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "登录"))
        self.pushButton_2.setText(_translate("MainWindow", "注册"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "账号："))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "密码："))
        self.dengluBT.setText(_translate("MainWindow", "登录"))
        self.checkBox.setText(_translate("MainWindow", "记住"))
        self.lineEdit_6.setPlaceholderText(_translate("MainWindow", "输入账号："))
        self.lineEdit_7.setPlaceholderText(_translate("MainWindow", "设置密码："))
        self.lineEdit_8.setPlaceholderText(_translate("MainWindow", "确认密码："))
        self.regestBT.setText(_translate("MainWindow", "注册"))

import resource_rc
