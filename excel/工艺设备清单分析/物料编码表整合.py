import xlwt
import xlrd
import re

wb = xlwt.Workbook()
sheet2 = wb.add_sheet("MyData")

workbook = xlrd.open_workbook('公司物料代码编码表.xlsx')
sheet_names = workbook.sheet_names()
print(type(sheet_names))
rowsall = 0
for name in sheet_names:
    print(name)
    sheet1 = workbook.sheet_by_name(name)
    for r in range(sheet1.nrows):
        rows = sheet1.row_values(r)

        matchobj = re.match(r'[A-Za-z]+', rows[1], re.I)
        if matchobj:
            # print(rows[1])
            if rows[1] != "":
                rowsall = rowsall + 1
                for i in range(len(rows)):
                    sheet2.write(rowsall, i, rows[i])

wb.save('e.xls')
