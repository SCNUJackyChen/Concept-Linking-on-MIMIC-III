# coding=utf-8

r"""
- 连接MIMIC-III Postgres数据库;
- 从数据库检索指定的数据
- 保存在本地.csv文件夹
"""

import psycopg2
import csv
from tqdm import *


class Diagnosis2Diseases(object):
    def __init__(self, seq_num):
        """
        获得疾病诊断优先级序号
        :param seq_num: 疾病诊断优先级序号
        """
        self.seq_num = seq_num

    def link_2_postgres(self):
        """
        连接MIMIC-III的Postgres数据库
        :return: postgres数据库操作对象
        """
        postgres = psycopg2.connect(
            database='mimic', user='postgres', password='123456', host='127.0.0.1', port='5432')

        assert postgres, print('无法连接数据库！')

        return postgres

    def query_postgres(self):
        """
        执行SQL语句，查询postgres数据库
        :return: 存储文本数据的list
        """
        postgres = self.link_2_postgres()
        seq_num = "dia_icd = " + str(self.seq_num)
        postgres_obj = postgres.cursor()

        postgres_obj.execute\
            (("""
                set search_path to mimiciii;
                
                select
                    --入院号
                    distinct on(ad.hadm_id)
                    ad.hadm_id,--入院号
                    drg.hadm_id,--入院号
                    note.hadm_id,--入院号
                    dia_icd.hadm_id,--入院号
                    ---以上四个数据理论上是重复的，只是为了检验是否比对一致
                    
                    --信息
                    pa.gender,--性别
                    round((cast(ad.admittime as date)-cast(pa.dob as date))/365.2),--年龄
                    --体重由于inputevents表中的patientsweight只有2万多条，估计是有很多人没有体重这一记录，所以不采用
                    ad.admission_type,--入院类型
                    ad.marital_status,--婚姻状态
                    ad.ethnicity,--人种
                    ad.religion,--宗教信仰
                    --后期可能还需要加入一些医学生理数据的信息
                    
                    --诊断文本
                    ad.diagnosis,--诊断文本
                    drg.description,--诊断相关组文本
                    note.text,--出院总结
                    
                    --疾病码及文本
                    dia_icd.seq_num,--疾病ICD-9码优先级
                    dia_icd.icd9_code,--疾病ICD-9码
                    icd_dia.short_title,--对应ICD-9码的短文本
                    icd_dia.long_title--对应ICD-0码的长文本   
                from
                    admissions as ad,--入院表
                    drgcodes as drg,--诊断相关组表
                    noteevents as note, --注释表
                    patients as pa, --病人表
                    diagnoses_icd as dia_icd, --诊断ICD表
                    d_icd_diagnoses as icd_dia --ICD码对应表
                where
                    ad.hadm_id = drg.hadm_id and
                    ad.hadm_id = note.hadm_id and
                    ad.subject_id = pa.subject_id and
                    icd_dia.icd9_code = dia_icd.icd9_code and
                    ad.hadm_id = dia_icd.hadm_id and
                    dia_icd.seq_num = 1
                    
                    ;
            """))
        # 在数据库中不做判断属性是否为空值的操作，防止检索时间过久
        original_data = postgres_obj.fetchall()
        data = []
        for row in tqdm(original_data, desc='convert data from tuple to list', leave=False):
            check = set(row[0:3])  # 判断前四项的hadm_id属性是否一致
            if len(check) == 1:
                if None not in row:  # 判断每条记录中的每一个属性是否有空值
                    data.append(row[3:])
                else:
                    print('此条记录有空值属性，不添加！')  # 新生儿没有婚姻状态，显然是空值，这种情况要不要排除？
                    print(row)
            else:
                print('此条记录前四项校验失败，不添加！')

        print(len(data))


        for idx, line in enumerate(data):
            print(line)
            assert idx != 10, exit()
        exit()


dia_2_dis = Diagnosis2Diseases(1)
dia_2_dis.query_postgres()
