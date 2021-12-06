from flask import Flask, render_template, json, request, redirect, url_for, session, escape
from sqlalchemy import create_engine, text
from DAOS import DAO
import random
from base64 import b64encode
from PIL import Image
import random
import pymysql
import util
app = Flask(__name__, static_url_path='/static')
app.secret_key=b'1234abcdefghqwer'


@app.route("/")
def index():
	return "RECOM SERVER!"

@app.route("/recom/<user_id>")
def recom(user_id):
	db = pymysql.connect(host='localhost', user='man1', db='foodwiki', charset='utf8')
	with db.cursor() as curs:
		sql = 'SELECT like_list, dislike_list FROM User_tb WHERE user_id={}'.format(user_id)
		curs.execute(sql)
		res = curs.fetchall()	
		tp = res[0]
		me_gl = tp[0]
		me_bl = tp[1]
		me_rt = util.decode_ls(me_gl, me_bl)

		sql_t = 'SELECT C.user_id, (SELECT COUNT(*) FROM (SELECT menu_id FROM Review_tb WHERE user_id={}) AS A NATURAL JOIN (SELECT menu_id FROM Review_tb WHERE user_id=C.user_id) AS B) FROM User_tb as C'.format(user_id)
		curs.execute(sql_t)
		res_t = curs.fetchall()
		
		sql_1 = 'SELECT user_id, like_list, dislike_list FROM User_tb WHERE NOT user_id={}'.format(user_id)	
		curs.execute(sql_1)
		res_1 = curs.fetchall()
	
	u_id_ls= []
	
	for row in res_1:
		u_id, u_gl, u_bl = row
		rt = util.decode_ls(u_gl, u_bl)
		rt += me_rt
		rt_set = set(rt)	

		overlap_num = len(rt) - len(rt_set) 
		if overlap_num + res_t[int(u_id)][1] > 5:
			sum_ls = util.overlap_ls(me_gl, u_gl) + util.overlap_ls(me_bl, u_bl) - util.overlap_ls(me_gl, u_bl) - util.overlap_ls(me_bl, u_gl)
			db.ping()
			if sum_ls/overlap_num > 0.3:
				with db.cursor() as curs:
					sql_l = 'SELECT AVG(CT) FROM (SELECT MAX(rating) - MIN(rating) AS CT FROM (SELECT menu_id, rating FROM Review_tb WHERE (user_id={} OR user_id={})AND menu_id IN(SELECT * FROM (SELECT menu_id FROM Review_tb WHERE user_id={}) AS A NATURAL JOIN (SELECT menu_id FROM Review_tb WHERE user_id={}) AS B)) AS C GROUP BY menu_id) AS E'.format(user_id, u_id, user_id, u_id)
					curs.execute(sql_l)
					res_l = curs.fetchall()
				tp_l = res_l[0]
				if tp_l[0] == None:
					continue
				if tp_l[0] <2.5:
					u_id_ls.append(u_id)	
		db.ping()
	
	tem_food = []
	
	for u_id in u_id_ls:
		with db.cursor() as curs:
			sql_tm = 'SELECT * FROM (SELECT menu_id FROM Review_tb WHERE user_id={} AND RATING=5) AS A NATURAL JOIN (SELECT DISTINCT(menu_id) FROM Review_tb WHERE menu_id NOT IN (SELECT menu_id FROM Review_tb WHERE user_id={})) AS B' .format(u_id, user_id)
			curs.execute(sql_tm)
			res_tm = curs.fetchall()
			for f in res_tm:
				tem_food.append(f[0])
		
	rs = []
	for s in set(tem_food):
		if tem_food.count(s) >1:
			rs.append(s)

	with db.cursor() as curs:
			sql_mb = 'SELECT menu_id FROM Review_tb WHERE user_id={} AND RATING=5' .format(user_id)
			curs.execute(sql_mb)
			res_mb = curs.fetchall()
			for f in res_mb:
				rs.append(f[0])
	db.close()  
	
	if len(rs) != 0:
		return str(random.choice(rs))
	else:
		lens = util.get_table_rows('Menu_tb')
		return str(random.randint(0, lens[0]-1))

	



	

@app.route("/food_ranking")
def food_ranking():
	db = pymysql.connect(host='localhost', user='man1', db='foodwiki', charset='utf8')
	curs = db.cursor()	
	#all date
	sql = 'SELECT menu_id, menu_name, img_id FROM Menu_tb NATURAL JOIN  (SELECT menu_id FROM Review_tb Group by menu_id HAVING COUNT(*)>3 ORDER BY AVG(rating) DESC) as A '

	curs.execute(sql)
	res = curs.fetchall()
	
	cat = random.randint(0, 8)
	
	#category
	sql_1 = 'SELECT menu_id, menu_name, img_id FROM Menu_tb NATURAL JOIN  (SELECT menu_id FROM Review_tb Group by menu_id HAVING COUNT(*)>3 ORDER BY AVG(rating) DESC) as A WHERE category={}'.format(cat)


	curs.execute(sql_1)
	res_1 = curs.fetchall()
	
	resp = ""	
	for comp in res:
		tmp = str(comp[0]) + "_" + str(comp[1]) + "_" + str(comp[2]) + "/"
		resp+=tmp
	resp += "@" + str(cat) + "@"
	for comp in res_1:
		tmp = str(comp[0]) + "_" + str(comp[1]) + "_" + str(comp[2]) + "/"
		resp+=tmp


	db.commit()
	db.close()  


	
	return resp

 

	
'''	#Today days
	sql_t = 'SELECT menu_id, AVG(rating) FROM (SELECT menu_id, rating from Review_tb WHERE post_date > DATE_ADD(NOW(), INTERVAL -1 DAY)) as A Group by menu_id HAVING COUNT(*) > 4 ORDER BY AVG(rating) DESC;'
	curs.execute(sql_t)
	res_t = curs.fetchall()
	'''
	    	
if __name__ == "__main__":
	app.run(threaded=True, port=3099, host='127.0.0.1')

