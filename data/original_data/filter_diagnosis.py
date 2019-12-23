# coding=utf-8

r"""
过滤提纯从MIMIC-III数据库提取出来的diagnosis-2-disease.csv文件或者diagnosis-2-procedure.py文件，主要是过滤掉不符合要求的diagnosis项
不符合要求的diagnosis项指的是diagnosis只含单个英文字符，如 s p fall等这类情况
"""

import os
import csv
import re


dia_dis = os.path.abspath('.') + '\\diagnosis-2-disease.csv'
dia_dis_filter = os.path.abspath('.') + '\\diagnosis-2-disease-filter.csv'
dia_pro = os.path.abspath('.') + '\\diagnosis-2-procedure.csv'
dia_pro_filter = os.path.abspath('.') + '\\diagnosis-2-procedure-filter.csv'


def filter_dia(line):
    """
    过滤diagnosis不符合要求的csv行
    :param line: csv某一行
    :return: 是否要删除这一行
    """
    line_split = line[0].split(' ')  # 先切分diagnosis

    if len(line_split) == 1:  # 切分后只有一个单词的
        if len(line_split[0]) <= 3:  # 只有一个单词的情况下，单词的长度小于等于3，认为是无意义的单词，删除这条line
            return False
        else:
            return True

    elif len(line_split) == 2:  # 切分后有两个单词的
        for i in line_split:  # 有一个单词只有一个字符
            if len(i) == 1:
                return False
        return True

    elif len(line_split) == 3:  # 切分后有三个单词的
        one_count = 0  # 长度为1的字符计数
        for i in line_split:
            if len(i) == 1:
                one_count += 1
            if one_count == 2:  # 如果该条只有三个字符，同时有两个都是一个单独字母的，认为此条无效
                return False
        return True
    else:
        return True  # 不是以上三种情况则保留


def filter_diagnosis(src_file, filter_file):
    """
    读入原始的diagnosis-2-xxx.csv文件，使用过滤规则过滤diagnosis，重新写出过滤后的新文件
    :param src_file: 原始diagnosis-2-xxx.csv文件。
    :param filter_file: 写出的新文件
    :return: 打印原始文件条数，过滤后的文件条数
    """
    dia_xxx_f = csv.reader(open(src_file, 'r'))
    save_line = []
    for idx, line in enumerate(dia_xxx_f):
        if filter_dia(line):
            save_line.append(line)

    output = open(filter_file, mode='w', newline='', encoding='utf-8')
    csv_writer = csv.writer(output, dialect='excel')
    for row in save_line:
        csv_writer.writerow(row)

    print('原始文件条数{}，过滤后的文件条数{}！'.format(idx, len(save_line)))


filter_diagnosis(dia_dis, dia_dis_filter)
filter_diagnosis(dia_pro, dia_pro_filter)
