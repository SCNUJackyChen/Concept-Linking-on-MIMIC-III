# coding=utf-8

r"""
数据可视化图，主要是对输入序列和目标序列的长度进行可视化显示
"""

import matplotlib.pyplot as plt
import seaborn as sns


class InputTargetLengthVisual(object):
    def __init__(self, input_seq:list, target_seq:list):
        """
        赋值输入序列和目标序列，都为集合
        :param input: 输入序列
        :param target: 目标序列
        """
        self.input = [len(i.split(' ')) for i in input_seq]
        self.target = [len(j[0].split(' ')) for j in target_seq]
        assert len(self.input) == len(self.target), print('输入序列个数和目标序列个数不一致！')
        self.seq_len = len(self.input)

    def _bar_map(self):
        """
        输入、目标序列长度分布对比柱状图
        :return:
        """
        x = [i for i in range(self.seq_len)]
        plt.bar(x, self.input, label='diagnosis text length', color='blue', width=0.8, alpha=0.5)
        plt.bar(x, self.target, label='concept text length', color='green', width=0.8, alpha=0.5)
        plt.title('The Length Compare of Input sequence and Target Sequence')
        plt.xlabel('Each input or target text sequence')
        plt.ylabel('The text length of input or target sequence')
        plt.legend()
        plt.show()

    def _his_map(self):
        """
        输入、目标序列长度概率分布直方图
        :return:
        """
        plt.hist(self.input, 25, density=False, histtype='stepfilled', facecolor='blue', alpha=0.5,
                 label='diagnosis text sequence')
        plt.hist(self.target, 25, density=False, histtype='stepfilled', facecolor='green', alpha=0.5,
                 label='concept text sequence')
        plt.title('Length statistics of diagnosis or concept text sequences')
        plt.xlabel('The length of text sequence')
        plt.ylabel('The number of texts of a certain sequence length')
        plt.legend()
        plt.show()

        sns.rugplot(self.input, color='blue')
        sns.kdeplot(self.input, shade=True, color='blue', alpha=0.5, label='diagnosis text sequence')
        sns.rugplot(self.target, color='green')
        sns.kdeplot(self.target, shade=True, color='green', alpha=0.5, label='concept text sequence')
        plt.title('Length statistics of diagnosis or concept text sequences')
        plt.xlabel('The length of text sequence')
        plt.ylabel('The number of texts of a certain sequence length')
        plt.legend()
        plt.show()

    def show(self):
        """
        显示柱状图和直方图
        :return:
        """
        # self._bar_map()
        self._his_map()