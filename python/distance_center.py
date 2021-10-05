# 编写人：谭神冬
# 座右铭：安然度日
# 时间： 2021/5/27 22:07
# 脚本意义：计算指定原子团的质心到液滴质心的距离
# 使用方法：python [输入文件] [输出文件] [初始帧数] [终止帧数] [有机物原子数] [运行核数] [原子团个数i] [index_1] [index_2] [index_i]
import sys
import numpy as np
from multiprocessing import Pool
input_file = str(sys.argv[1])   # 输入文件
output_file = str(sys.argv[2])  # 输出文件
cal_init = int(sys.argv[3])     # 初始帧数
cal_fina = int(sys.argv[4])     # 终止帧数
org_num = int(sys.argv[5])      # 有机物原子数
core = int(sys.argv[6])         # 运行核数选择
def read_lines(num):  # 读入文件坐标储存到列表res
    filename = input_file  # 输入文件
    with open(filename) as f:
        content = f.readlines()
        lines = list(map(lambda x: x.strip(), content))
        res = [x for x in lines[(num - 1) * (int(lines[0]) + 2)+2:num * (int(lines[0]) + 2)]]
    return res
def center_mass(all):  # 质心计算公式
    masses = np.array(all)
    nonZeroMasses = masses[np.nonzero(masses[:, 3])]
    CM = np.average(nonZeroMasses[:, :3], axis=0, weights=nonZeroMasses[:, 3])  # 质量权重，求得质心坐标
    return CM
def merge(i):  # 坐标原子加权分类
    atom = i.split()
    if atom[0] == 'H':
        atom_xyz = [float(atom[1]), float(atom[2]), float(atom[3]), 1.007947]
    elif atom[0] == 'O':
        atom_xyz = [float(atom[1]), float(atom[2]), float(atom[3]), 15.99943]
    else:
        atom_xyz = [float(atom[1]), float(atom[2]), float(atom[3]), 12.01078]
    return atom_xyz
def distance(frame):  # 指定原子团簇质心坐标到液滴质心的距离
    WA = []
    org = []
    l = []
    for i in frame[0:int(len(frame)-org_num)]:    # 12：有机物原子个数
        atom_xyz = merge(i)
        WA.append(atom_xyz)
    list_sp = [int(sys.argv[x + 8]) for x in range(int(sys.argv[7]))]
    for j in [frame[i] for i in list_sp]:
        atom_xyz = merge(j)
        org.append(atom_xyz)
    CM_water = center_mass(WA)
    CM_org = center_mass(org)
    vector1 = np.array(CM_water)
    vector2 = np.array(CM_org)
    l_d = np.sqrt(np.sum(np.square(vector1 - vector2)))  # 两点距离计算
    l.append(l_d)
    print(CM_water)
    print(CM_org)
    return l

if __name__ == '__main__':
    p = Pool(core)     # 调用核数
    res1 = p.map(read_lines,range(cal_init,cal_fina))   # 帧数选择
    res2 = p.map(distance,res1)
    doc = open(output_file, 'w')  # 输出文件
    for h in res2:
      print(h,file = doc)
    doc.close()
    print('你好呀，质心距离计算已经完成')
