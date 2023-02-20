import sys
import time
from threading import Timer

import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from Utils.EMADictSmoothing import EMADictSmoothing
from Utils.FullBodyPoseEmbedder import FullBodyPoseEmbedder
from Utils.PoseClassificationVisualizer import PoseClassificationVisualizer
from Utils.PoseClassifier import PoseClassifier
from Utils.RepetitionCounter import RepetitionCounter
from UI.jishiyundong import Ui_Form

from mediapipe.python.solutions import pose as mp_pose
from mediapipe.python.solutions import drawing_utils as mp_drawing

class jishuyundongMain(QtWidgets.QWidget):
    def __init__(self,list,time,username):
        super().__init__()
        self.list=list
        self.time=time
        self.username=username
        self.ui=Ui_Form()
        self.ui.setupUi(self)
        self.timer_camera = QtCore.QTimer()
        self.cap = cv2.VideoCapture()
        self.CAM_NUM = 0
        self.temp = 0
        self.count = 0
        self.ui.label_3.setText(str(self.list[self.temp]))
        self.ui.label_6.setText("卡顿为休息时间，休息时间默认为15秒")
        self.ui.label_8.setText(str(self.time))
        self.ui.label_5.setText(str(self.username))
        self.alltime=self.time*len(self.list)/2+(len(self.list)/2-1)*8
        self.slots_init()
    def slots_init(self):
        self.ui.openshexiangtou.clicked.connect(self.button_open_camera_click)
        self.timer_camera.timeout.connect(self.show_shexiangtou)
        self.ui.fanhui.clicked.connect(self.close)

    def button_open_camera_click(self):

        if self.timer_camera.isActive() == False:
            flag = self.cap.open(self.CAM_NUM)
            if flag == False:
                msg = QtWidgets.QMessageBox.Warning(self, u'Warning', u'请检测相机与电脑是否连接正确',
                                                    buttons=QtWidgets.QMessageBox.Ok,
                                                    defaultButton=QtWidgets.QMessageBox.Ok)
            else:
              self.temp=0
              self.timer_camera.start(30)
              self.ui.openshexiangtou.setText(u'关闭相机')
        else:
            self.timer_camera.stop()
            self.cap.release()
            self.ui.label.clear()
            self.ui.openshexiangtou.setText(u'打开相机')
    def show_shexiangtou(self):
            self.ui.label_3.setText(self.list[self.temp])

            self.cap=cv2.VideoCapture(0)
            video_n_frames = self.cap.get(cv2.CAP_PROP_FRAME_COUNT)
            # 初始化跟踪器。
            pose_tracker = mp_pose.Pose(upper_body_only=False)
            # 始化嵌入器。
            pose_embedder = FullBodyPoseEmbedder()
            # 初始化分类器。
            # 检查您使用的参数是否与引导期间相同。
            pose_classifier = PoseClassifier(
                pose_samples_folder=self.list[self.temp+1],
                pose_embedder=pose_embedder,
                top_n_by_max_distance=30,
                top_n_by_mean_distance=10)
            # 初始化 EMA 平滑。
            pose_classification_filter = EMADictSmoothing(
                window_size=10,
                alpha=0.2)
            # 初始化计数器。
            repetition_counter = RepetitionCounter(
                class_name='down',
                enter_threshold=6,
                exit_threshold=4)
            # 初始化渲染器。
            pose_classification_visualizer = PoseClassificationVisualizer(
                class_name='down',
                plot_x_max=video_n_frames,
                # 如果它与 `top_n_by_mean_distance` 相同，图形看起来会更好。
                plot_y_max=10)
            self.cap.open(0)
            self.startTime=int(time.time())
            print("开始时间" + str(self.startTime))
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
                    assert pose_landmarks.shape == (33, 3), 'Unexpected landmarks shape: {}'.format(
                        pose_landmarks.shape)

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
                self.output_frame = cv2.resize(self.output_frame, (900, 800))
                self.output_frame = cv2.cvtColor(self.output_frame, cv2.COLOR_BGR2RGB)
                cv2.putText(self.output_frame, str(int(repetitions_count)), (540, 100), cv2.FONT_HERSHEY_PLAIN, 7,
                            (255, 0, 0), 8)
                showImage = QtGui.QImage(self.output_frame.data, self.output_frame.shape[1],
                                         self.output_frame.shape[0],
                                         QtGui.QImage.Format_RGB888)
                self.ui.label.setPixmap(QtGui.QPixmap.fromImage(showImage))
                if cv2.waitKey(1) in [ord('q'), 27] or (int(time.time())-self.time)==self.startTime:  # 按键盘上的q或esc退出（在英文输入法下）
                    self.temp+=2
                    print(self.temp)
                    if self.temp == len(self.list):
                        self.timer_camera.stop()
                        self.cap.release()
                        self.ui.label.clear()
                        self.ui.openshexiangtou.setText(u'打开相机')
                        return
                    else:
                        time.sleep(15)
                    print("结束时间"+str(int(time.time())))
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
            self.zjm.ui.widget_6.show()
            if self.cap.isOpened():
                self.cap.release()
            if self.timer_camera.isActive():
                self.timer_camera.stop()
            event.accept()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     win = jishuyundongMain(["深蹲","shendunCSV","俯卧撑","fowoshenCSV","引体向上","yintiCSV"],15,11)
#     sys.exit(app.exec_())