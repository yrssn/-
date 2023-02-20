import csv

import cv2
from matplotlib import pyplot as plt
import numpy as np
import os
from PIL import Image, ImageDraw
import sys
import tqdm

from mediapipe.python.solutions import drawing_utils as mp_drawing
from mediapipe.python.solutions import pose as mp_pose

from Utils.Core import show_image


class BootstrapHelper(object):
    """Helps to bootstrap images and filter pose samples for classification."""

    def __init__(self,
                 images_in_folder,
                 images_out_folder,
                 csvs_out_folder):
        self._images_in_folder = images_in_folder
        self._images_out_folder = images_out_folder
        self._csvs_out_folder = csvs_out_folder

        # Get list of pose classes and print image statistics.
        self._pose_class_names = sorted([n for n in os.listdir(self._images_in_folder) if not n.startswith('.')])

    def bootstrap(self, per_pose_class_limit=None):
        """引导给定文件夹中的图像。

         文件夹中所需的图像（与图像输出文件夹相同）：
           pushups_up/
             image_001.jpg
             image_002.jpg
             ...
           pushups_down/
             image_001.jpg
             image_002.jpg
             ...
           ...

         生成的 CSV 出文件夹：
           up.csv
           down.csv

         生成的带有姿势 3D 地标的 CSV 结构：
           样品_00001,x1,y1,z1,x2,y2,z2,....
           样品_00002,x1,y1,z1,x2,y2,z2,....
        """
        # 为 CVS 创建输出文件夹。
        if not os.path.exists(self._csvs_out_folder):
            os.makedirs(self._csvs_out_folder)

        for pose_class_name in self._pose_class_names:
            print('Bootstrapping ', pose_class_name, file=sys.stderr)

            # 姿势类的路径。
            images_in_folder = os.path.join(self._images_in_folder, pose_class_name)
            images_out_folder = os.path.join(self._images_out_folder, pose_class_name)
            csv_out_path = os.path.join(self._csvs_out_folder, pose_class_name + '.csv')
            if not os.path.exists(images_out_folder):
                os.makedirs(images_out_folder)

            with open(csv_out_path, 'w') as csv_out_file:
                csv_out_writer = csv.writer(csv_out_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                # 获取图像列表。
                image_names = sorted([n for n in os.listdir(images_in_folder) if not n.startswith('.')])
                print(image_names)
                if per_pose_class_limit is not None:
                    image_names = image_names[:per_pose_class_limit]

                # 引导每个图像。
                for image_name in tqdm.tqdm(image_names):
                    # 加载图像。
                    input_frame = cv2.imread(os.path.join(images_in_folder, image_name))
                    input_frame = cv2.cvtColor(input_frame, cv2.COLOR_BGR2RGB)
                    # 初始化新的姿势跟踪器并运行它。
                    with mp_pose.Pose(upper_body_only=False) as pose_tracker:
                        result = pose_tracker.process(image=input_frame)
                        pose_landmarks = result.pose_landmarks

                    # 使用姿势预测保存图像（如果检测到姿势）。
                    output_frame = input_frame.copy()
                    if pose_landmarks is not None:
                        mp_drawing.draw_landmarks(
                            image=output_frame,
                            landmark_list=pose_landmarks,
                            connections=mp_pose.POSE_CONNECTIONS)
                    output_frame = cv2.cvtColor(output_frame, cv2.COLOR_RGB2BGR)
                    cv2.imwrite(os.path.join(images_out_folder, image_name), output_frame)

                    # 如果检测到姿势，则保存地标。
                    if pose_landmarks is not None:
                        # 获取地标。
                        frame_height, frame_width = output_frame.shape[0], output_frame.shape[1]
                        pose_landmarks = np.array(
                            [[lmk.x * frame_width, lmk.y * frame_height, lmk.z * frame_width]
                             for lmk in pose_landmarks.landmark],
                            dtype=np.float32)
                        assert pose_landmarks.shape == (33, 3), 'Unexpected landmarks shape: {}'.format(
                            pose_landmarks.shape)
                        csv_out_writer.writerow([image_name] + pose_landmarks.flatten().astype(np.str).tolist())

                    # 绘制 XZ 投影并与图像连接。
                    projection_xz = self._draw_xz_projection(
                        output_frame=output_frame, pose_landmarks=pose_landmarks)
                    output_frame = np.concatenate((output_frame, projection_xz), axis=1)

    def _draw_xz_projection(self, output_frame, pose_landmarks, r=0.5, color='red'):
        frame_height, frame_width = output_frame.shape[0], output_frame.shape[1]
        img = Image.new('RGB', (frame_width, frame_height), color='white')

        if pose_landmarks is None:
            return np.asarray(img)

        # 根据图像宽度缩放半径。
        r *= frame_width * 0.01

        draw = ImageDraw.Draw(img)
        for idx_1, idx_2 in mp_pose.POSE_CONNECTIONS:
            # 翻转 Z 并将臀部中心移动到图像的中心。
            x1, y1, z1 = pose_landmarks[idx_1] * [1, 1, -1] + [0, 0, frame_height * 0.5]
            x2, y2, z2 = pose_landmarks[idx_2] * [1, 1, -1] + [0, 0, frame_height * 0.5]

            draw.ellipse([x1 - r, z1 - r, x1 + r, z1 + r], fill=color)
            draw.ellipse([x2 - r, z2 - r, x2 + r, z2 + r], fill=color)
            draw.line([x1, z1, x2, z2], width=int(r), fill=color)

        return np.asarray(img)

    def align_images_and_csvs(self, print_removed_items=False):
        """确保图像文件夹和 CSV 具有相同的样本。 仅在图像文件夹和 CSV 中保留样本的交集。
        """
        for pose_class_name in self._pose_class_names:
            # 姿势类的路径。
            images_out_folder = os.path.join(self._images_out_folder, pose_class_name)
            csv_out_path = os.path.join(self._csvs_out_folder, pose_class_name + '.csv')

            # 将 CSV 读入内存。
            rows = []
            with open(csv_out_path,newline='') as csv_out_file:
                csv_out_reader = csv.reader(csv_out_file, delimiter=',')
                for row in csv_out_reader:
                    if len(row) == 0:
                        continue
                    else:
                        rows.append(row)
            for row in rows:
                print(row[0])
            # CSV 中保留的图像名称。
            image_names_in_csv = []

            # 重写没有相应图像的 CSV 删除行。
            with open(csv_out_path, 'w',newline='') as csv_out_file:
                csv_out_writer = csv.writer(csv_out_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                for row in rows:
                    image_name = row[0]
                    image_path = os.path.join(images_out_folder, image_name)
                    if os.path.exists(image_path):
                        image_names_in_csv.append(image_name)
                        csv_out_writer.writerow(row)
                    elif print_removed_items:
                        print('Removed image from CSV: ', image_path)

            # 删除 CSV 中没有对应行的图像。
            for image_name in os.listdir(images_out_folder):
                if image_name not in image_names_in_csv:
                    image_path = os.path.join(images_out_folder, image_name)
                    os.remove(image_path)
                    if print_removed_items:
                        print('Removed image from folder: ', image_path)

    def analyze_outliers(self, outliers):
        """将每个样本与所有其他样本进行分类以找出异常值。

         如果样本的分类与原始类别不同 - 它应该
         要么被删除，要么应该添加更多类似的样本。
        """
        for outlier in outliers:
            image_path = os.path.join(self._images_out_folder, outlier.sample.class_name, outlier.sample.name)

            print('Outlier')
            print('  sample path =    ', image_path)
            print('  sample class =   ', outlier.sample.class_name)
            print('  detected class = ', outlier.detected_class)
            print('  all classes =    ', outlier.all_classes)

            img = cv2.imread(image_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            show_image(img, figsize=(20, 20))

    def remove_outliers(self, outliers):
        """从图像文件夹中删除异常值."""
        for outlier in outliers:
            image_path = os.path.join(self._images_out_folder, outlier.sample.class_name, outlier.sample.name)
            os.remove(image_path)

    def print_images_in_statistics(self):
        """从输入图像文件夹打印统计信息。"""
        self._print_images_statistics(self._images_in_folder, self._pose_class_names)

    def print_images_out_statistics(self):
        """Prints statistics from the output image folder."""
        self._print_images_statistics(self._images_out_folder, self._pose_class_names)

    def _print_images_statistics(self, images_folder, pose_class_names):
        print('Number of images per pose class:')
        for pose_class_name in pose_class_names:
            n_images = len([
                n for n in os.listdir(os.path.join(images_folder, pose_class_name))
                if not n.startswith('.')])
            print('  {}: {}'.format(pose_class_name, n_images))