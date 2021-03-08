# 将物料代码表多个表汇总到一个表格，方便导入到filemaker数据库

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

# sheet1 = workbook.sheet_by_index(5) # sheet索引从0开始
# print(sheet1.name, sheet1.nrows, sheet1.ncols)
# rows = sheet1.row_values(1389)
# cols = sheet1.col_values(1) # 获取第1列内容
# print(rows)
# print(cols)

# sheet1 = wb.add_sheet("MyData")
# for q in range()
# for i in range(len(rows)):
#     sheet1.write(1,i,rows[i])
# wb.save('e.xls')
