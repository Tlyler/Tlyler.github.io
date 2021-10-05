# 编写人：谭神冬
# 座右铭：安然度日
# 时间： 2021/4/13 8:59
import sys
import numpy as np
cal_init = int(sys.argv[1])     # 初始帧数
cal_fina = int(sys.argv[2])     # 终止帧数
input_file = str(sys.argv[3])   # 输入文件
output_file = str(sys.argv[4])  # 输出文件
angle_all = []
with open (input_file) as f:
  content = f.readlines()
  lines = list(map(lambda x: x.strip(), content))
  for y in range(cal_init, cal_fina):
      xyz_position = []
      c1 = lines[291+y*301]  # 290/299 292/302 295/302  # 行-1 yan: 291/301
      print(c1)
      xyzitem1 = [c1.split()[1], c1.split()[2], c1.split()[3]]
      xyz_position.append(xyzitem1)
      c2 = lines[293+y*301]  # 293/299 294/302 yan: 293/301
      print(c2)
      xyzitem2 = [c2.split()[1], c2.split()[2], c2.split()[3]]
      xyz_position.append(xyzitem2)
      h = float(xyz_position[0][2])-float(xyz_position[1][2])
      vector1 = np.array([float(xyz_position[0][0]),float(xyz_position[0][1]),float(xyz_position[0][2])])
      vector2 = np.array([float(xyz_position[1][0]),float(xyz_position[1][1]),float(xyz_position[1][2])])
      l_d = np.sqrt(np.sum(np.square(vector1-vector2)))
      angle =  np.degrees(np.arcsin(h/l_d))
      angle_all.append(angle)

doc = open(output_file, 'w')
for k in angle_all:
  print(k,file = doc)
doc.close()