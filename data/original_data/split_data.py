# coding=utf-8

r"""
对于处理过的数据拆分为训练（父概念）、验证（父概念）和测试（父概念）数据，包括diagnosis--disease和diagnosis--procedure
"""

import csv
import numpy as np
import os
from tqdm import *
from sklearn.model_selection import KFold, train_test_split
from functools import reduce
import sys
sys.path.append(os.path.abspath('..'))
from data.data_visual.data_visual_map import InputTargetLengthVisual


def split_data(src_file, un_repeat, add_dia, add_desc, add_text, add_father, father, max_len, out_path):
    """
    读取diagnosis-2-xxx.csv文件，分离数据为训练、验证和测试数据，每一个都附带父概念
    :param src_file: 源文件路径
    :param un_repeat: 是否对diagnosis序列进行去重
    :param add_dia: 是否添加diagnosis序列
    :param add_desc: 是否添加description序列
    :param add_text:· 是否添加text序列
    :param add_father: 是否添加father序列再concept后面
    :param father: 是否单独写出concept对应的father序列
    :param max_len: diagnosis综合序列的最大序列长度
    :param out_path: 处理完写出文件的相对路径
    :return:
    """
    text_data = csv.reader(open(src_file, 'r'))
    diagnosis = []  # 诊断集
    concept = []  # 概念集
    fathers = []  # 父概念集
    un_repeat_con = []  # 存放无重复的概念集
    for idx, line in enumerate(text_data):
        if idx != 0:  # 第一行不读取
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

    show = InputTargetLengthVisual(diagnosis, concept)  # 序列画图
    show.show()

    train_x, val_infer_x, train_y, val_infer_y = train_test_split(  # 分离训练数据、验证-测试数据，默认比例9:1
        diagnosis, concept, train_size=0.9, test_size=0.1, shuffle=True, random_state=2019)
    val_x, infer_x, val_y, infer_y = train_test_split(  # 分离验证、测试数据，默认比例9:1
        val_infer_x, val_infer_y, train_size=0.2, test_size=0.8, shuffle=True, random_state=2019)

    with open(out_path + '\\train-dia.txt', mode='w', encoding='utf-8') as train_dia:  # 写训练diagnosis数据
        for idx, i in enumerate(train_x):
            train_dia.write(i)
            if idx != len(train_x) - 1:
                train_dia.write('\n')
    with open(out_path + '\\train-con.txt', mode='w', encoding='utf-8') as train_con:  # 写训练concept数据
        for idx, i in enumerate(train_y):
            train_con.write(i[0])
            if idx != len(train_y) - 1:
                train_con.write('\n')
    with open(out_path + '\\train-father.txt', mode='w', encoding='utf-8') as train_father:  # 写选了concept父概念数据
        for idx, i in enumerate(train_y):
            train_father.write(i[1] if i[1] else 'none')
            if idx != len(train_y) - 1:
                train_father.write('\n')

    with open(out_path + '\\val-dia.txt', mode='w', encoding='utf-8') as val_dia:  # 写验证diagnosis数据
        for idx, i in enumerate(val_x):
            val_dia.write(i)
            if idx != len(val_x) - 1:
                val_dia.write('\n')
    with open(out_path + '\\val-con.txt', mode='w', encoding='utf-8') as val_con:  # 写验证concept数据
        for idx, i in enumerate(val_y):
            val_con.write(i[0])
            if idx != len(val_y) - 1:
                val_con.write('\n')
    with open(out_path + '\\val-father.txt', mode='w', encoding='utf-8') as val_father:  # 写验证concept父概念数据
        for idx, i in enumerate(val_y):
            val_father.write(i[1] if i[1] else 'none')
            if idx != len(val_y) - 1:
                val_father.write('\n')

    with open(out_path + '\\infer-dia.txt', mode='w', encoding='utf-8') as infer_dia:  # 写测试diagnosis数据
        for idx, i in enumerate(infer_x):
            infer_dia.write(i)
            if idx != len(infer_x) - 1:
                infer_dia.write('\n')
    with open(out_path + '\\infer-con.txt', mode='w', encoding='utf-8') as infer_con:  # 写测试concept数据
        for idx, i in enumerate(infer_y):
            infer_con.write(i[0])
            if idx != len(val_infer_y) - 1:
                infer_con.write('\n')
    with open(out_path + '\\infer-father.txt', mode='w', encoding='utf-8') as infer_father:  # 写测试concept父概念数据
        for idx, i in enumerate(infer_y):
            infer_father.write(i[1] if i[1] else 'none')
            if idx != len(infer_y) - 1:
                infer_father.write('\n')

    print('处理并写出数据完成\n')


src_path = os.path.abspath('.') + '\\processed_data\\'
tgt_path = os.path.abspath('.') + '\\split_data\\'
disease_or_procedure = 'procedure'

if disease_or_procedure == 'disease':
    # 写diagnosis--disease全数据
    full_file = src_path + 'diagnosis-2-disease-filter.csv'
    out_path = tgt_path + 'dia--dis\\full'
    split_data(full_file, False, True, False, False, False, True, 100, out_path)

    # 写diagnosis--disease top50数据
    full_file = src_path + 'diagnosis-2-disease-filter-50.csv'
    out_path = tgt_path + 'dia--dis\\top50'
    split_data(full_file, False, True, False, False, False, True, 100, out_path)

    # 写diagnosis+description--disease 全数据
    full_file = src_path + 'diagnosis-2-disease-filter.csv'
    out_path = tgt_path + 'dia-desc--dis\\full'
    split_data(full_file, False, True, True, False, False, True, 100, out_path)

    # 写diagnosis+description--disease top50数据
    full_file = src_path + 'diagnosis-2-disease-filter-50.csv'
    out_path = tgt_path + 'dia-desc--dis\\top50'
    split_data(full_file, False, True, True, False, False, True, 100, out_path)
else:
    # 写diagnosis--procedure 全数据
    full_file = src_path + 'diagnosis-2-procedure-filter.csv'
    out_path = tgt_path + 'dia--pro\\full'
    split_data(full_file, False, True, False, False, False, True, 100, out_path)

    # 写diagnosis--procedure top50数据
    full_file = src_path + 'diagnosis-2-procedure-filter-50.csv'
    out_path = tgt_path + 'dia--pro\\top50'
    split_data(full_file, False, True, False, False, False, True, 100, out_path)

    # 写diagnosis+description--procedure 全数据
    full_file = src_path + 'diagnosis-2-procedure-filter.csv'
    out_path = tgt_path + 'dia-desc--pro\\full'
    split_data(full_file, False, True, True, False, False, True, 100, out_path)

    # 写diagnosis+description--procedure top50数据
    full_file = src_path + 'diagnosis-2-procedure-filter-50.csv'
    out_path = tgt_path + 'dia-desc--pro\\top50'
    split_data(full_file, False, True, True, False, False, True, 100, out_path)
