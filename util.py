import pymysql
from base64 import b64encode
import copy
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
	
def len_ls(l):
	res = []
	if l != None:
		tmp_gl = l.split('_')
		tmp_gl.pop()
		return len(tmp_gl)
	else:
		return 0



def decode_ls(gl, bl):
	res = []
	if gl != None:
		tmp_gl = gl.split('_')
		tmp_gl.pop()
		res += tmp_gl
	if bl != None:
		tmp_bl = bl.split('_')
		tmp_bl.pop()
		res+= tmp_bl
	return res

def overlap_ls(A, B):
	cnt=0
	if A != None:
		tmp_A = A.split('_')
		tmp_A.pop()
	if B != None:
		tmp_B = B.split('_')
		tmp_B.pop()


	for a in tmp_A:
		if a in tmp_B:
			cnt+=1
	return cnt


def decode_rank(data):
	db = pymysql.connect(host='localhost', user='db_user', db='foodwiki', charset='utf8')
	curs = db.cursor()

	div = data.split("@")
	all_rank = div[0]
	cat_num = div[1]
	cat_rank = div[2]
		
	#all rank
	all_res = []
	all_div = all_rank.split('/')
	all_div.pop()
	cnt = 0
	img_ls = []
	for comp in all_div:
		tup = comp.split('_')
		all_res.append((tup[0], tup[1]))
		img_ls.append(tup[2])
		cnt+=1
		if cnt>4:
			break	
	
	tp = copy.deepcopy(img_ls)
	
	id_ls = ""
	id_ls += "img_id={}".format(img_ls[0])
	del img_ls[0]
	for i_id in img_ls:
		id_ls += " OR img_id={}".format(i_id)
	
	
	
	sql_1 = 'SELECT img, img_id FROM Img_tb WHERE ' + id_ls
	curs.execute(sql_1)
	res_1 = curs.fetchall()
	
	all_rank = []
	
	for j in range(len(tp)):
		for i in range(len(all_res)):
			if int(res_1[i][1]) == int(tp[j]):
				all_rank.append((all_res[j][0], all_res[j][1], b64encode(res_1[i][0]).decode()))
	
	#cat
	cat_res = []
	cat_name = cat[int(cat_num)]
	if len(cat_rank) != 0:
		cat_div = cat_rank.split('/')
		cat_div.pop()
		cnt = 0
		img_ls = []
		cat_tmp = []
		for comp in cat_div:
			tup = comp.split('_')
			cat_res.append((tup[0], tup[1]))
			img_ls.append(tup[2])
			cnt+=1
			if cnt>2:
				break
		id_ls = ""
		id_ls += "img_id={}".format(img_ls[0])
		del img_ls[0]
		for i_id in img_ls:
			id_ls += " OR img_id={}".format(i_id)
		
		sql_2 = 'SELECT img FROM Img_tb WHERE ' + id_ls
		curs.execute(sql_2)
		res_2 = curs.fetchall()
		
		cat_rank = []
		
		for j in range(len(cat_res)):
			cat_rank.append((cat_res[j][0], cat_res[j][1], b64encode(res_2[j][0]).decode()))						
	else:
		cat_rank = []		
			
	db.close()			
			
	return all_rank, cat_name, cat_rank
