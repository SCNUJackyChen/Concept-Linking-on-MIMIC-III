from ICD_9_Ontology import ICD_9_Ontology
a = ICD_9_Ontology()
# b = a.get_concept_by_cid('001')
# print(b.get())
# c = b.get_descendants()
# for concept in c:
#     print(concept.get())

b = a.get_concept_by_cid('990')
print(b.get())
print(b.Is_fine_grained())

lis1 = b.get_descendants()
for concept in lis1:
    print(concept.get())
# lis2 = b.get_all_ancestor()
# for concept in lis2:
#     print(concept.get())

#print(b.cid,b.description)
# import xlrd
# import xlwt
# fg = xlrd.open_workbook("fg.xls")
#
# workbook = xlwt.Workbook(encoding='ascii')
# worksheet = workbook.add_sheet('sheet 1')
# current_row = 0
# sheet1 = fg.sheets()[0]
# lis = []
# n = sheet1.nrows
# for i in range(1, n):
#     cid, cd = sheet1.row_values(i)[0], sheet1.row_values(i)[1]
#     if cid[0] == 'E':
#         temp = list(cid)
#         temp.insert(4, '.')
#         cid = ''.join(temp)
#     else:
#         temp = list(cid)
#         temp.insert(3, '.')
#         cid = ''.join(temp)
#     lis.append((cid, cd))
# for concept in lis:
#     worksheet.write(current_row, 0, concept[0])
#     worksheet.write(current_row, 1, concept[1])
#     print('current_row: ',current_row, concept)
#     current_row = current_row + 1
#     workbook.save('temp.xls')








