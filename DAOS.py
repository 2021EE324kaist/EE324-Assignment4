import pymysql
import time
import datetime

cat = ['한식', '중식', '일식', '양식','분식', '할랄푸드', '패스트푸드', '디저트/카페음료', '기타']

def get_table_rows(tb_name):
		db = pymysql.connect(host='localhost', user='db_user', db='foodwiki', charset='utf8')
		curs = db.cursor()	
		sql = 'SELECT COUNT(*) FROM {}'.format(tb_name)
		curs.execute(sql)
		res = curs.fetchall()	
		db.commit()
		db.close()   
		return res[0]
	


class DAO:
	def __init__(self, db):
		self.db=db
		pass

	def register(self, data):
		user_id = get_table_rows('User_tb')[0]
		db = pymysql.connect(host='localhost', user='db_user', db=self.db, charset='utf8')
		curs = db.cursor()		
		
		sql = '''INSERT INTO User_tb(user_id, id, passwd, nickname) VALUES (%s, %s, %s, %s)'''
		curs.execute(sql, (user_id, data['id'], data['pw'], data['nickname']))
		db.commit()
		db.close()

	def login(self, id_, pw):
		db = pymysql.connect(host='localhost', user='db_user', db=self.db, charset='utf8')
		curs = db.cursor()	
			
		sql = "SELECT user_id, nickname FROM User_tb WHERE id='{}' AND passwd='{}'".format(id_, pw)
		curs.execute(sql)
		db.commit()
		db.close()
		
		return curs.fetchall()
		
			
			
	
	def insert(self, tmp_id):
		db = pymysql.connect(host='localhost', user='db_user', db=self.db, charset='utf8')
		curs = db.cursor()
		
		sql = '''INSERT INTO tmp_table(tmp_id) VALUES (%s)'''
		curs.execute(sql, (tmp_id))
		db.commit()
		db.close()
       
	def upload_img(self, tmp_id, format_img, img):
		db = pymysql.connect(host='localhost', user='db_user', db=self.db, charset='utf8')
		curs = db.cursor()
		sql = '''INSERT INTO IMG_TA(id, format, img) VALUES (%s, %s, %s)''' 
		curs.execute(sql, (tmp_id, format_img, img))
		db.commit()
		db.close()  
 
	def upload_food(self, data, img):
		db = pymysql.connect(host='localhost', user='db_user', db=self.db, charset='utf8')
		curs = db.cursor()
		img_id = user_id = get_table_rows('Img_tb')[0]
		menu_id = user_id = get_table_rows('Menu_tb')[0]
		
		sql_1 = '''INSERT INTO Menu_tb(menu_name, menu_id, img_id, category, description, res_name, price, post_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)''' 
		sql_2 = '''INSERT INTO Img_tb(img_id, img) VALUES (%s, %s)'''
		
		post_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		
		
		curs.execute(sql_1, (data['Menu_name'], menu_id, img_id, data['Category'], data['Description'], data['Res_name'], data['Price'], post_date))
		curs.execute(sql_2, (img_id, img))
		
		db.commit()
		db.close()  

	def upload_review(self, data, img, user_id):
		db = pymysql.connect(host='localhost', user='db_user', db=self.db, charset='utf8')
		curs = db.cursor()
		img_id = get_table_rows('Img_tb')[0]
		review_id = user_id = get_table_rows('Review_tb')[0]

		sql_1 = '''INSERT INTO Review_tb(review_id, user_id, menu_id, title, description,  post_date, img_id, good, bad, rating) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''' 
		
		sql_2 = '''INSERT INTO Img_tb(img_id, img) VALUES (%s, %s)'''
		
		post_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		
		
		curs.execute(sql_1, (review_id, user_id, data['m_id'], data['title'], data['Description'], post_date, img_id, "0", "0", data['rating']))
		curs.execute(sql_2, (img_id, img))
		
		db.commit()
		db.close()  

	def get_f_id_by_name(self, food_n):
		db = pymysql.connect(host='localhost', user='db_user', db=self.db, charset='utf8')
		curs = db.cursor()
		sql = '''SELECT menu_id FROM Menu_tb WHERE menu_name=(%s)'''
		curs.execute(sql, (food_n))
		res = curs.fetchall()
		if len(res) == 0:
			return None
		return res[0]

	def get_food(self, food_id):
		db = pymysql.connect(host='localhost', user='db_user', db=self.db, charset='utf8')
		curs = db.cursor()
		
		sql_1 = '''SELECT * FROM Menu_tb WHERE menu_id=(%s)'''
		sql_2 = '''SELECT img FROM Img_tb WHERE img_id=(%s)'''
		curs.execute(sql_1, (food_id))
		res = curs.fetchall()
		if len(res) == 0:
			return None, None
		row_s = list(res[0])
		img_id = row_s[2]
		print(row_s[3])
		row_s[3] = cat[int(row_s[3])]
		curs.execute(sql_2, (img_id))
		res_2 = curs.fetchall()
		for row in res_2:
			img = row[0]
		
		db.commit()
		db.close()       
		return img, row_s
	
	def get_review_list(self, menu_id):
		db = pymysql.connect(host='localhost', user='db_user', db=self.db, charset='utf8')
		curs = db.cursor()
		
		sql = '''SELECT review_id, title, good, bad FROM Review_tb WHERE menu_id=(%s)'''
		curs.execute(sql, (menu_id))
		res = curs.fetchall()
		db.commit()
		db.close()
		return res

	def get_food_list(self):
		db = pymysql.connect(host='localhost', user='db_user', db=self.db, charset='utf8')
		curs = db.cursor()
		
		sql = '''SELECT menu_name, menu_id FROM Menu_tb'''
		curs.execute(sql)
		res = curs.fetchall()
		db.commit()
		db.close()
		return res

		
	def get_review(self, r_id):
		db = pymysql.connect(host='localhost', user='db_user', db=self.db, charset='utf8')
		curs = db.cursor()
		
		sql_1 = '''SELECT * FROM Review_tb WHERE review_id=(%s)'''
		sql_2 = '''SELECT img FROM Img_tb WHERE img_id=(%s)'''
		curs.execute(sql_1, (r_id))
		res = curs.fetchall()
		row_s = list(res[0])
		img_id = row_s[7]
		curs.execute(sql_2, (img_id))
		res_2 = curs.fetchall()
		for row in res_2:
			img = row[0]
		
		db.commit()
		db.close()       
		return img, row_s


			
		
     




