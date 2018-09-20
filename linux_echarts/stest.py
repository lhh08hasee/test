
import subprocess
import time
import MySQLdb as mysql

db = mysql.connect(user="graph", passwd="123456", db="test", host="200.200.200.67")
db.autocommit(True)
cur = db.cursor()
p = subprocess.Popen("ps aux|grep skin_server.py|grep python|grep -v grep|awk '{print $2 }'", shell=True, stdout=subprocess.PIPE)
pids = p.stdout.readlines()
t = int(time.time())
while True:
        for pid in pids:
                print(pid)
                pid = pid[:-1]
                cpucmd = "top -b -n1|grep " +pid + "|awk '{print $9}'"
                memcmd = "top -b -n1|grep " +pid + "|awk '{print $10}'"
                iotpscmd = "iostat -d  -k 1 1|awk '{print $2}'"
                readcmd = "iostat -d  -k 1 1|awk '{print $3}'"
                writecmd = "iostat -d  -k 1 1|awk '{print $4}'"
                awaitcmd = "iostat -d -x -k |awk '{print $10}'"
                utilscmd = "iostat -d -x -k |awk '{print $14}'"
                usavgcmd = "iostat -c|awk '{print $2}'"
                p = subprocess.Popen(cpucmd, shell=True, stdout=subprocess.PIPE)
                cpu = p.stdout.readlines()[0]
                print(cpu)
                p = subprocess.Popen(memcmd, shell=True, stdout=subprocess.PIPE)
                mem= p.stdout.readlines()[0]
                p = subprocess.Popen(iotpscmd, shell=True, stdout=subprocess.PIPE)
                iotps= p.stdout.readlines()[3]
                p = subprocess.Popen(readcmd, shell=True, stdout=subprocess.PIPE)
                read= p.stdout.readlines()[3]
                p = subprocess.Popen(writecmd, shell=True, stdout=subprocess.PIPE)
                write= p.stdout.readlines()[3]
                p = subprocess.Popen(awaitcmd, shell=True, stdout=subprocess.PIPE)
                await= p.stdout.readlines()[3]	
                p = subprocess.Popen(utilscmd, shell=True, stdout=subprocess.PIPE)
                utils= p.stdout.readlines()[3]
                p = subprocess.Popen(usavgcmd, shell=True, stdout=subprocess.PIPE)
                usavg= p.stdout.readlines()[3]	
        print(iotps,read,write,await,utils,usavg)
        sql = 'insert into serverinfo (pid,cpu,mem,time) value (%s,%s,%s,%s)'%(pid,cpu,mem,t)
        cur.execute(sql)
        time.sleep(10)
		
	
        sql = 'insert into iostat (readd,writes,awaits,utils,tps,time,usavg) value (%s,%s,%s,%s,%s,%s,%s)'%(read,write,await,utils,iotps,t,usavg)
        cur.execute(sql)
        time.sleep(10)

