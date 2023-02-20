class EMADictSmoothing(object):
    """平滑姿势分类。"""

    def __init__(self, window_size=10, alpha=0.2):
        self._window_size = window_size
        self._alpha = alpha

        self._data_in_window = []

    def __call__(self, data):
        """平滑给定的姿势分类。

         通过计算每个姿势的指数移动平均线来完成平滑
         在给定的时间窗口中观察到的类。 错过的姿势课程被替换
         与 0。

         参数：
           数据：带有姿势分类的字典。 样本：
               {
                 “俯卧撑”：8，
                 “俯卧撑”：2，
               }

         结果：
           字典格式相同，但使用平滑和浮动而不是
           整数值。 样本：
             {
               “俯卧撑”：8.3，
               “俯卧撑”：1.7，
             }
        """
        # 将新数据添加到窗口的开头以获得更简单的代码。
        self._data_in_window.insert(0, data)
        self._data_in_window = self._data_in_window[:self._window_size]

        # 获得所有钥匙。
        keys = set([key for data in self._data_in_window for key, _ in data.items()])

        # 获取平滑值。
        smoothed_data = dict()
        for key in keys:
            factor = 1.0
            top_sum = 0.0
            bottom_sum = 0.0
            for data in self._data_in_window:
                value = data[key] if key in data else 0.0

                top_sum += factor * value
                bottom_sum += factor

                # 更新因子。
                factor *= (1.0 - self._alpha)

            smoothed_data[key] = top_sum / bottom_sum

        return smoothed_data