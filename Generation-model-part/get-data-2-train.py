# coding=utf-8

r"""
先简单的抽取diagnosis-2diseases表的diagnosis列和icd9_code text列，初步使用Transformer模型进行训练
"""

import csv
import numpy as np
import os
from tqdm import *
from sklearn.model_selection import KFold, train_test_split
from functools import reduce
import sys
sys.path.append('..')
from data_visual.data_visual_map import InputTargetLengthVisual

un_repeat = False  # 是否对输入序列进行去重
add_dia = True  # 是否对diagnosis文本加入diagnosis
add_desc = False  # 是否对diagnosis文本加上description
add_text = False  # 是否对diagnosis文本加上text文本
add_father = False # 是否对concept加上father文本
father = True  # 是否单独写出father文本
max_len = 100  # 序列token最大长度

file_path = os.path.abspath('..') + '\\data\\original_data\\diagnosis-2-disease.csv'
text_data = csv.reader(open(file_path, 'r'))
diagnosis = []  # 诊断集
concept = []  # 概念集
fathers = []  # 父概念集
un_repeat_con = []  # 存放无重复的概念集
for idx, line in enumerate(text_data):
    if idx != 0:
        if un_repeat:  # 去重概念
            if line[12] not in un_repeat_con:
                dia = line[0] if add_dia else ''
                if add_desc:
                    dia = dia + ' ' + line[1]  # 加description
                if add_text:
                    dia = dia + ' ' + line[2]  # 加text
                if dia.split(' ') > max_len:  # 诊断文本序列最大词数
                    new_dia = [lambda x, y: x + ' ' + y, dia.split(' ')[:100]]
                    diagnosis.append(new_dia)
                else:
                    diagnosis.append(dia)
                if add_father:  # 对概念加上父概念
                    concept.append(line[12] + ' ' + line[14])
                else:  # 不加父概念
                    concept.append(line[12])
        else:  # 不去重概念
            dia = line[0] if add_dia else ''  # 加diagnosis
            if add_desc:
                dia = dia + ' ' + line[1]  # 加description
            if add_text:
                dia = dia + ' ' + line[2]  # 加text
            if len(dia.split(' ')) > max_len:  # 当前诊文本条数超过最大词数
                new_dia = ''  # 截取前100个单词
                for i in dia.split(' ')[:100]:
                    new_dia = new_dia + ' ' + i
                diagnosis.append(new_dia)
            else:
                diagnosis.append(dia)

            assert not (father and add_father), print('不能同时对概念加上父概念和单独写出父概念')
            con_fa = [None, None]  # 概念父概念集
            if len(line) >= 14:  # 有父概念
                con_fa[0] = (line[12] + ' ' + line[14]) if add_father else line[12]
                con_fa[1] = line[14] if father else None
            else:
                con_fa[0] = line[12]
            concept.append(con_fa)
    un_repeat_con.append(line[12])  # 已经加入的概念集合

assert len(diagnosis) == len(concept), '诊断文本条数和概念文本条数不一致，无法写入！'
print('原数据条数{}'.format(idx))
print('数据集最长序列词数{}'.format(max([len(i.split(' ')) for i in diagnosis])))
print('筛选后的数据条数{}'.format(len(diagnosis)))
show = InputTargetLengthVisual(diagnosis, concept)
show.show()

train_x, val_infer_x, train_y, val_infer_y = train_test_split(
    diagnosis, concept, train_size=0.9, test_size=0.1, shuffle=True, random_state=2019)
val_x, infer_x, val_y, infer_y = train_test_split(
    val_infer_x, val_infer_y, train_size=0.2, test_size=0.8, shuffle=True, random_state=2019)
assert len(train_x) == len(train_y)
assert len(val_x) == len(val_y)
assert len(infer_x) == len(infer_y)

with open('dia-2-dis\\train-dia.txt', mode='w', encoding='utf-8') as train_dia:
    for i in train_x:
        train_dia.write(i)
        train_dia.write('\n')

with open('dia-2-dis\\train-con.txt', mode='w', encoding='utf-8') as train_con:
    for i in train_y:
        train_con.write(i[0])
        train_con.write('\n')

with open('dia-2-dis\\train-father.txt', mode='w', encoding='utf-8') as train_father:
    for i in train_y:
        train_father.write(i[1] if i[1] else 'None')
        train_father.write('\n')

with open('dia-2-dis\\val-dia.txt', mode='w', encoding='utf-8') as val_dia:
    for i in val_x:
        val_dia.write(i)
        val_dia.write('\n')

with open('dia-2-dis\\val-con.txt', mode='w', encoding='utf-8') as val_con:
    for i in val_y:
        val_con.write(i[0])
        val_con.write('\n')

with open('dia-2-dis\\val-father.txt', mode='w', encoding='utf-8') as val_father:
    for i in val_y:
        val_father.write(i[1] if i[1] else 'None')
        val_father.write('\n')

with open('dia-2-dis\\infer-dia.txt', mode='w', encoding='utf-8') as infer_dia:
    for i in infer_x:
        infer_dia.write(i)
        infer_dia.write('\n')

with open('dia-2-dis\\infer-con.txt', mode='w', encoding='utf-8') as infer_con:
    for i in infer_y:
        infer_con.write(i[0])
        infer_con.write('\n')

with open('dia-2-dis\\infer-father.txt', mode='w', encoding='utf-8') as infer_father:
    for i in infer_y:
        infer_father.write(i[1] if i[1] else 'None')
        infer_father.write('\n')
