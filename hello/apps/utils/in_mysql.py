#_*_ encoding:utf8 _*_

import pymysql
import time
password = "123456"

db = pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     passwd="12345678",
                     db="hello",
                     charset="utf8")
cursor = db.cursor()
sql = "insert into users_userprofile(username,password,birday,first_name,last_name,is_superuser,address,mobile,gender,image,email,is_staff,is_active,date_joined,nick_name,token) value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

d=[]
for i in range(20):
    ctime = int(time.time())
    localTime = time.localtime(ctime)
    ctime = time.strftime("%Y-%m-%d %H:%M", localTime)
    bir = ctime
    user = "雏田%s" %(i+3)
    email = "%s@muye.com" %(i+3)
    join = ctime
    token = "abcd%s" %i
    s=(user,password,bir,"日向","雏田",0,"木叶",19999999999,"female","image/default.png",email,1,0,join,"",token)
    d.append(s)

t=tuple(d)
cursor.executemany(sql,t)
db.commit()


cursor.close()
db.close()
