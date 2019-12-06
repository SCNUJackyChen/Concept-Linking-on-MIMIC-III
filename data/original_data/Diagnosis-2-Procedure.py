# coding=utf-8

r"""
- 连接MIMIC-III Postgres数据库;
- 从数据库检索指定的数据
- 保存在本地.csv文件夹
"""

import psycopg2
import csv
from tqdm import *
import re
import locale
import decimal
from decimal import Decimal
from ICD_9_procedure import ICD_9_Procedure, Concept
import csv
import os


class Diagnosis2Procedure(object):
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

        postgres_obj.execute \
            (("""
                set search_path to mimiciii;

                select
                    --入院号
                    distinct on(ad.hadm_id)
                    ad.hadm_id,--入院号
                    drg.hadm_id,--入院号
                    note.hadm_id,--入院号
                    pro_icd.hadm_id,--入院号
                    ---以上四个数据理论上是重复的，只是为了检验是否比对一致

                    --信息
                    pa.gender,--性别
                    round((cast(ad.admittime as date)-cast(pa.dob as date))/365.2) as age,--年龄
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
                    pro_icd.seq_num,--疾病ICD-9码优先级
                    pro_icd.icd9_code,--疾病ICD-9码
                    icd_pro.short_title,--对应ICD-9码的短文本
                    icd_pro.long_title--对应ICD-0码的长文本   
                from
                    admissions as ad,--入院表
                    drgcodes as drg,--诊断相关组表
                    noteevents as note, --注释表
                    patients as pa, --病人表
                    procedures_icd as pro_icd, --诊断ICD表
                    d_icd_procedures as icd_pro --ICD码对应表
                where
                    ad.hadm_id = drg.hadm_id and
                    ad.hadm_id = note.hadm_id and
                    ad.subject_id = pa.subject_id and
                    icd_pro.icd9_code = pro_icd.icd9_code and
                    ad.hadm_id = pro_icd.hadm_id and
                    pro_icd.seq_num = 1
                    ;
            """))
        # 在数据库中不做判断属性是否为空值的操作，防止检索时间过久
        original_data = postgres_obj.fetchall()
        data = []
        for row in tqdm(original_data, desc='convert data from tuple to list', leave=False):
            check = set(row[0:3])  # 判断前四项的hadm_id属性是否一致
            if len(check) == 1:
                if None not in row:  # 判断每条记录中的每一个属性是否有空值
                    data.append(list(row[3:]))
                else:
                    print('此条记录有空值属性，不添加！')  # 新生儿没有婚姻状态，显然是空值，这种情况要不要排除？
                    # print(row)
            else:
                print('此条记录前四项校验失败，不添加！')

        print('筛选后的数据条数为{}'.format(len(data)))
        print('展示数据前10条')
        for idx, line in enumerate(data):
            print(line)
            if idx >= 10:
                break
        return data

    def _normalize_text(self, text):
        """
        # 对于文本做去除无关字符的处理
        :param text: 原始文本
        :return: 处理过后的文本
        """
        text = text.lower().strip()
        text = re.sub(r"([.!?])", r" \1", text)
        text = re.sub(r"[^a-zA-Z]+", r" ", text)

        return text

    def age_2_word(self, number):
        """
        年龄数字到文本的变换
        :param number: 输入的年龄数字
        :return: 数值化的年龄
        """
        NUMBER_CONSTANT = {0: "zero ", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven",
                           8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen",
                           14: "fourteen", 15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen",
                           19: "nineteen"}
        IN_HUNDRED_CONSTANT = {2: "twenty", 3: "thirty", 4: "forty", 5: "fifty", 6: "sixty", 7: "seventy", 8: "eighty",
                               9: "ninety"}
        BASE_CONSTANT = {0: " ", 1: "hundred", 2: "thousand", 3: "million", 4: "billion"}
        if str(number).isnumeric():
            if str(number)[0] == '0' and len(str(number)) > 1:
                return self.age_2_word(int(number[1:]))
            if int(number) < 20:
                return NUMBER_CONSTANT[int(number)]
            elif int(number) < 100:
                if str(number)[1] == '0':
                    return IN_HUNDRED_CONSTANT[int(str(number)[0])]
                else:
                    return IN_HUNDRED_CONSTANT[int(str(number)[0])] + "-" + NUMBER_CONSTANT[int(str(number)[1])]
            else:
                locale.setlocale(locale.LC_ALL, "English_United States.1252")
                strNumber = locale.format("%d", number, grouping=True)
                numberArray = str(strNumber).split(",")
                stringResult = ""
                groupCount = len(numberArray) + 1
                for groupNumber in numberArray:
                    if groupCount > 1 and groupNumber[0:] != "000":
                        stringResult += str(self.getUnderThreeNumberString(str(groupNumber))) + " "
                    else:
                        break
                    groupCount -= 1
                    if groupCount > 1:
                        stringResult += BASE_CONSTANT[groupCount] + ","
                endPoint = len(stringResult) - len(" hundred,")
                return stringResult

        else:
            print("please input a number!")

    def getUnderThreeNumberString(self, number):
        NUMBER_CONSTANT = {0: "zero ", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven",
                           8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen",
                           14: "fourteen", 15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen",
                           19: "nineteen"}
        IN_HUNDRED_CONSTANT = {2: "twenty", 3: "thirty", 4: "forty", 5: "fifty", 6: "sixty", 7: "seventy", 8: "eighty",
                               9: "ninety"}
        BASE_CONSTANT = {0: " ", 1: "hundred", 2: "thousand", 3: "million", 4: "billion"}
        if str(number).isnumeric() and len(number) < 4:
            if len(number) < 3:
                return self.age_2_word(int(number));
            elif len(number) == 3 and number[0:] == "000":
                return " ";
            elif len(number) == 3 and number[1:] == "00":
                return NUMBER_CONSTANT[int(number[0])] + "  " + BASE_CONSTANT[1];
            else:
                return NUMBER_CONSTANT[int(number[0])] + "  " + BASE_CONSTANT[
                    1] + " and " + self.age_2_word((number[1:]));
        else:
            print("number must below 1000");

    def process_text(self, data):
        """
        处理从postgres数据库中检索出的文本数据
        :return: 返回处理过的数据存储list
        """
        process_data = []
        icd_9_pro = ICD_9_Procedure()  # 声明ICD-9疾病本体对象

        for line in tqdm(data, desc='处理数据中...', leave=False):
            one = []
            one.append(self._normalize_text(line[7]))  # 诊断文本处理
            one.append(self._normalize_text(line[8]))  # 诊断相关组文本处理
            one.append(line[9])  # TODO 出院总结文本待处理
            one.append('female' if line[1] == 'f' else 'male')  # 性别处理
            age = int(float(str((line[2]).quantize(Decimal('0.0'))).split("'")[0]))  # 年龄从字符转化为数值
            one.append(self._normalize_text(self.age_2_word(age if age == 89 else age)))  # 年龄处理
            for item in range(3, 7, 1):
                one.append(self._normalize_text(line[item]))  # 入院类型、婚姻状态、人种、宗教信仰处理
            one.append(self._normalize_text(line[12]))  # ICD-9码短文本处理
            one.append(self._normalize_text(line[13]))  # ICD-9码长文本处理
            icd9_code = line[11]  # ICD-9编码处理 TODO 换成Procedure之后编码转化出现问题，待修改
            if 'E' not in icd9_code:
                if len(icd9_code) >= 4:
                    icd9_code = icd9_code[:2] + '.' + icd9_code[2:]
                else:
                    icd9_code = icd9_code[:2] + '.' + icd9_code[2:]
            else:
                if len(icd9_code) > 4:
                    icd9_code = icd9_code[:4] + '.' + icd9_code[4:]
            one.append(icd9_code)
            procedure = icd_9_pro.get_concept_by_cid(icd9_code)  # 获取ICD-9码对应的文本
            one.append(self._normalize_text(procedure.get()[1]))
            procedure_fathers = procedure.get_all_ancestor()  # 回溯ICD-9码的父概念及其文本
            for father in procedure_fathers:
                one.append(father.get()[0])
                one.append(self._normalize_text(father.get()[1]))
            process_data.append(one)
        return process_data


