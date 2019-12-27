# conding=utf-8

r"""
使用匹配抽取模型，对测试的diagnosis，生成k个候选的概念及匹配概率
做成一个函数的形式，输入是一个测试的测试的diagnosis的txt文件，输出是一个含有k个候选的concept概念，及一个对应的匹配概率文件
"""

import gensim
import csv
from fse.inputs import IndexedList
from fse.models import SIF
import math
import numpy as np
from sklearn.preprocessing import normalize, scale, MinMaxScaler
import logging
from tqdm import tqdm
import os


def candidate_con_4_dia(infer_dia, infer_dia_repeat_k, train_con, k:int,
                        infer_candi_k_con, infer_candi_k_pro, word_vec_f):
    """
    读入测试的diagnosis文件，载入预训练的BioNLP词向量，读入训练的concept文件，生成k个候选的概念和对应的概率
    :param infer_dia: 测试的diagnosis txt文件
    :param infer_dia_repeat_k: 由于测试需要，也要对diagnosis txt文件每条复制k次写出
    :param train_con: 训练的concept txt文件，也是候选概念的来源
    :param k: 候选概念数
    :param infer_candi_k_con: 写出候选概念文件
    :param infer_candi_k_pro: 写出候选概念文件匹配概率文件
    :param word_vec_f: 预训练好的BioNLP词向量
    :return: 写出两个文件，一个是候选的concept文件，一个是对应的匹配概率文件
    """
    print('载入BioNLP词向量...')
    bio_nlp_model = gensim.models.KeyedVectors.load_word2vec_format(word_vec_f, binary=True)  # 载入BioNLP词向量
    print('载入BioNLP向量文件完成！')

    train_cons = []  # 存储训练的概念集
    with open(train_con, 'r', encoding='utf-8') as train_con_f:
        for row in tqdm(train_con_f, desc='读取训练的concept文件', leave=False):
            train_cons.append(row)
    train_cons = [i.split() for i in list(set(train_cons))]  # 去重并切分概念序列
    concepts = IndexedList(train_cons)  # 概念序列化
    sif = SIF(bio_nlp_model)  # SIF模型
    sif.train(concepts)  # 用训练的概念序列去训练SIF模型

    infer_candi_k_con_f = open(infer_candi_k_con, 'w', encoding='utf-8')  # 输出候选concept文件
    infer_candi_k_pro_f = open(infer_candi_k_pro, 'w', encoding='utf-8')  # 输出候选concept对应概率的文件
    infer_dia_repeat_k_f = open(infer_dia_repeat_k, 'w', encoding='utf-8')  # 重复写k次诊断dia

    with open(infer_dia, 'r', encoding='utf-8') as infer_dia_f:
        for dia in tqdm(infer_dia_f, desc='查询和当前diagnosis最相似的k个候选概念', leave=False):
            for _ in range(k):  # 每条dia写k次
                infer_dia_repeat_k_f.write(dia.split('\n')[0])
                infer_dia_repeat_k_f.write('\n')

            dia_candi_cons = sif.sv.similar_by_sentence(  # 查询和当前诊断余弦相似度最大的k个候选概念
                dia.split(), model=sif, topn=k, indexable=concepts.items)

            for con_p in dia_candi_cons:  # 依次写出候选概念和对应的匹配概率
                candi_con = ''
                for word in con_p[0]:
                    candi_con += ' ' + word
                infer_candi_k_con_f.write(candi_con)  # 写出这个候选的concept
                infer_candi_k_con_f.write('\n')
                infer_candi_k_pro_f.write(str(round(con_p[2], 3)))  # 写出这个concept对应的匹配概率
                infer_candi_k_pro_f.write('\n')

    infer_candi_k_con_f.close()
    infer_candi_k_pro_f.close()
    infer_dia_repeat_k_f.close()

    print('读写完毕')


k = 25
train_con = os.path.abspath('..') + '\\data\\original_data\\split_data\\dia-desc--dis\\full\\train-con.txt'
infer_dia = os.path.abspath('..') + '\\data\\original_data\\split_data\\dia-desc--dis\\full\\infer-dia.txt'
infer_dia_repeat_k = os.path.abspath('..') + \
              '\\data\\original_data\\split_data\\dia-desc--dis\\full\\infer-dia-repeat-' + str(k) + '.txt'
infer_candi_k_con = os.path.abspath('..') + \
                    '\\data\\original_data\\split_data\\dia-desc--dis\\full\\infer-candi-' + str(k) + '-con.txt'
infer_candi_k_pro = os.path.abspath('..') + \
                    '\\data\\original_data\\split_data\\dia-desc--dis\\full\\infer-candi-' + str(k) + '-pro.txt'
bio_nlp = os.path.abspath('.') + '\\BioNLP-word-embedding.bin'

candidate_con_4_dia(infer_dia, infer_dia_repeat_k, train_con, k, infer_candi_k_con, infer_candi_k_pro, bio_nlp)






