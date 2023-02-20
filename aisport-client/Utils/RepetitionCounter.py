class RepetitionCounter(object):
    """计算给定目标姿势类的重复次数。"""

    def __init__(self, class_name, enter_threshold=6, exit_threshold=4):
        self._class_name = class_name

        # 如果姿势计数器通过给定的阈值，那么我们输入姿势。
        self._enter_threshold = enter_threshold
        self._exit_threshold = exit_threshold

        # 我们要么处于给定的姿势，要么没有。
        self._pose_entered = False

        # 我们退出姿势的次数。
        self._n_repeats = 0

    @property
    def n_repeats(self):
        return self._n_repeats

    def __call__(self, pose_classification):
        """计算给定帧之前发生的重复次数。

         我们使用两个阈值。 首先，您需要高于更高的进入
         姿势，然后你需要走到较低的姿势下方才能退出它。 不同之处
         阈值之间使其稳定预测抖动（这将
         在只有一个阈值的情况下导致错误计数）。

         参数：
           pose_classification：当前帧上的姿势分类字典。
             样本：
               {
                 “俯卧撑”：8.3，
                 “俯卧撑”：1.7，
               }

         回报：
           重复的整数计数器。
        """
        # 获得姿势自信。
        pose_confidence = 0.0
        if self._class_name in pose_classification:
            pose_confidence = pose_classification[self._class_name]

        # 在第一帧或者如果我们不在姿势中，只需检查我们是否
        # 在这个框架上输入它并更新状态。
        if not self._pose_entered:
            self._pose_entered = pose_confidence > self._enter_threshold
            return self._n_repeats

        # 如果我们处于姿势并正在退出它，则增加计数器并
        # 更新状态。
        if pose_confidence < self._exit_threshold:
            self._n_repeats += 1
            self._pose_entered = False

        return self._n_repeats