dia_2_pro = Diagnosis2Procedure(1)  # 数据类对象
dia_2_pro_data = dia_2_pro.query_postgres()  # 查询数据库
process_data = dia_2_pro.process_text(dia_2_pro_data)  # 处理文本
file_path = os.getcwd() + '\\'
title = [['diagnosis', 'description', 'text', 'gender', 'age', 'admission-type', 'marry status', 'ethnicity',
          'religion', 'short-title', 'long-title', 'icd9-code',
          'icd9-code text', 'father icd9-code', 'father icd9-code text', 'Last two items in loop']]
total_text = title + process_data

output = open((file_path + 'diagnosis-2-procedure' + '.csv'), mode='w', newline='', encoding='utf-8')  # 写成.csv文件
csv_writer = csv.writer(output, dialect='excel')
for row in tqdm(total_text, desc='开始写入csv文件...', leave=False):
    csv_writer.writerow(row)
print('成功写入diagnosis-2-procedure.csv文件！')

exit()
with open('diagnosi-2-disease.txt', mode='w', encoding='utf-8') as txt_file:
    for row in tqdm(total_text, desc='开始写入txt文件...', leave=False):
        for item in row:
            txt_file.write(item)
            txt_file.write(' ')
        txt_file.write('\n')
print('成功写入diagnosis-2-diseases.txt文件！')



