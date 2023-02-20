import sys

from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

from UI.shexiangtou import Ui_Form
# from UI.zhujiemiantest import zhujiemainMain

from Utils.EMADictSmoothing import EMADictSmoothing
from Utils.FullBodyPoseEmbedder import FullBodyPoseEmbedder
from Utils.PoseClassificationVisualizer import PoseClassificationVisualizer
from Utils.PoseClassifier import PoseClassifier
from Utils.RepetitionCounter import RepetitionCounter
import time
import json

import requests
import numpy as np
from mediapipe.python.solutions import pose as mp_pose
import cv2
from mediapipe.python.solutions import drawing_utils as mp_drawing




class shixiangtouMain(QtWidgets.QWidget):
    def __init__(self,pose_samples_folder,class_name,username,sportName):
        super().__init__()
        self.pose_samples_folder=pose_samples_folder
        self.class_name=class_name
        self.sportName=sportName
        self.username=username
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.timer_camera = QtCore.QTimer()

        self.cap = cv2.VideoCapture()
        self.CAM_NUM = 0
        self.count = 0
        self.time = 0
        self.startTime = 0
        self.endtime = 0
        self.pTime = 0
        self.ui.yonghuminglb.setText(self.username)
        self.ui.label_4.setText(self.sportName)
        self.slots_init()


    def slots_init(self):
        self.ui.shexiangtouBT.clicked.connect(self.button_open_camera_click)
        self.ui.tuichuBT.clicked.connect(self.close)
        self.timer_camera.timeout.connect(self.show_camera)
        self.ui.tuichuBT_2.clicked.connect(self.add_count_and_time)




    def button_open_camera_click(self):
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(self.CAM_NUM)
            if flag == False:
                msg = QtWidgets.QMessageBox.Warning(self, u'Warning', u'请检测相机与电脑是否连接正确',
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)
            else:
                self.timer_camera.start(30)
                self.ui.shexiangtouBT.setText(u'关闭相机')
        else:
            self.endtime = time.time()
            print(int(self.endtime-self.startTime))
            self.timer_camera.stop()
            self.cap.release()
            self.ui.label.clear()
            self.ui.shexiangtouBT.setText(u'打开相机')


    def show_camera(self):
        # flag, self.input_frame = self.cap.read()
        self.cap = cv2.VideoCapture(0)
        video_n_frames = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
        # 初始化跟踪器。
        pose_tracker = mp_pose.Pose(upper_body_only=False)
        # 始化嵌入器。
        pose_embedder = FullBodyPoseEmbedder()

        # 初始化分类器。
        # 检查您使用的参数是否与引导期间相同。
        pose_classifier = PoseClassifier(
            pose_samples_folder=self.pose_samples_folder,
            pose_embedder=pose_embedder,
            top_n_by_max_distance=30,
            top_n_by_mean_distance=10)

        # 初始化 EMA 平滑。
        pose_classification_filter = EMADictSmoothing(
            window_size=10,
            alpha=0.2)
        # 初始化计数器。
        repetition_counter = RepetitionCounter(
            class_name=self.class_name,
            enter_threshold=6,
            exit_threshold=4)

        # 初始化渲染器。
        pose_classification_visualizer = PoseClassificationVisualizer(
            class_name=self.class_name,
            plot_x_max=video_n_frames,
            # 如果它与 `top_n_by_mean_distance` 相同，图形看起来会更好。
            plot_y_max=10)
        self.cap.open(0)
        pTime = 0
        self.startTime = time.time()
        while self.cap.isOpened():
            # 获取视频的下一帧。
            success, self.input_frame = self.cap.read()
            if not success:
                break
            # 运行姿势跟踪器。
            input_frame = cv2.cvtColor(self.input_frame, cv2.COLOR_BGR2RGB)
            result = pose_tracker.process(image=input_frame)
            pose_landmarks = result.pose_landmarks

            # 绘制姿势预测。
            self.output_frame = self.input_frame.copy()
            if pose_landmarks is not None:
                mp_drawing.draw_landmarks(
                    image=self.output_frame,
                    landmark_list=pose_landmarks,
                    connections=mp_pose.POSE_CONNECTIONS)

            if pose_landmarks is not None:
                # 取地标。
                frame_height, frame_width = self.output_frame.shape[0], self.output_frame.shape[1]
                pose_landmarks = np.array([[lmk.x * frame_width, lmk.y * frame_height, lmk.z * frame_width]
                                           for lmk in pose_landmarks.landmark], dtype=np.float32)
                assert pose_landmarks.shape == (33, 3), 'Unexpected landmarks shape: {}'.format(pose_landmarks.shape)

                # 对当前帧上的姿势进行分类。
                pose_classification = pose_classifier(pose_landmarks)

                # 使用 EMA 进行平滑分类。
                pose_classification_filtered = pose_classification_filter(pose_classification)
                print(pose_classification_filtered)
                # 计算重复次数。
                repetitions_count = repetition_counter(pose_classification_filtered)
            else:
                # 没有姿势 => 当前帧上没有分类。
                pose_classification = None

                # 仍然在过滤器中添加空分类以保持正确
                # 平滑未来的帧。
                pose_classification_filtered = pose_classification_filter(dict())
                pose_classification_filtered = None

                # 不要假设该人已“冻结”而更新计数器。 只是
                # 取最新的重复次数。
                repetitions_count = repetition_counter.n_repeats
            self.output_frame = cv2.resize(self.output_frame, (760, 620))
            self.output_frame = cv2.cvtColor(self.output_frame, cv2.COLOR_BGR2RGB)
            # 绘制分类图和重复计数器。
            # output_frame = pose_classification_visualizer(
            #     frame=output_frame,
            #     pose_classification=pose_classification,
            #     pose_classification_filtered=pose_classification_filtered,
            #     repetitions_count=repetitions_count)
            # 显示视频的中间帧以跟踪进度。
            # print(repetitions_count)
            cv2.putText(self.output_frame, str(int(repetitions_count)), (540, 100), cv2.FONT_HERSHEY_PLAIN, 7,
                        (255, 0, 0), 8)
            self.count = repetitions_count
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(self.output_frame, str(int(fps)), (30, 450), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
            # cv2.imshow('canny', np.array(self.output_frame))
            showImage = QtGui.QImage(self.output_frame.data, self.output_frame.shape[1], self.output_frame.shape[0],
                                     QtGui.QImage.Format_RGB888)
            self.ui.label.setPixmap(QtGui.QPixmap.fromImage(showImage))
            if cv2.waitKey(1) in [ord('q'), 27]:  # 按键盘上的q或esc退出（在英文输入法下）
                break
    def add_count_and_time(self):
        # self.endtime=time.time()
        if self.count != 0:
            self.time = (self.endtime - self.startTime)+self.time
            if self.count >= 50:
                self.sscore = 98
            elif self.count >= 30:
                self.sscore = 90
            elif self.count >= 20:
                self.sscore = 88
            elif self.count >= 10:
                self.sscore = 78
            else:
                self.sscore = 60
            try:
                data = {"suid": self.username, "sid": None, "stime": time.strftime("%Y-%m-%d %H:%M:%S"), "sname":self.sportName, "scount": self.count, "sscore": self.sscore,"syundongtime":int(self.endtime-self.startTime)}
                url = "http://43.136.75.221:8085/addsportdata"
                r = requests.post(url, data)
            except:
                print("不对劲")



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
            if self.cap.isOpened():
                self.cap.release()
            if self.timer_camera.isActive():
                self.timer_camera.stop()
            self.add_count_and_time()
            event.accept()


