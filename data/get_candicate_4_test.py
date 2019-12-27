# coding=utf-8

r"""
为测试的diagnosis数据，获取k条候选的概念，并重新写出
"""

import os
import sys
sys.path.append(os.path.abspath('..') + '\\retrieval_model\\matching.py')
from retrieval_model.matching import MatchingModel


def get_candidate_4_test(train_concept, candidate_k, infer_dia):
    """
    为测试的diagnosis获取k个候选的概念
    :param train_concept: 训练的概念集路径
    :param candidate_k: 候选的个数
    :param infer_dia: 测试的诊断路径
    :return: 分别存储为两个文件，一个存放diagnosis+对应的concept，一个存放对应的匹配概率
    """
    match_model = MatchingModel(train_concept, os.path.abspath('..') +
                                '\\retrieval_model\\BioNLP-word-embedding.bin')
    with open(infer_dia, 'r', encoding='utf-8') as dia_f:
        infer_diagnosis = dia_f.readlines()
        for dia in infer_diagnosis:
            candidate_cons = match_model.query(dia, candidate_k)
            for con in candidate_cons:
                print(con)

train_concept = os.path.abspath('.') + '\\original_data\\split_data\\dia--dis\\full\\train-con.csv'
candidate_k = 25
infer_diagnosis = os.path.abspath('.') + '\\original_data\\split_data\\dia--dis\\full\\infer-dia.txt'

get_candidate_4_test(train_concept, candidate_k, infer_diagnosis)


