import numpy as np
from mediapipe.python.solutions import pose as mp_pose
import tqdm
import cv2
from notebook import files
import matplotlib.pyplot as plt
from Utils.Core import show_image
from Utils.EMADictSmoothing import EMADictSmoothing
from Utils.FullBodyPoseEmbedder import FullBodyPoseEmbedder
from Utils.PoseClassificationVisualizer import PoseClassificationVisualizer
from Utils.PoseClassifier import PoseClassifier
from Utils.RepetitionCounter import RepetitionCounter
from mediapipe.python.solutions import drawing_utils as mp_drawing

video_path = '99.mp4'
class_name='down'
out_video_path = '99_out.mp4'

# 打开视频。
video_cap = cv2.VideoCapture(video_path)

# 获取一些视频参数以生成带有分类的输出视频。
video_n_frames = video_cap.get(cv2.CAP_PROP_FRAME_COUNT)
video_fps = video_cap.get(cv2.CAP_PROP_FPS)
video_width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))
video_height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

pose_samples_folder = 'tiaoshenCSV'


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


# 打开输出视频。
out_video = cv2.VideoWriter(out_video_path, cv2.VideoWriter_fourcc(*'mp4v'), video_fps, (video_width, video_height))

frame_idx = 0
output_frame = None
with tqdm.tqdm(total=video_n_frames, position=0, leave=True) as pbar:
    while True:
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

        # 绘制分类图和重复计数器。
        output_frame = pose_classification_visualizer(
            frame=output_frame,
            pose_classification=pose_classification,
            pose_classification_filtered=pose_classification_filtered,
            repetitions_count=repetitions_count)

        # 保存输出帧。
        out_video.write(cv2.cvtColor(np.array(output_frame), cv2.COLOR_RGB2BGR))

        # 显示视频的中间帧以跟踪进度。
        # if frame_idx % 500 == 0:
        #     show_image(output_frame)

        frame_idx += 50
        pbar.update()


# 关闭输出视频。
out_video.release()

# 释放 MediaPipe 资源。
pose_tracker.close()

# 显示视频的最后一帧。
if output_frame is not None:
    show_image(output_frame)

# 下载生成的视频
files.download(out_video_path)
