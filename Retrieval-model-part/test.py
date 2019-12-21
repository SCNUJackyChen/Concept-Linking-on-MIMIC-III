import matching

model = matching.MatchingModel('diag+desc-con50.csv','to/your/path/model.bin')
cands = model.query(['infarction'],topk=25)
print(cands)
