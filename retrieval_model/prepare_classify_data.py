# coding=utf-8

r"""
融合字符匹配子模型的字符相似度和序列语义理解子模型的生成loss，把融合问题视为一个二分类问题，即k个候选的概念中，真实的为1，不真实的为0，
该程序主要是准备二分类所需的数据
"""

import os
from tqdm import tqdm


def prepare_classify_data(k):
    """
    从训练好的匹配模型和生成模型的结果数据中准备相应的二分类数据
    :return:
    """
    pass

base_path = 'E:\\pycharm\\Reproduce_Transformer\\results\\'
source_data = None
story_path = 'E:\\pycharm\\Reproduce_Transformer\\model_ensemble\\class_data\\'
processed_data = None


