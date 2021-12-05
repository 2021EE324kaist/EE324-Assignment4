import pymysql
import util
import time
def bad_user(u_id):

	db = pymysql.connect(host='localhost', user='man2', db='foodwiki', charset='utf8')
	with db.cursor() as curs:
		sql_1 = 'SELECT AVG(rating) FROM Review_tb WHERE user_id={}'.format(u_id)
		sql_2 = 'SELECT COUNT(*) FROM Review_tb WHERE user_id={} AND rating > 3'.format(u_id)
		curs.execute(sql_1)
		res_1 = curs.fetchall()	
		curs.execute(sql_2)
		res_2 = curs.fetchall()	
		
		if res_1[0][0] is not None and res_1[0][0] < 1.7 and res_2[0][0] <3:
			return True

	with db.cursor() as curs:
		sql_3 = 'SELECT like_list, dislike_list FROM User_tb WHERE user_id={}'.format(u_id)
		curs.execute(sql_3)
		res_3 = curs.fetchall()
		gl, bl = res_3[0]
		gl_len = util.len_ls(gl)
		bl_len = util.len_ls(bl)
		
		if gl_len + bl_len > 0 and gl_len/(gl_len+bl_len) < 0.2:
			return True

	with db.cursor() as curs:	
		sql_4 = 'SELECT COUNT(*) FROM Review_tb WHERE user_id={}'.format(u_id)
		curs.execute(sql_4)
		res_4 = curs.fetchall()
		if res_4[0][0] < 3:
			return True
	
	db.close()
	
	return False
			
def bad_review(bu):
	br = []
	db = pymysql.connect(host='localhost', user='man2', db='foodwiki', charset='utf8')
	if len(bu) >0:
		with db.cursor() as curs:
			bu_str = ""
			bu_str += "user_id = {}".format(bu[0])
			del bu[0]
			for u_id in bu:
				bu_str += " OR user_id={}".format(u_id)
			
			sql_1 = 'SELECT review_id FROM Review_tb WHERE ' + bu_str
			curs.execute(sql_1)
			res_1 = curs.fetchall()
		for r_id in res_1:
			br.append(r_id[0])
	
	with db.cursor() as curs:
		sql_2 = 'SELECT good, bad, review_id FROM Review_tb WHERE good + bad > 20'
		curs.execute(sql_2)
		res_2 = curs.fetchall()
		
		for good, bad, r_id in res_2:
			if good + bad > 20 and bad/(good+bad) > 0.9:
				br.append(r_id)
	if len(br) >0:
		with db.cursor() as curs:
			br_str = ""
			br_str += "review_id = {}".format(br[0])		
			del br[0]
			for r_id in br:
				br_str += " OR review_id={}".format(r_id)
			sql_3 = 'UPDATE Review_tb SET is_bad=1 WHERE ' + br_str
			curs.execute(sql_3)
	db.commit()
	db.close()


def loop():
	while(1):
		bu = []
		user_len = util.get_table_rows('User_tb')[0]
		for i in range(user_len):
			if bad_user(i):
				bu.append(i)
		
		bad_review(bu)
		time.sleep(3600)

if __name__ == "__main__":
	loop()


