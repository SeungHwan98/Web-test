import pymysql

conn = pymysql.connect(host='202.30.19.152', port=3306, user='alarm_user', password='1111', db='lg_dt_db', charset='utf8')
cursor = conn.cursor()

print(dir(cursor))