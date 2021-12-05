import pymysql

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
	div = data.split("@")
	all_rank = div[0]
	cat_num = div[1]
	cat_rank = div[2]
		
	#all rank
	all_res = []
	all_div = all_rank.split('/')
	all_div.pop()
	cnt = 0
	for comp in all_div:
		tup = comp.split('_')
		all_res.append((tup[0], tup[1]))
		cnt+=1
		if cnt>4:
			break		
	#cat
	cat_res = []
	cat_res.append(cat[int(cat_num)])
	cat_div = cat_rank.split('/')
	cat_div.pop()
	cnt = 0
	for comp in cat_div:
		tup = comp.split('_')
		cat_res.append((tup[0], tup[1]))
		cnt+=1
		if cnt>2:
			break
	return all_res, cat_res
