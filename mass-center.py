# 编写人：谭神冬
# 座右铭：question keep answer
# 时间： 2021/5/23 19:55
import numpy as np
filename = 'C:/Users/Lenovo/Desktop/test.xyz'
def read_lines(filename):
  with open (filename) as f:
    content = f.readlines()
    lines = list(map(lambda x: x.strip(), content))
    return lines
def center_mass(num): # 相应帧的水质心的计算
  all = []
  lines = read_lines(filename)
  for i in lines[(num-1)*(int(lines[0])+2):num*(int(lines[0])+2)]:
    if i[0]=='i' or i.isdigit():
      continue
    elif i[0]=='H':
      atom = i.split()
      H_xyz = [float(atom[1]),float(atom[2]),float(atom[3]),1.007947]
      all.append(H_xyz)
    elif i[0]=='O':
      atom = i.split()
      O_xyz = [float(atom[1]),float(atom[2]),float(atom[3]),14.00672]
      all.append(O_xyz)
    else:
      break
  masses = np.array(all)
  nonZeroMasses = masses[np.nonzero(masses[:,3])]
  CM = np.average(nonZeroMasses[:,:3], axis=0, weights=nonZeroMasses[:,3])
  return CM
#print(center_mass(20))

def distance(num): # 所有水与质心的距离计算
  lines = read_lines(filename)
  l = []
  for j in lines[(num-1)*(int(lines[0])+2):num*(int(lines[0])+2)]:
    if j[0]=='O':
      atom = j.split()
      vector1 = np.array([float(atom[1]),float(atom[2]),float(atom[3])])
      vector2 = np.array(center_mass(1))
      l_d = np.sqrt(np.sum(np.square(vector1 - vector2)))
      l.append(l_d)
    elif j[0]=='C':
      break
  return l

def cata(data): # 数据分类
  intervals = {'{}-{}'.format(0.4*x,0.4*(x+1)):0 for x in range(20)}
  for list in data:
      for interval in intervals:
          start,end = tuple(interval.split('-'))
          if float(start)<=list<=float(end):
              intervals[interval] +=1
  return intervals

# for num in range(100):
l = distance(2)
print(cata(l))