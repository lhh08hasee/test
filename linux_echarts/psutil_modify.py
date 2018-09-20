import psutil
import time
import MySQLdb as mysql

db = mysql.connect(user="graph", passwd="123456", db="test", host="200.200.200.67")
db.autocommit(True)
cur = db.cursor()
def getinfo():
	mem = psutil.virtual_memory()
	memtotal = mem.total
	memfree = mem.free
	mempercent = mem.percent
	memused = mem.used
	cpu = psutil.cpu_percent(1)
	return memtotal,memfree,memused,mempercent,cpu
	
if __name__== "__main__":
	while True:
		try:
			memtotal,memfree,memused,mempercent,cpu =getinfo()
			t = int(time.time())
			sql = 'insert into stat (mem_free,mem_usage,mem_total,mempercent,cpu,time) value (%s,%s,%s,%s,%s,%s)'%(memfree,memused,memtotal,mempercent,cpu,t)
			cur.execute(sql)
			time.sleep(10)
		except Exception as e:
			print(e)


