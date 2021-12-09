import pymysql
import time
import datetime
from util import get_table_rows
from base64 import b64encode
cat = ['한식', '중식', '일식', '양식','분식', '할랄푸드', '패스트푸드', '디저트/카페음료', '기타']




class DAO:
	def __init__(self, db):
		self.db=db
		pass

	def register(self, data):
		user_id = get_table_rows('User_tb')[0]
		db = pymysql.connect(host='localhost', user='db_user', db=self.db, charset='utf8')
		curs = db.cursor()		
		
		sql_0 = 'SELECT COUNT(*) FROM User_tb WHERE id="{}" OR nickname="{}"'.format(data['id'], data['nickname'])
		curs.execute(sql_0)
		res = curs.fetchall()
		if res[0][0] != 0:
			return False
				
		sql = '''INSERT INTO User_tb(user_id, id, passwd, nickname) VALUES (%s, %s, %s, %s)'''
		curs.execute(sql, (user_id, data['id'], data['pw'], data['nickname']))
		db.commit()
		db.close()
		
		return True

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

	def is_reviewed(self, user_id, menu_id):
		db = pymysql.connect(host='localhost', user='db_user', db=self.db, charset='utf8')
		curs = db.cursor()
		sql = "SELECT COUNT(*) FROM Review_tb WHERE user_id='{}' AND menu_id='{}'".format(user_id, menu_id)
		curs.execute(sql)
		res = curs.fetchall()
		if res[0][0]!=0:
			return True
		return False
		
		
		

	def upload_review(self, data, img, user_id):
		db = pymysql.connect(host='localhost', user='db_user', db=self.db, charset='utf8')
		curs = db.cursor()
		img_id = get_table_rows('Img_tb')[0]
		review_id = get_table_rows('Review_tb')[0]
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
			ret= None
			
		elif len(res) ==1:
			ret = res[0]

		else:
			sql_1 = '''SELECT menu_name, menu_id, img FROM Menu_tb NATURAL JOIN Img_tb WHERE menu_name=(%s)'''
			curs.execute(sql_1, (food_n))
			res_1 = curs.fetchall()
			res_ls = []
			for row in res_1:
				res_ls.append([row[0], row[1], b64encode(row[2]).decode()])
			ret = res_ls
			
		db.commit()
		db.close()			
		return ret


			

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
		
		sql_1 = '''SELECT review_id, title, good, bad , img FROM Review_tb NATURAL JOIN Img_tb WHERE menu_id=(%s) AND is_bad=0'''		
		curs.execute(sql_1, (menu_id))
		res_1 = curs.fetchall()
		sql_2= '''SELECT review_id, title, good, bad , img FROM Review_tb NATURAL JOIN Img_tb WHERE menu_id=(%s) AND is_bad=1'''		
		curs.execute(sql_2, (menu_id))
		res_2 = curs.fetchall()		
		
		r1 = list(res_1)
		r1.reverse()
		r2 = list(res_2)
		r2.reverse()
		
		res_t = r1+r2
		res_ls = []
		for row in res_t:
			res_ls.append([row[0], row[1], row[2], row[3], b64encode(row[4]).decode()])	
		
		
		
		db.commit()
		db.close()
		return res_ls

	def get_food_list(self):
		db = pymysql.connect(host='localhost', user='db_user', db=self.db, charset='utf8')
		curs = db.cursor()
		
		sql = '''SELECT menu_name, menu_id, img FROM Menu_tb NATURAL JOIN Img_tb'''
		curs.execute(sql)
		res = curs.fetchall()
		
		res_ls = []
		for row in res:
			res_ls.append([row[0], row[1], b64encode(row[2]).decode()])
		db.commit()
		db.close()
		return res_ls

	
	
		
	def get_review(self, r_id):
		db = pymysql.connect(host='localhost', user='db_user', db=self.db, charset='utf8')
		curs = db.cursor()
		
		sql_1 = '''SELECT * FROM Review_tb WHERE review_id=(%s)'''
		sql_2 = '''SELECT img FROM Img_tb WHERE img_id=(%s)'''
		curs.execute(sql_1, (r_id))
		res = curs.fetchall()
		row_s = list(res[0])
		img_id = row_s[6]
		curs.execute(sql_2, (img_id))
		res_2 = curs.fetchall()
		for row in res_2:
			img = row[0]
		
		db.commit()
		db.close()       
		return img, row_s

	def remove(self, r_id):
		db = pymysql.connect(host='localhost', user='db_user', db=self.db, charset='utf8')
		curs = db.cursor()
		sql = "DELETE FROM Review_tb WHERE review_id='{}'".format(r_id)
		curs.execute(sql)
		db.commit()
		db.close()		
			
	def is_evaluated(self, r_id, u_id):
		db = pymysql.connect(host='localhost', user='db_user', db=self.db, charset='utf8')
		curs = db.cursor()
		sql = '''SELECT like_list FROM User_tb WHERE user_id=(%s)'''
		curs.execute(sql, (u_id))
		res = curs.fetchall()
		tmp = res[0]
		tmp = tmp[0]
		if tmp is not None:
			r_ls = tmp.split('_')
			if str(r_id) in r_ls:
				return True
		
		sql_2 = '''SELECT dislike_list FROM User_tb WHERE user_id=(%s)'''
		curs.execute(sql_2, (u_id))
		res = curs.fetchall()
		tmp = res[0]
		tmp = tmp[0]
		db.commit()
		db.close() 
		if tmp is None:
			return False
		else:
			r_ls = tmp.split('_')
			if str(r_id) in r_ls:
				return True
			return False

			


	def like_up(self, r_id, u_id):
		if self.is_evaluated(r_id, u_id):
			return False
		db = pymysql.connect(host='localhost', user='db_user', db=self.db, charset='utf8')
		curs = db.cursor()
		
		sql_1 = '''SELECT good FROM Review_tb WHERE review_id=(%s)'''
		curs.execute(sql_1, (r_id))
		res = curs.fetchall()
		tmp = res[0]
		like_cnt = tmp[0]
		like_cnt+=1
		
		sql_2 = '''SELECT like_list FROM User_tb WHERE user_id=(%s)'''
		curs.execute(sql_2, (u_id))
		res = curs.fetchall()
		tmp = res[0]
		r_ls = tmp[0]
		if r_ls is None:
			r_ls = ""
		r_ls = r_ls +  r_id + "_" 
		
		sql_3 = 'Update Review_tb SET good={} WHERE review_id={}'.format(like_cnt, r_id)
		curs.execute(sql_3)
		
		sql_4 = 'Update User_tb SET like_list="{}" WHERE user_id={}'.format(r_ls, u_id)
		curs.execute(sql_4)
		db.commit()
		db.close()  
		
		return True

	def dislike_up(self, r_id, u_id):
		if self.is_evaluated(r_id, u_id):
			return False
		
		db = pymysql.connect(host='localhost', user='db_user', db=self.db, charset='utf8')
		curs = db.cursor()
		
		sql_1 = '''SELECT bad FROM Review_tb WHERE review_id=(%s)'''
		curs.execute(sql_1, (r_id))
		res = curs.fetchall()
		tmp = res[0]
		like_cnt = tmp[0]
		like_cnt+=1
		
		sql_2 = '''SELECT dislike_list FROM User_tb WHERE user_id=(%s)'''
		curs.execute(sql_2, (u_id))
		res = curs.fetchall()
		tmp = res[0]
		r_ls = tmp[0]
		if r_ls is None:
			r_ls = ""
		r_ls = r_ls +  r_id + "_" 
		
		
		sql_3 = 'Update Review_tb SET bad={} WHERE review_id={}'.format(like_cnt, r_id)
		curs.execute(sql_3)
		
		sql_4 = 'Update User_tb SET dislike_list="{}" WHERE user_id={}'.format(r_ls_2, u_id)
		curs.execute(sql_4)
		db.commit()
		db.close()  
		
		return True



						
		
     




