import numpy as np


class FullBodyPoseEmbedder(object):
    """将 3D 姿势地标转换为 3D 嵌入."""

    def __init__(self, torso_size_multiplier=2.5):
        # 乘数应用于躯干以获得最小的身体尺寸。
        self._torso_size_multiplier = torso_size_multiplier

        # 出现在预测中的地标名称。
        self._landmark_names = [
            'nose',
            'left_eye_inner', 'left_eye', 'left_eye_outer',
            'right_eye_inner', 'right_eye', 'right_eye_outer',
            'left_ear', 'right_ear',
            'mouth_left', 'mouth_right',
            'left_shoulder', 'right_shoulder',
            'left_elbow', 'right_elbow',
            'left_wrist', 'right_wrist',
            'left_pinky_1', 'right_pinky_1',
            'left_index_1', 'right_index_1',
            'left_thumb_2', 'right_thumb_2',
            'left_hip', 'right_hip',
            'left_knee', 'right_knee',
            'left_ankle', 'right_ankle',
            'left_heel', 'right_heel',
            'left_foot_index', 'right_foot_index',
        ]

    def __call__(self, landmarks):
        """规范化姿势标志并转换为嵌入

         参数：
           landmarks - 具有形状 (N, 3) 的 3D 地标的 NumPy 数组。

         结果：
           具有形状 (M, 3) 的姿势嵌入的 Numpy 数组，其中“M”是
           `_get_pose_distance_embedding` 中定义的成对距离。
        """
        assert landmarks.shape[0] == len(self._landmark_names), 'Unexpected number of landmarks: {}'.format(
            landmarks.shape[0])

        # 获取姿势地标。
        landmarks = np.copy(landmarks)

        # 标准化地标。
        landmarks = self._normalize_pose_landmarks(landmarks)

        # 获取嵌入。
        embedding = self._get_pose_distance_embedding(landmarks)

        return embedding

    def _normalize_pose_landmarks(self, landmarks):
        """标准化地标平移和缩放。"""
        landmarks = np.copy(landmarks)

        # 规范化翻译。
        pose_center = self._get_pose_center(landmarks)
        landmarks -= pose_center

        # 标准化规模。
        pose_size = self._get_pose_size(landmarks, self._torso_size_multiplier)
        landmarks /= pose_size
        # 不需要乘以 100，但更容易调试。
        landmarks *= 100

        return landmarks

    def _get_pose_center(self, landmarks):
        """将姿势中心计算为臀部之间的点。"""
        left_hip = landmarks[self._landmark_names.index('left_hip')]
        right_hip = landmarks[self._landmark_names.index('right_hip')]
        center = (left_hip + right_hip) * 0.5
        return center

    def _get_pose_size(self, landmarks, torso_size_multiplier):
        """计算姿势大小。

         它是两个值中的最大值：
           * 躯干大小乘以`torso_size_multiplier`
           * 从姿势中心到任何姿势地标的最大距离
        """
        # 这种方法仅使用 2D 地标来计算姿势大小。
        landmarks = landmarks[:, :2]

        # 臀部中心。
        left_hip = landmarks[self._landmark_names.index('left_hip')]
        right_hip = landmarks[self._landmark_names.index('right_hip')]
        hips = (left_hip + right_hip) * 0.5

        # 肩部居中。
        left_shoulder = landmarks[self._landmark_names.index('left_shoulder')]
        right_shoulder = landmarks[self._landmark_names.index('right_shoulder')]
        shoulders = (left_shoulder + right_shoulder) * 0.5

        # 躯干尺寸作为最小的身体尺寸。
        torso_size = np.linalg.norm(shoulders - hips)

        # 到姿势中心的最大距离。
        pose_center = self._get_pose_center(landmarks)
        max_dist = np.max(np.linalg.norm(landmarks - pose_center, axis=1))

        return max(torso_size * torso_size_multiplier, max_dist)

    def _get_pose_distance_embedding(self, landmarks):
        """将姿势地标转换为 3D 嵌入。

         我们使用几个成对的 3D 距离来形成姿势嵌入。 所有距离
         包括带符号的 X 和 Y 分量。 我们涵盖不同类型的配对
         不同的姿势类。 随意删除一些或添加新的。

         参数：
           landmarks - 具有形状 (N, 3) 的 3D 地标的 NumPy 数组。

         结果：
           具有形状 (M, 3) 的姿势嵌入的 Numpy 数组，其中“M”是
           成对距离。
        """
        embedding = np.array([
            # 一关节。

            self._get_distance(
                self._get_average_by_names(landmarks, 'left_hip', 'right_hip'),
                self._get_average_by_names(landmarks, 'left_shoulder', 'right_shoulder')),

            self._get_distance_by_names(landmarks, 'left_shoulder', 'left_elbow'),
            self._get_distance_by_names(landmarks, 'right_shoulder', 'right_elbow'),

            self._get_distance_by_names(landmarks, 'left_elbow', 'left_wrist'),
            self._get_distance_by_names(landmarks, 'right_elbow', 'right_wrist'),

            self._get_distance_by_names(landmarks, 'left_hip', 'left_knee'),
            self._get_distance_by_names(landmarks, 'right_hip', 'right_knee'),

            self._get_distance_by_names(landmarks, 'left_knee', 'left_ankle'),
            self._get_distance_by_names(landmarks, 'right_knee', 'right_ankle'),

            # Two joints.

            self._get_distance_by_names(landmarks, 'left_shoulder', 'left_wrist'),
            self._get_distance_by_names(landmarks, 'right_shoulder', 'right_wrist'),

            self._get_distance_by_names(landmarks, 'left_hip', 'left_ankle'),
            self._get_distance_by_names(landmarks, 'right_hip', 'right_ankle'),

            # Four joints.

            self._get_distance_by_names(landmarks, 'left_hip', 'left_wrist'),
            self._get_distance_by_names(landmarks, 'right_hip', 'right_wrist'),

            # Five joints.

            self._get_distance_by_names(landmarks, 'left_shoulder', 'left_ankle'),
            self._get_distance_by_names(landmarks, 'right_shoulder', 'right_ankle'),

            self._get_distance_by_names(landmarks, 'left_hip', 'left_wrist'),
            self._get_distance_by_names(landmarks, 'right_hip', 'right_wrist'),

            # 交叉身体。

            self._get_distance_by_names(landmarks, 'left_elbow', 'right_elbow'),
            self._get_distance_by_names(landmarks, 'left_knee', 'right_knee'),

            self._get_distance_by_names(landmarks, 'left_wrist', 'right_wrist'),
            self._get_distance_by_names(landmarks, 'left_ankle', 'right_ankle'),

            # 身体弯曲方向。

            # self._get_distance(
            #     self._get_average_by_names(landmarks, 'left_wrist', 'left_ankle'),
            #     landmarks[self._landmark_names.index('left_hip')]),
            # self._get_distance(
            #     self._get_average_by_names(landmarks, 'right_wrist', 'right_ankle'),
            #     landmarks[self._landmark_names.index('right_hip')]),
        ])

        return embedding

    def _get_average_by_names(self, landmarks, name_from, name_to):
        lmk_from = landmarks[self._landmark_names.index(name_from)]
        lmk_to = landmarks[self._landmark_names.index(name_to)]
        return (lmk_from + lmk_to) * 0.5

    def _get_distance_by_names(self, landmarks, name_from, name_to):
        lmk_from = landmarks[self._landmark_names.index(name_from)]
        lmk_to = landmarks[self._landmark_names.index(name_to)]
        return self._get_distance(lmk_from, lmk_to)

    def _get_distance(self, lmk_from, lmk_to):
        return lmk_to - lmk_from