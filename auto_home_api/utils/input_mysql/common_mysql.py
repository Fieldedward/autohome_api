import pymysql

# 链接数据库
conn = pymysql.connect(
	# 主机地址
	host='127.0.0.1',
	# 端口号
	port=3306,
	user='root',
	password='12345678',
	# 链接的库的名称
	database='test_car',
	# 字符串类型
	charset='utf8',
	# 自动二次确认
	autocommit=True
)

cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

sql = "INSERT INTO test_car.car(NAME) VALUES ('布加迪');"

affect_rows = cursor.execute(sql)

cursor.fetchall()
