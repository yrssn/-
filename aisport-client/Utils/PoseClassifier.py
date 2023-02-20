import csv
import numpy as np
import os

from Utils.PoseSample import PoseSample
from Utils.PoseSampleOutlier import PoseSampleOutlier


class PoseClassifier(object):
    """对姿势地标进行分类。"""

    def __init__(self,
                 pose_samples_folder,
                 pose_embedder,
                 file_extension='csv',
                 file_separator=',',
                 n_landmarks=33,
                 n_dimensions=3,
                 top_n_by_max_distance=30,
                 top_n_by_mean_distance=10,
                 axes_weights=(1., 1., 0.2)):
        self._pose_embedder = pose_embedder
        self._n_landmarks = n_landmarks
        self._n_dimensions = n_dimensions
        self._top_n_by_max_distance = top_n_by_max_distance
        self._top_n_by_mean_distance = top_n_by_mean_distance
        self._axes_weights = axes_weights

        self._pose_samples = self._load_pose_samples(pose_samples_folder,
                                                     file_extension,
                                                     file_separator,
                                                     n_landmarks,
                                                     n_dimensions,
                                                     pose_embedder)

    def _load_pose_samples(self,
                           pose_samples_folder,
                           file_extension,
                           file_separator,
                           n_landmarks,
                           n_dimensions,
                           pose_embedder):
        """从给定文件夹加载姿势样本。

         所需的文件夹结构：
           中性站立.csv
           down.csv
           up.csv
           squats_down.csv
           ...

         所需的 CSV 结构：
           样品_00001,x1,y1,z1,x2,y2,z2,....
           样品_00002,x1,y1,z1,x2,y2,z2,....
           ...
        """
        # 文件夹中的每个文件代表一个姿势类。
        file_names = [name for name in os.listdir(pose_samples_folder) if name.endswith(file_extension)]

        pose_samples = []
        for file_name in file_names:
            # 使用文件名作为姿势类名称。
            class_name = file_name[:-(len(file_extension) + 1)]

            # 解析 CSV。
            with open(os.path.join(pose_samples_folder, file_name)) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=file_separator)
                for row in csv_reader:
                    assert len(row) == n_landmarks * n_dimensions + 1, 'Wrong number of values: {}'.format(len(row))
                    landmarks = np.array(row[1:], np.float32).reshape([n_landmarks, n_dimensions])
                    pose_samples.append(PoseSample(
                        name=row[0],
                        landmarks=landmarks,
                        class_name=class_name,
                        embedding=pose_embedder(landmarks),
                    ))

        return pose_samples

    def find_pose_sample_outliers(self):
        """针对整个数据库对每个样本进行分类。"""
        # 找出目标姿势中的异常值
        outliers = []
        for sample in self._pose_samples:
            # 为目标找到最近的姿势。
            pose_landmarks = sample.landmarks.copy()
            pose_classification = self.__call__(pose_landmarks)
            class_names = [class_name for class_name, count in pose_classification.items() if
                           count == max(pose_classification.values())]

            # 如果最近的姿势具有不同的类别或更多，则样本是异常值
            # 一个姿势类被检测为最近。
            if sample.class_name not in class_names or len(class_names) != 1:
                outliers.append(PoseSampleOutlier(sample, class_names, pose_classification))

        return outliers

    def __call__(self, pose_landmarks):
        """对给定的姿势进行分类。

         分类分两个阶段进行：
           * 首先，我们按 MAX 距离选取前 N 个样本。 它允许删除样本
             与给定姿势几乎相同，但几乎没有关节弯曲
             其他方向。
           * 然后我们按平均距离选择前 N 个样本。 去除异常值后
             在上一步中，我们可以选择平均接近的样本。

         参数：
           pose_landmarks：具有形状为 (N, 3) 的 3D 地标的 NumPy 数组。

         回报：
           包含数据库中最近姿势样本计数的字典。 样本：
             {
               “俯卧撑”：8，
               “俯卧撑”：2，
             }
        """
        # 检查提供的姿势和目标姿势是否具有相同的形状。
        assert pose_landmarks.shape == (self._n_landmarks, self._n_dimensions), 'Unexpected shape: {}'.format(
            pose_landmarks.shape)

        # 获得给定的姿势嵌入。
        pose_embedding = self._pose_embedder(pose_landmarks)
        flipped_pose_embedding = self._pose_embedder(pose_landmarks * np.array([-1, 1, 1]))

        # 按最大距离过滤。
        #
        # 这有助于消除异常值 - 与
        # 给定一个，但有一个关节弯曲到另一个方向，实际上
        # 代表不同的姿势类。
        max_dist_heap = []
        for sample_idx, sample in enumerate(self._pose_samples):
            max_dist = min(
                np.max(np.abs(sample.embedding - pose_embedding) * self._axes_weights),
                np.max(np.abs(sample.embedding - flipped_pose_embedding) * self._axes_weights),
            )
            max_dist_heap.append([max_dist, sample_idx])

        max_dist_heap = sorted(max_dist_heap, key=lambda x: x[0])
        max_dist_heap = max_dist_heap[:self._top_n_by_max_distance]

        # 按平均距离过滤。
        #
        # 去除异常值后，我们可以通过平均距离找到最近的位姿。
        mean_dist_heap = []
        for _, sample_idx in max_dist_heap:
            sample = self._pose_samples[sample_idx]
            mean_dist = min(
                np.mean(np.abs(sample.embedding - pose_embedding) * self._axes_weights),
                np.mean(np.abs(sample.embedding - flipped_pose_embedding) * self._axes_weights),
            )
            mean_dist_heap.append([mean_dist, sample_idx])

        mean_dist_heap = sorted(mean_dist_heap, key=lambda x: x[0])
        mean_dist_heap = mean_dist_heap[:self._top_n_by_mean_distance]

        # 将结果收集到地图中：（class_name -> n_samples）
        class_names = [self._pose_samples[sample_idx].class_name for _, sample_idx in mean_dist_heap]
        result = {class_name: class_names.count(class_name) for class_name in set(class_names)}

        return result