# 编写人：谭神冬
# 座右铭：question keep answer
# 时间： 2021/5/23 21:33
# 脚本介绍：计算液滴质心到表面的密度变化，目的是确定液滴的半径
# 使用方法：python [脚本名] [有机物原子数] [壳层间隔距离] [预测液滴半径] [运行核数] [初始帧数] [终止帧数]
import numpy as np
import math
import sys
from multiprocessing import Pool
num_org = int(sys.argv[1])   # num_org:有机物的原子数
inter = float(sys.argv[2])   # 间隔距离，可取0.1~1等，建议取值0.5
r = float(sys.argv[3])       # 预测可取半径，根据液滴尺寸选择
core = int(sys.argv[4])      # 运行核数选择
cal_init = int(sys.argv[5])  # 初始帧数
cal_fina = int(sys.argv[6])  # 终止帧数
def read_lines(num): # 读取坐标文件，放入列表中
  filename = 'C:/Users/Lenovo/Desktop/in.xyz' # 输入文件，按所需修改
  with open (filename) as f:
    content = f.readlines()
    lines = list(map(lambda x: x.strip(), content)) 
    res = [x for x in lines[(num-1)*(int(lines[0])+2):num*(int(lines[0])+2)-num_org]]
  return res
def center_mass(frame): # 计算每个水分子到质心的距离（第一步计算质心坐标，第二步计算每个水分子坐标到质心的距离）
  all = []
  l = []
  for i in frame[0:int(frame[0])+2-num_org]:  # 相应帧的水质心的计算 num_org:有机物的原子数
    if i[0]=='H':
      atom = i.split()
      H_xyz = [float(atom[1]),float(atom[2]),float(atom[3]),1.007947]
      all.append(H_xyz)
    elif i[0]=='O':
      atom = i.split()
      O_xyz = [float(atom[1]),float(atom[2]),float(atom[3]),15.99943]
      all.append(O_xyz)
  masses = np.array(all)
  nonZeroMasses = masses[np.nonzero(masses[:,3])]
  CM = np.average(nonZeroMasses[:,:3], axis=0, weights=nonZeroMasses[:,3])  # 质量权重，求得质心坐标
  for j in frame[0:int(frame[0])+2-num_org]:  # 所有水与质心的距离计算
    if j[0]=='O':
      atom = j.split()
      vector1 = np.array([float(atom[1]),float(atom[2]),float(atom[3])])
      vector2 = np.array(CM)
      l_d = np.sqrt(np.sum(np.square(vector1 - vector2)))  # 两点距离计算
      l.append(l_d)
  return l
def cata(data): # 对距离的大小进行数值分类
  intervals = {'{:0>6.2f}-{:0>6.2f}'.format(inter*x,inter*(x+1)):0 for x in range(int(r/inter))}
  for list in data:
      for interval in intervals:
          start,end = tuple(interval.split('-'))
          if float(start)<=list<=float(end):
              intervals[interval] +=1
  return intervals
def density(item):  # 个数转化成密度
    for k in item:
        NA = 6.02 * 0.1
        item[k] = (item[k]*18*3)/(NA*4*math.pi*((float(k[-4:]))**3-(float(k[:4]))**3))
    return item
def merge(item):    # 合并列表中key相同的字典
    dic = {}
    for _ in item:
        for k, v in _.items():
            dic.setdefault(k, []).append(v)
    res5 = [{k:v} for k, v in dic.items()]
    return res5
def average(item):  # 对列表的值取平均值
    for k in item:
       item[k] = np.mean(item[k])
    return item
if __name__ == '__main__':
    p = Pool(core)
    res1 = p.map(read_lines,range(cal_init,cal_fina))
    res2 = p.map(center_mass,res1)
    res3 = p.map(cata,res2)
    res4 = p.map(density,res3)
    res5 = merge(res4)
    res6 = p.map(average,res5)
    doc = open('output12.txt', 'w')  # 输出文件
    for h in res6:
      print(h,file = doc)
    doc.close()
    print('你好呀，密度计算已经完成')





