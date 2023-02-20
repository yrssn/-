import numpy as np
import pyttsx3
from mediapipe.python.solutions import pose as mp_pose
import cv2
from mediapipe.python.solutions import drawing_utils as mp_drawing
import matplotlib.pyplot as plt
from Utils.Core import show_image
from Utils.EMADictSmoothing import EMADictSmoothing
from Utils.FullBodyPoseEmbedder import FullBodyPoseEmbedder
from Utils.PoseClassificationVisualizer import PoseClassificationVisualizer
from Utils.PoseClassifier import PoseClassifier
from Utils.RepetitionCounter import RepetitionCounter


# 打开视频。
video_cap = cv2.VideoCapture(r"D:\pythonProject1\UI\shiping\八段锦.mp4")

while video_cap.isOpened():
    # 获取视频的下一帧。
    success, input_frame = video_cap.read()
    if not success:
        break
    cv2.imshow('camera',np.array(input_frame))
    if cv2.waitKey(1) in [ord('q'), 27]:  # 按键盘上的q或esc退出（在英文输入法下）
        break

# 关闭摄像头
video_cap.release()
# 关闭图像窗口
cv2.destroyAllWindows()
