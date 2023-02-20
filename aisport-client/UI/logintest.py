from PyQt5 import QtGui
from qtpy import QtCore

import login
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
import requests

from PyQt5 import QtCore, QtGui, QtWidgets

class loginMain(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = login.Ui_MainWindow()
        self.ui.setupUi(self)
        self.slot_init()
        self.ui.widget_3.hide()
        self.show()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.isMaximized() == False:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, mouse_event):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(mouse_event.globalPos() - self.m_Position)  # 更改窗口位置
            mouse_event.accept()

    def mouseReleaseEvent(self, mouse_event):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
    def slot_init(self):
        self.ui.pushButton.clicked.connect(self.change_widget3)
        self.ui.pushButton_2.clicked.connect(self.change_widget2)
        self.ui.dengluBT.clicked.connect(self.login)
        self.ui.regestBT.clicked.connect(self.regest)

    def login(self):
        from UI.zhujiemiantest import zhujiemainMain
        try:
            if self.ui.lineEdit.text()=="" or self.ui.lineEdit_2.text() =="":
                ok = QtWidgets.QPushButton()
                # cancel = QtWidgets.QPushButton()
                msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, u'错误提示', u'账号密码为空！')
                msg.addButton(ok, QtWidgets.QMessageBox.ActionRole)
                # msg.addButton(cancel, QtWidgets.QMessageBox.RejectRole)
                ok.setText(u'确定')
                # cancel.setText(u'取消')
                if msg.exec_() == QtWidgets.QMessageBox.RejectRole:
                    self.show()
            else:
                print(11111111111111)
                data = {"username": self.ui.lineEdit.text()}
                url = "http://43.136.75.221:8085/login"
                r = requests.post(url, data)

                if r.json()['username'] == str(self.ui.lineEdit.text()) and r.json()['password'] == str(self.ui.lineEdit_2.text()):
                    self.close()
                    self.zhujiemainMain=zhujiemainMain(self.ui.lineEdit.text())
                    self.zhujiemainMain.show()
                else:
                    self.ui.lineEdit.setText(self.ui.lineEdit.text())
                    self.ui.lineEdit_2.setText("")
                    ok = QtWidgets.QPushButton()
                    # cancel = QtWidgets.QPushButton()
                    msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, u'错误提示', u'输入的密码错误！')
                    msg.addButton(ok, QtWidgets.QMessageBox.ActionRole)
                    # msg.addButton(cancel, QtWidgets.QMessageBox.RejectRole)
                    ok.setText(u'确定')
                    # cancel.setText(u'取消')
                    if msg.exec_() == QtWidgets.QMessageBox.RejectRole:
                        self.ui.lineEdit.setText(self.ui.lineEdit.text())
                        self.ui.lineEdit_2.setText("")
                        self.show()
                    print("账号密码错误")
        except Exception as e:
            ok = QtWidgets.QPushButton()
            # cancel = QtWidgets.QPushButton()
            msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, u'错误提示', u'账号不存在！')
            msg.addButton(ok, QtWidgets.QMessageBox.ActionRole)
            # msg.addButton(cancel, QtWidgets.QMessageBox.RejectRole)
            ok.setText(u'确定')
            # cancel.setText(u'取消')
            if msg.exec_() == QtWidgets.QMessageBox.RejectRole:
                self.ui.lineEdit.setText(self.ui.lineEdit.text())
                self.ui.lineEdit_2.setText("")
                self.show()

    def regest(self):
        from UI.zhujiemiantest import zhujiemainMain
        if self.ui.lineEdit_6.text() == "" or self.ui.lineEdit_7.text() == "" or self.ui.lineEdit_8.text()=="":
            ok = QtWidgets.QPushButton()
            msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, u'错误提示', u'账号密码为空！')
            msg.addButton(ok, QtWidgets.QMessageBox.ActionRole)
            ok.setText(u'确定')
            if msg.exec_() == QtWidgets.QMessageBox.RejectRole:
                self.show()
        else:
            data = {"username": self.ui.lineEdit_6.text(),"password":self.ui.lineEdit_7.text()}
            url = "http://43.136.75.221:8085/regesit"
            r = requests.post(url, data)
            if r.content == b'0':
                ok = QtWidgets.QPushButton()
                # cancel = QtWidgets.QPushButton()
                msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, u'错误提示', u'账号已经存！')
                msg.addButton(ok, QtWidgets.QMessageBox.ActionRole)
                # msg.addButton(cancel, QtWidgets.QMessageBox.RejectRole)
                ok.setText(u'确定')
                # cancel.setText(u'取消')
                if msg.exec_() == QtWidgets.QMessageBox.RejectRole:
                    self.ui.lineEdit_6.setText(self.ui.lineEdit.text())
                    self.ui.lineEdit_7.setText("")
                    self.ui.lineEdit_8.setText("")
                    self.show()
                    self.ui.widget_2.hide()
                    self.ui.widget_3.show()
            else:
                if r.content == b'1':
                    # ok = QtWidgets.QPushButton()
                    # # cancel = QtWidgets.QPushButton()
                    # msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, u'注册成功', u'点击确定跳转到主界面！')
                    # msg.addButton(ok, QtWidgets.QMessageBox.ActionRole)
                    # # msg.addButton(cancel, QtWidgets.QMessageBox.RejectRole)
                    # ok.setText(u'确定')
                    # # cancel.setText(u'取消')
                    # if msg.exec_() == QtWidgets.QMessageBox.RejectRole:
                    self.close()
                    self.zhujiemainMain = zhujiemainMain(self.ui.lineEdit_6.text())
                    self.zhujiemainMain.show()

    def change_widget3(self):
        self.ui.widget_3.hide()
        self.ui.widget_2.show()
    def change_widget2(self):
        self.ui.widget_2.hide()
        self.ui.widget_3.show()
    #


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = loginMain()
    sys.exit(app.exec_())
