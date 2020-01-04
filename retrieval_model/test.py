import os
import sys
sys.path.append(os.path.abspath('.'))
from retrieval_model.matching import MatchingModel

model = MatchingModel('diag+desc-con50.csv', os.path.abspath('.') + '\\BioNLP-word-embedding.bin')
cands = model.query(['infarction'], topk=25)
print(cands)