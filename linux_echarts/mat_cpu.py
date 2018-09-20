#coding:utf-8

from matplotlib import pyplot as plt
import MySQLdb as mysql
from pyecharts import Line


con = mysql.connect(user="graph", passwd="123456", db="test", host="200.200.200.67")
cur = con.cursor()
sql = 'select cpu from stat'
cur.execute(sql)
cpu_data = cur.fetchall()
all_cpu = []
for cpu in cpu_data:
    cpu_num = eval(cpu[0])
    all_cpu.append(cpu_num)

# 使用pyecharts画图
x = [i for i in range(32)]
line = Line("CPU使用率")
line.add("CPU", x, all_cpu, mark_point=["average"], mark_line=["max", "average"])
line.render()

# 使用matplotlib画图
# plt.plot(all_cpu)
# plt.show()

con.close()

