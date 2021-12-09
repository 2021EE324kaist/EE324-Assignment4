import pymysql


num=21

f = open("{}.jpg".format(num), "rb").read()
img = bytearray(f)

db = pymysql.connect(host='localhost', user='db_user', db='foodwiki', charset='utf8')
curs = db.cursor()



sql = '''UPDATE Img_tb SET img = (%s) WHERE img_id=(%s)'''
curs.execute(sql, (img, str(num)))

db.commit()
db.close()  
