#coding:utf-8

from flask import Flask, render_template
import MySQLdb as mysql
from pyecharts import Line
from datetime import datetime
import time

app = Flask(__name__)

DATAFORMAT = "%Y-%m-%d %H:%M:%S"
REMOTE_HOST = "https://pyecharts.github.io/assets/js"
CON = mysql.connect(user="graph", passwd="123456", db="test", host="200.200.200.67")
CUR = CON.cursor()

@app.route("/")
def hello():
    s3d = cpu_line()
    return render_template(
        "pyecharts.html",
        myechart=s3d.render_embed(),
        host=REMOTE_HOST,
        script_list=s3d.get_js_dependencies(),
    )


@app.route("/mem")
def mem():
    s2d = mem_line()
    return render_template(
        "pyecharts.html",
        myechart=s2d.render_embed(),
        host=REMOTE_HOST,
        script_list=s2d.get_js_dependencies(),
    )


def mem_line():
    sql = 'SELECT mem,time FROM serverinfo'
    CUR.execute(sql)
    mem_data = CUR.fetchall()
    all_mem = []
    mem_time = []
    for mem in mem_data:
        mem_num = eval(mem[0])
        mem_date = eval(mem[1])
        all_mem.append(mem_num)
        time_local = time.localtime(mem_date)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        mem_time.append(dt)
    line = Line("MEM使用率")
    line.add("MEM", mem_time, all_mem)
    return line


def cpu_line():
    sql = 'select cpu from stat'
    CUR.execute(sql)
    cpu_data = CUR.fetchall()
    all_cpu = []
    for cpu in cpu_data:
        cpu_num = eval(cpu[0])
        all_cpu.append(cpu_num)
    x = [i for i in range(32)]
    line = Line("CPU使用率")
    line.add("CPU", x, all_cpu, mark_point=["average"], mark_line=["max", "average"])
    return line


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
