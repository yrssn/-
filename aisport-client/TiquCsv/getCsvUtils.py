from notebook import files

from Utils.BootstrapHelper import BootstrapHelper
from Utils.FullBodyPoseEmbedder import FullBodyPoseEmbedder
from Utils.PoseClassifier import PoseClassifier
import csv
import os
import numpy as np

class getCsv(object):
    def __init__(self,bootstrap_images_in_folder,bootstrap_images_out_folder,bootstrap_csvs_out_folder):
        self.bootstrap_images_in_folder=bootstrap_images_in_folder
        self.bootstrap_images_out_folder=bootstrap_images_out_folder
        self.bootstrap_csvs_out_folder=bootstrap_csvs_out_folder
    def getCsv(self):
        # images_in_folder 所需的结构：
        #
        #   fitness_poses_images_in/
        #     pushups_up/
        #       image_001.jpg
        #       image_002.jpg
        #       ...
        #     pushups_down/
        #       image_001.jpg
        #       image_002.jpg
        #       ...
        #     ...
        # 初始化助手。
        bootstrap_helper = BootstrapHelper(
            images_in_folder=self.bootstrap_images_in_folder,
            images_out_folder=self.bootstrap_images_out_folder,
            csvs_out_folder=self.bootstrap_csvs_out_folder,
        )

        # 检查有多少姿势类和图像可用。
        print('检查有多少姿势类和图像可用')
        bootstrap_helper.print_images_in_statistics()
        # 引导所有图像。
        # 将限制设置为一些小数字以进行调试。
        print('引导所有图像,提取特征')
        bootstrap_helper.bootstrap(per_pose_class_limit=None)
        # 检查引导了多少图像。
        print('检查引导了多少图像')
        bootstrap_helper.print_images_out_statistics()
        # 在没有检测到姿势的初始引导图像之后，仍然保存在
        # 用于调试目的的文件夹（但不在 CSV 中）。 让我们删除它们。
        # bootstrap_helper.align_images_and_csvs(print_removed_items=False)
        # bootstrap_helper.print_images_out_statistics()
        # Align CSVs with filtered images.
        bootstrap_helper.align_images_and_csvs(print_removed_items=False)
        bootstrap_helper.print_images_out_statistics()

        # 将姿势地标转换为嵌入。
        pose_embedder = FullBodyPoseEmbedder()

        # 根据姿势数据库对姿势进行分类。
        pose_classifier = PoseClassifier(
            pose_samples_folder=self.bootstrap_csvs_out_folder,
            pose_embedder=pose_embedder,
            top_n_by_max_distance=30,
            top_n_by_mean_distance=10)

        outliers = pose_classifier.find_pose_sample_outliers()
        print('Number of outliers: ', len(outliers))
        # 分析异常值。
        bootstrap_helper.analyze_outliers(outliers)
        # 删除所有异常值（如果您不想手动选择）。
        bootstrap_helper.remove_outliers(outliers)
        # 重新整理二分类数据
        bootstrap_helper.align_images_and_csvs(print_removed_items=False)
        bootstrap_helper.print_images_out_statistics()


    def dump_for_the_app(self):
        pose_samples_folder = 'image_out'
        pose_samples_csv_path = 'image_out.csv'
        file_extension = 'csv'
        file_separator = ','

        # 文件夹中的每个文件代表一个姿势类。
        file_names = [name for name in os.listdir(pose_samples_folder) if name.endswith(file_extension)]

        with open(pose_samples_csv_path, 'w') as csv_out:
            csv_out_writer = csv.writer(csv_out, delimiter=file_separator, quoting=csv.QUOTE_MINIMAL)
            for file_name in file_names:
                # 使用文件名作为姿势类名称。
                class_name = file_name[:-(len(file_extension) + 1)]

                # 一个文件行：`sample_00001,x1,y1,x2,y2,....`。
                with open(os.path.join(pose_samples_folder, file_name)) as csv_in:
                    csv_in_reader = csv.reader(csv_in, delimiter=file_separator)
                    for row in csv_in_reader:
                        row.insert(1, class_name)
                        csv_out_writer.writerow(row)
        # files.download(pose_samples_csv_path)


