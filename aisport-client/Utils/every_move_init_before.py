import time

import numpy as np
from mediapipe.python.solutions import pose as mp_pose
import cv2
from mediapipe.python.solutions import drawing_utils as mp_drawing
import matplotlib.pyplot as plt
from Utils.Core import show_image
import pyttsx3

from Utils.EMADictSmoothing import EMADictSmoothing
from Utils.FullBodyPoseEmbedder import FullBodyPoseEmbedder
from Utils.PoseClassificationVisualizer import PoseClassificationVisualizer
from Utils.PoseClassifier import PoseClassifier
from Utils.RepetitionCounter import RepetitionCounter


class init_before():
    def __init__(self,class_name,pose_samples_folder):
        self.class_name=class_name
        self.pose_samples_folder=pose_samples_folder
    def move_before_init_and_run(self):
        class_name = self.class_name
        pose_samples_folder = self.pose_samples_folder

        # 打开视频。
        video_cap = cv2.VideoCapture(1)

        # 获取一些视频参数以生成带有分类的输出视频。
        video_n_frames = video_cap.get(cv2.CAP_PROP_FRAME_COUNT)
        video_fps = video_cap.get(cv2.CAP_PROP_FPS)
        video_width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        video_height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        # 初始化跟踪器。
        pose_tracker = mp_pose.Pose(upper_body_only=False)

        # 始化嵌入器。
        pose_embedder = FullBodyPoseEmbedder()

        # 初始化分类器。
        # 检查您使用的参数是否与引导期间相同。
        pose_classifier = PoseClassifier(
            pose_samples_folder=pose_samples_folder,
            pose_embedder=pose_embedder,
            top_n_by_max_distance=30,
            top_n_by_mean_distance=10)

        # # 取消注释以验证分类器使用的目标姿势并找出异常值。
        # outliers = pose_classifier.find_pose_sample_outliers()
        # print('Number of pose sample outliers (consider removing them): ', len(outliers))

        # 初始化 EMA 平滑。
        pose_classification_filter = EMADictSmoothing(
            window_size=10,
            alpha=0.2)

        # 初始化计数器。
        repetition_counter = RepetitionCounter(
            class_name=class_name,
            enter_threshold=6,
            exit_threshold=4)

        # 初始化渲染器。
        pose_classification_visualizer = PoseClassificationVisualizer(
            class_name=class_name,
            plot_x_max=video_n_frames,
            # 如果它与 `top_n_by_mean_distance` 相同，图形看起来会更好。
            plot_y_max=10)

        # 打开cap
        video_cap.open(0)
        # 无限循环，直到break被触发
        pTime = 0
        count=0
        endtime=0
        starttime=time.time()
        run_time=0

        cv2.namedWindow("canny", 0)
        cv2.resizeWindow("canny", 800, 600)
        while video_cap.isOpened():
            # 获取视频的下一帧。
            success, input_frame = video_cap.read()
            if not success:
                break
            # 运行姿势跟踪器。
            input_frame = cv2.cvtColor(input_frame, cv2.COLOR_BGR2RGB)
            result = pose_tracker.process(image=input_frame)
            pose_landmarks = result.pose_landmarks

            # 绘制姿势预测。
            output_frame = input_frame.copy()
            if pose_landmarks is not None:
                mp_drawing.draw_landmarks(
                    image=output_frame,
                    landmark_list=pose_landmarks,
                    connections=mp_pose.POSE_CONNECTIONS)

            if pose_landmarks is not None:
                # 取地标。
                frame_height, frame_width = output_frame.shape[0], output_frame.shape[1]
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

            output_frame = cv2.cvtColor(output_frame, cv2.COLOR_BGR2RGB)
            # 绘制分类图和重复计数器。
            # output_frame = pose_classification_visualizer(
            #     frame=output_frame,
            #     pose_classification=pose_classification,
            #     pose_classification_filtered=pose_classification_filtered,
            #     repetitions_count=repetitions_count)
            # 显示视频的中间帧以跟踪进度。
            print(repetitions_count)
            cv2.putText(output_frame, str(int(repetitions_count)), (540, 100), cv2.FONT_HERSHEY_PLAIN, 7, (255, 0, 0), 8)
            count=repetitions_count
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            pTime = cTime
            cv2.putText(output_frame, str(int(fps)), (30, 450), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)
            cv2.imshow('canny', np.array(output_frame))
            if cv2.waitKey(1) in [ord('q'), 27]:  # 按键盘上的q或esc退出（在英文输入法下）
                endtime=time.time()
                break

        # 关闭摄像头
        video_cap.release()
        pose_tracker.close()
        # 关闭图像窗口
        cv2.destroyAllWindows()
        run_time=endtime-starttime
        return count,run_time
