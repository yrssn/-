from PyQt5.QtWidgets import QWidget, QApplication,QFileDialog
from Video import Ui_Form
from PyQt5.QtCore import QDir
import cv2 as cv
from PyQt5.QtGui import QPixmap,QImage
import sys
import numpy as np
import cv2 as cv

class QmyWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__ui = Ui_Form()
        self.__ui.setupUi(self)
        self.fileName = ""
        self.cap = False
        self.cap2 = False

    def on_pushButton_1_pressed(self):
        self.cap = cv.VideoCapture(0)
        if not self.cap.isOpened():
            print("Cannot open camera")
            exit()
        while True:
            # Capture frame-by-frame
            ret, frame = self.cap.read()
            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                self.on_pushButton_3_clicked()
                break
            # Our operations on the frame come here
            #gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            # Display the resulting frame
            # cv.imshow('frame', gray)
            # cv.imshow('frame', frame)
            if cv.waitKey(1) == ord('q'):
                break
            img = QImage(frame.data,frame.shape[1],frame.shape[0],3*frame.shape[1],QImage.Format.Format_BGR888) 
            pixmap = QPixmap.fromImage(img)
            # if(pixmap.width()>400):
            #     ratio = pixmap.width()/400
            #     pixmap.setDevicePixelRatio(ratio)
            self.__ui.label_1.setPixmap(pixmap)

    def on_pushButton_2_pressed(self):
        curPath = QDir.currentPath()
        title = "选择视频"
        filt = "视频文件(*.mp4);;所有文件(*.*)"
        self.fileName,flt = QFileDialog.getOpenFileName(self,title,curPath,filt)
        if self.fileName == "":
            return
        self.cap2 = cv.VideoCapture(self.fileName)
        if not self.cap2.isOpened():
            print("Cannot open camera")
            exit()
        while True:
            # Capture frame-by-frame
            ret, frame = self.cap2.read()
            # if frame is read correctly ret is True
            if not ret:
                print("Can't receive frame (stream end?). Exiting ...")
                self.on_pushButton_4_clicked()
                break
            # Our operations on the frame come here
            #gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            # Display the resulting frame
            # cv.imshow('frame', gray)
            # cv.imshow('frame', frame)
            if cv.waitKey(1) == ord('q'):
                break
            img = QImage(frame.data,frame.shape[1],frame.shape[0],3*frame.shape[1],QImage.Format.Format_BGR888) 
            pixmap = QPixmap.fromImage(img)
            # if(pixmap.width()>400):
            #     ratio = pixmap.width()/400
            #     pixmap.setDevicePixelRatio(ratio)
            self.__ui.label_2.setPixmap(pixmap)

    def on_pushButton_3_clicked(self):
        self.__ui.label_1.setText("摄像头已经关闭")
        self.cap.release()

    def on_pushButton_4_clicked(self):
        self.__ui.label_2.setText("视频已经关闭")
        self.cap2.release()
        


if  __name__ == "__main__":
   app = QApplication(sys.argv)   #创建App，用QApplication类
   myWidget=QmyWidget()
   myWidget.show()
   sys.exit(app.exec())     