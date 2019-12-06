from ICD_9_procedure import ICD_9_Procedure, Concept
a = ICD_9_Procedure()
b = a.get_concept_by_cid('99.9')
print(b.get())

lis = b.get_descendants()
for concept in lis:
    print(concept.get())

