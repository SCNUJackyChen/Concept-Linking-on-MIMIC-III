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
        :return:
        """
        postgres = self.link_2_postgres()
        seq_num = "dia_icd = " + str(self.seq_num)
        postgres_obj = postgres.cursor()

        postgres_obj.execute\
            (("""
                set search_path to mimiciii;
                
                select
                    --distinct on(ad.hadm_id)
                    --ad.hadm_id,
                    --ad.subject_id,
                    --distinct on(ad.hadm_id)
                    ad.hadm_id,
                    --distinct on(note.hadm_id)
                    --pa.gender,
                    --inmv.patientweight,
                    ad.diagnosis,
                    dia_icd.icd9_code,
                    dia_icd.seq_num
                    --drg.description,
                    --note.hadm_id,
                    --drg.hadm_id
                    --note.text
                    --drg.description,
                    --note.text    
                from
                    admissions as ad,--入院表
                    drgcodes as drg,--诊断相关组表
                    noteevents as note,--注释表
                    patients as pa,--病人表
                    inputevents_mv as inmv, --输入表
                    diagnoses_icd as dia_icd --诊断ICD表
                    d_icd_diagnosis as icd_dia --诊断ICD码对应表
                where
                    --ad.hadm_id = drg.hadm_id and
                    --ad.hadm_id = note.hadm_id
                    --ad.subject_id = pa.subject_id and
                    --pa.subject_id = inmv.subject_id --先以subject_id连接pa表格inmv表，检查数量，25110条，太少放弃
                    --ad.hadm_id = inmv.hadm_id --以hadm_id连接ad表和inmv表，21879条，为什么这么少呢？
                    ad.hadm_id = dia_icd.hadm_id and --以hadm_id连接ad表和dia_icd表
                    dia_icd.seq_num = 1
                                
                            ;
            """))
        original_data = postgres_obj.fetchall()
        data = []
        for row in tqdm(original_data, desc='convert data from tuple to list', leave=False):
            if row[0] is not None:
                data.append(list(row))
        print(len(data))


        for idx, line in enumerate(data):
            print(line)
            assert idx != 10, exit()
        exit()


dia_2_dis = Diagnosis2Diseases(1)
dia_2_dis.query_postgres()

"""
set search_path to mimiciii;
                            CREATE INDEX test_index ON noteevents(hadm_id);
                            select 
                                --distinct on (note.hadm_id)
                                note.hadm_id as "入院号",
                                ad.hadm_id as "入院号",
                                drg.hadm_id as "入院号"
                                /*
                                round( (cast(ad.admittime as date)-cast(pa.dob as date))/365.2, 0) as "年龄",
                                inmv.patientweight as "体重",
                                pa.gender as "性别",
                                ad.admission_type as "入院类型",
                                ad.insurance as "保险状态",
                                ad.religion as "宗教信仰",
                                ad.marital_status as "婚姻状态",
                                ad.ethnicity as "人种",
                        
                                ad.diagnosis as "入院诊断短文本",
                                drg.description as "病人诊断相关组短文本",
                                note.text as "出院病人总结报告长文本",
                                
                                dia.seq_num as "病人诊断疾病优先级",
                                dia.icd9_code as "诊断疾病对应的ICD-9编码",
                                icd_dia.short_title as "疾病ICD-9编码对应的短文本描述",
                                icd_dia.long_title as "疾病ICD-9编码对应的长文本描述"
                                */
                            from
                                admissions as ad, --入院表
                                noteevents as note, --病人注释表
                                drgcodes as drg, --诊断相关组表
                                inputevents_mv as inmv, --输入表
                                patients as pa, --病人表
                                diagnoses_icd as dia, --病人ICD疾病表
                                d_icd_diagnoses as icd_dia --ICD-9疾病描述表
                            where
                                ad.hadm_id = note.hadm_id and
                                drg.hadm_id = ad.hadm_id and
                                drg.hadm_id = note.hadm_id and
                                inmv.hadm_id = ad.hadm_id and
                                ad.subject_id = pa.subject_id and
                                dia.hadm_id = ad.hadm_id and
                                dia.seq_num = 1 and
                                icd_dia.icd9_code = dia.icd9_code 
"""
