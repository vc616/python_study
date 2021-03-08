import xlwt
import xlrd
import re
import pandas as pd
import numpy
df1 = pd.read_excel(
    "G:/users/VC/PycharmProjects/Pycharm_all/to_github/excel/物料表格整理/ABB.xlsx",
    sheet_name="'ABB-施耐德'")

# wb = xlwt.Workbook()
# sheet2 = wb.add_sheet("MyData")

# workbook = xlrd.open_workbook("G:/users/VC/PycharmProjects/Pycharm_all/to_github/excel/物料表格整理/ABB.xlsx")
# sheet_names = workbook.sheet_names()
# print(sheet_names)
# sheet1 = workbook.sheet_by_name(sheet_names[0])
# for r in range(sheet1.nrows):
#     rows = sheet1.row_values(r)
#     print(rows)
#         # matchobj = re.match(r'[A-Za-z]+', rows[1], re.I)
#         # if matchobj:
#         #     # print(rows[1])
#         #     if rows[1] != "":
#         #         rowsall = rowsall + 1
#         #         for i in range(len(rows)):
#         #             sheet2.write(rowsall, i, rows[i])