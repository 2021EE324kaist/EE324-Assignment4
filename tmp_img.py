import pymysql

f = open("no_image.png", "rb").read()
img = bytearray(f)

db = pymysql.connect(host='localhost', user='db_user', db='foodwiki', charset='utf8')
curs = db.cursor()


for img_id in range(222):
	sql = '''INSERT INTO Img_tb(img_id, img) VALUES (%s, %s)'''
	curs.execute(sql, (img_id, img))

db.commit()
db.close()  
