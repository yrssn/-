import sys
import time
import cv2
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
import threading
from UI import guofenshiandshe



class guofenshiandsheMain(QMainWindow):
    def __init__(self,username,sportname,shipingdizhi):
        super().__init__()
        self.ui=guofenshiandshe.Ui_MainWindow()
        self.ui.setupUi(self)
        self.username=username
        self.sportname=sportname
        self.shipingdizhi=shipingdizhi
        self.ui.label_2.setText(str(self.username))
        self.ui.label_3.setText(str("当前运动为："+self.sportname))
        self.starTime=0
        self.endTime=0
        self.timer_camera=QtCore.QTimer()
        self.timer_camera1=QtCore.QTimer()
        self.cap =cv2.VideoCapture()
        self.cap1=cv2.VideoCapture()
        self.CAM_NUM=0
        self.slot_init()
        self.show()
    def slot_init(self):
        self.timer_camera.timeout.connect(self.show_camera)
        self.timer_camera1.timeout.connect(self.show_vedio)
        self.ui.fanhui.clicked.connect(self.close)
        self.ui.openshiping.clicked.connect(self.openshiping)
        self.ui.openshiandshe.clicked.connect(self.openshiandshe)
        self.ui.openshexiangtou.clicked.connect(self.openshexiangtou)

    def openshiping(self):
        if self.timer_camera1.isActive() == False:
            flag = self.cap1.open(str(self.shipingdizhi))
            if flag == False:
                msg = QtWidgets.QMessageBox.Warning(self, u'Warning', u'请检测相机与电脑是否连接正确',
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)
            else:
                self.timer_camera1.start(300)
                self.ui.openshiping.setText(u'关闭视频')
        else:
            self.timer_camera1.stop()
            self.cap1.release()
            self.ui.label_5.clear()
            self.ui.openshiping.setText(u'打开视频')

    def openshiandshe(self):
        pass
    def openshexiangtou(self):
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(self.CAM_NUM)
            if flag == False:
                msg = QtWidgets.QMessageBox.Warning(self, u'Warning', u'请检测相机与电脑是否连接正确',
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)
            else:
                self.timer_camera.start(500)
                self.ui.openshexiangtou.setText(u'关闭摄像头')
        else:
            self.timer_camera.stop()
            self.cap.release()
            self.ui.label_6.clear()
            self.ui.openshexiangtou.setText(u'打开摄像头')

    def show_vedio(self):
        self.cap1 = cv2.VideoCapture(str(self.shipingdizhi))
        while True:
            success, self.input_frame = self.cap1.read()
            if not success:
                break
            self.input_frame=cv2.resize(self.input_frame,(760, 760))
            self.input_frame = cv2.cvtColor(self.input_frame, cv2.COLOR_BGR2RGB)
            showImage = QtGui.QImage(self.input_frame.data, self.input_frame.shape[1], self.input_frame.shape[0],
                                     QtGui.QImage.Format_RGB888)
            self.ui.label_5.setPixmap(QtGui.QPixmap.fromImage(showImage))
            # time.sleep(5)
            if cv2.waitKey(1) in [ord('q'), 27]:  # 按键盘上的q或esc退出（在英文输入法下）
                 break
    def show_camera(self):
        self.cap=cv2.VideoCapture(self.CAM_NUM)
        # video_n_frame= self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        self.cap.open(0)
        while self.cap.isOpened():
            success,self.input_frame1 =self.cap.read()
            if not success:
                break
            input_frame1=cv2.resize(input_frame1,(470, 750))
            input_frame1=cv2.cvtColor(input_frame1,cv2.COLOR_BGR2RGB)
            showImage = QtGui.QImage(self.input_frame1.data, self.input_frame1.shape[1],self.input_frame1.shape[0],
                                     QtGui.QImage.Format_RGB888)
            self.ui.label_6.setPixmap(QtGui.QPixmap.fromImage(showImage))
            if cv2.waitKey(1) in [ord('q'), 27]:  # 按键盘上的q或esc退出（在英文输入法下）
                break
    def closeEvent(self, event):
        ok = QtWidgets.QPushButton()
        cancel = QtWidgets.QPushButton()
        msg = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, u'关闭', u'是否关闭！')
        msg.addButton(ok, QtWidgets.QMessageBox.ActionRole)
        msg.addButton(cancel, QtWidgets.QMessageBox.RejectRole)
        ok.setText(u'确定')
        cancel.setText(u'取消')
        if msg.exec_() == QtWidgets.QMessageBox.RejectRole:
            event.ignore()
        else:
            from UI.zhujiemiantest import zhujiemainMain
            self.zjm=zhujiemainMain(self.username)
            self.zjm.show()
            self.zjm.ui.widget_5.show()
            if self.cap.isOpened():
                self.cap.release()
            if self.cap1.isOpened():
                self.cap1.release()
            if self.timer_camera.isActive():
                self.timer_camera.stop()
            if self.timer_camera1.isActive():
                self.timer_camera1.stop()
            event.accept()

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




# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     win = guofenshiandsheMain(11,"11",11)
#     win.show()
#     sys.exit(app.exec_())
