# 编写人：谭神冬
# 座右铭：安然度日
# 时间： 2021/6/22 10:20
import xlrd
import sys
cal_init = int(sys.argv[1])     # 初始帧数
cal_fina = int(sys.argv[2])     # 终止帧数
input_file = str(sys.argv[3])   # 输入文件
output_file = str(sys.argv[2])  # 输出文件
# file = 'C:/Users/Lenovo/Desktop/96LA.xlsx'
def read_excel(num):
    wb = xlrd.open_workbook(filename=input_file)  # 打开文件
    sheet1 = wb.sheet_by_index(0)  # 通过索引获取表格
    rows = sheet1.row_values(num)  # 获取行内容
    return rows
intervals = {'{:0>6.2f}-{:0>6.2f}'.format(5*x,5*(x+1)):0 for x in range(16)}
intervals1 = {'{:0>6.2f}-{:0>6.2f}'.format(5*x,5*(x+1)):0 for x in range(16)}
for i in range(cal_init,cal_fina):
    data = read_excel(i)
    list = float(data[1])
    for interval in intervals:
      start,end = tuple(interval.split('-'))
      if float(start)<=list<float(end):
          intervals[interval] = int(intervals[interval]) + int(data[0])
          intervals1[interval] += 1
print(intervals)
print(intervals1)

doc = open(output_file, 'w')  # 输出文件
for h in intervals:
    print(h,'\t', intervals[h],'\t',intervals1[h], file=doc)
doc.close()
