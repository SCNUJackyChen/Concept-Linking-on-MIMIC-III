#  MIMIC-III数据库概念连接项目匹配模型部分
## 介绍
这个模块为了生成模型服务，它的功能在于短时间内快速筛选出包含有目标医疗概念的候选集，
是一种粗略的检索方法。经过匹配模型的预处理，选出与查询最相似的top K个概念。
## 方法
对于医疗文本，我们采取BioNLP作为预训练好的词向量，利用SIF方法计算每条文本的句向量，
再利用余弦相似度筛选出与查询最相似的top K个候选概念。
## 精度
在top-50数据集上，表现如下（覆盖率=候选集中包含正确对应概念的查询数/总查询数）
 TOP-50  Code dataset | TFIDF | SIF+CBOW | SIF+BioNLP 
 --- | --- | --- | ---
 top5                 | 0.72  | 0.68     | **0.79**   
 top10                | 0.8   | 0.78     | **0.88**   
 top15                | 0.85  | 0.84     | **0.93**   
 top20                | 0.87  | 0.88     | **0.95**   
 top25                | 0.92  | 0.94     | **0.97**   

  表头  | 表头 
  ------------- | ------------- 
 单元格内容  | 单元格内容 
 单元格内容l  | 单元格内容

#  MIMIC-III Concept Linking -- Retrieval-Model-Part
## Introduction
This module serves the Generation-model part. It is a light-weighted and rough retrieval method that
aims to sift through the concepts set and narrow
down the size of candidates of concepts in an efficient way. Given a query, this module will
generate the most similar top K concepts of it.

## Method
For clinic text, we leverage BioNLP as pre-trained word embeddings, and SIF method is used
for calculating sentence embeddings for each text. Finally, the cosine similarity has been
computed in order to search for the top K candidates of concepts.

## Precision
In the top-50 dataset, our method has the following performance.
(The number represents coverage of top K candidates, which means the ratio of how many queries can
get their corresponding concepts in top K. e.g, top5-0.79 means 79% of the queries in dataset
can find their corresponding concepts in top 5 candidates.)
 TOP-50  Code dataset | TFIDF | SIF+CBOW | SIF+BioNLP 
 -------------------- | ----- | -------- | ---------- 
 top5                 | 0.72  | 0.68     | **0.79**   
 top10                | 0.8   | 0.78     | **0.88**   
 top15                | 0.85  | 0.84     | **0.93**   
 top20                | 0.87  | 0.88     | **0.95**   
 top25                | 0.92  | 0.94     | **0.97**   
