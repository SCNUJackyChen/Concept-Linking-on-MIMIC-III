import matching
import os

model = matching.MatchingModel('diag+desc-con50.csv', os.path.abspath('.') + '\\BioNLP-word-embedding.bin')
cands = model.query(['infarction'], topk=25)
print(cands)