import pymysql

db = pymysql.connect("localhost","root","1234","mall")
cursor = db.cursor()
sql = "select * from pms_product"
cursor.execute(sql)
datalist = []
data = cursor.fetchall()
for tmpData in data:
    print(tmpData)

