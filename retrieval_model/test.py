import os
import sys
sys.path.append(os.path.abspath('.'))
from retrieval_model.matching import MatchingModel

model = MatchingModel('diag+desc-con50.csv', 'D:\科研\caml-mimic-master\word2vec\PubMed-shuffle-win-2.bin')
cands = model.query(['infarction'], topk=25)
print(cands)