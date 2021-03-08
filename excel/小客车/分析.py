import xlwt
import xlrd
import re

wb = xlwt.Workbook()
# sheet2 = wb.add_sheet("MyData")

workbook = xlrd.open_workbook('yh1.xlsx')
sheet_names = workbook.sheet_names()
print(sheet_names)
rowsall = 0
# sheet1 = workbook.sheet_by_name(sheet1)
sheet1 = workbook.sheet_by_name("Sheet2")
a = []
for r in range(sheet1.nrows):
    rows = sheet1.row_values(r)
    # print(rows)
    a.append(rows[1])
# print(a)
b = []
c = []
w = 0
f = {}
for i in range(80):
    w = 0
    if (i >70 and i < 80):
        for k in a:
            # if (k>=i*10 and (k < (i+1)*10)):
            if k == i:
                w = w +1
        b.append(w)
        c.append(i)
        f[i] = w


print(c)
print(b)
print(f)
print(72>7*10 and (72 < (7+1)*10))