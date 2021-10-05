# 编写人：谭神冬
# 座右铭：安然度日
# 时间： 2021/5/25 22:09
# 使用方法：python [脚本名] [输入文件] [输出文件] [初始帧数] [终止帧数]
import numpy as np
import math
import sys
imput_file = str(sys.argv[1])   # 输入文件
output_file = str(sys.argv[2])  # 输出文件
cal_init = int(sys.argv[3])     # 初始帧数
cal_fina = int(sys.argv[4])     # 终止帧数
from multiprocessing import Pool
def read_lines(filename):
    with open (filename) as f:
        content = f.readlines()
        lines = list(map(lambda x: x.strip(), content))
    return lines
def insert(num): # 读取坐标文件，放入列表中
    filename_all = imput_file # 输入文件，按所需修改
    lines = read_lines(filename_all)
    res = [x for x in lines[(num-1)*(int(lines[0])+2):num*(int(lines[0])+2)]]
    S_coord = read_lines(str(sys.argv[5]))
    res.append(S_coord[num-1])
    return res
def text_save(num):  # filename为写入txt文件的路径，data为要写入数据列表.
    filename = output_file
    file = open(filename, 'a')
    data = insert(num)
    for i in range(len(data)):
        s = str(data[i]).replace('[', '').replace(']', '')  # 去除[],这两行按数据不同，可以选择
        s = s.replace("'", '').replace(',', '') + '\n'  # 去除单引号，逗号，每行末尾追加换行符
        file.write(s)
    file.close()

if __name__ == '__main__':
     p = Pool(1)
     res1 = p.map(text_save,range(cal_init,cal_fina))
     print('恭喜你，插入成功啦')
