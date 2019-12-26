# coding=utf-8

r"""
从训练的文件中获取对输入diagnosis候选的概念
"""
import csv
import os

train_concept_f = os.path.abspath('.') + '\\split_data\\dia-desc--dis\\full\\train-con.txt'
with open(train_concept_f, 'r', encoding='utf-8') as txt_f:
    train_con = txt_f.readlines()
train_concept_csv = os.path.abspath('.') + '\\split_data\\dia-desc--dis\\full\\train-con.csv'
output = open(train_concept_csv, mode='w', newline='', encoding='utf-8')
csv_writer = csv.writer(output, dialect='excel')
for row in train_con:
    csv_writer.writerow([row.split('\n')[0]])
print('将train-con.txt转化为train-con.csv成功')