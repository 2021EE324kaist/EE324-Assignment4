from flask import Flask, render_template, json, request, redirect, url_for, session, escape
from sqlalchemy import create_engine, text
from DAOS import DAO
import random
from base64 import b64encode
from PIL import Image
app = Flask(__name__, static_url_path='/static')
app.secret_key=b'1234abcdefghqwer'


@app.route("/")
def index():
	return render_template('index.html')

@app.route("/upload_food", methods=['GET', 'POST'])
def upload_food():
    if 'user_id' not in session:
        return render_template("Login_first.html")     
    elif session['user_id']== '':
        return render_template("Login_first.html")    	
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        f = request.files['img'].read()
        if len(f) == 0:
        	f = open("no_image.png", "rb").read()
        	f = bytearray(f)
        DAO('foodwiki').upload_food(data, f)	
        return render_template("upload_done.html")
    return render_template('upload_food.html', input = {})
    
@app.route("/upload_review/<m_id>",methods=['GET', 'POST'])
def upload_review(m_id):
    if 'user_id' not in session:
        return render_template("Login_first.html")  
    if session['user_id']== '':
        return render_template("Login_first.html")  
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        f = request.files['img'].read()
        if len(f) == 0:
        	f = open("no_image.png", "rb").read()
        	f = bytearray(f)
        DAO('foodwiki').upload_review(data, f, str(session['user_id']))	
        return render_template("upload_done.html")
    return render_template('upload_review.html', m_id = m_id)

@app.route("/food_list")
def get_food_list():
	ls = DAO('foodwiki').get_food_list()
	return render_template('food_list.html', foods=ls)

@app.route("/get_reviews/<m_id>")
def get_reviews(m_id):
	ls = DAO('foodwiki').get_review_list(m_id)
	return render_template('review_list.html', reviews=ls)

@app.route("/review/<r_id>")
def view_reviews(r_id):
	img, dic = DAO('foodwiki').get_review(r_id)	
	return render_template("view_review.html", img=b64encode(img).decode(), dic=dic)

@app.route("/food/<f_id>")
def get_food(f_id):
	ret, dic = DAO('foodwiki').get_food(f_id) 
	if ret is not None:
		return render_template("view_food.html", output='1557', img = b64encode(ret).decode(), dic = dic)
	else:
		return render_template("No Search.html") 

@app.route("/login", methods=['POST'])
def login():
	id_ = request.form['id']
	pw_ = request.form['pw']
	data =  DAO('foodwiki').login(id_, pw_)
	if(len(data)) == 0:
		return render_template('login_failed.html')	
		
	else:
		d = data[0]
		session['user_id'] = d[0]
		session['nickname'] = d[1]
		return render_template('index.html')	

@app.route("/login_form")
def login_1():
	return render_template('login.html')	
	
@app.route("/logout")
def logout():
	session.clear()
	return redirect(url_for('index'))

@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
    	data = request.form.to_dict(flat=True)

    	DAO('foodwiki').register(data)

    	return render_template('index.html')
    return render_template('register.html')


@app.route("/search", methods=['GET','POST'])
def search(m_id = None):  
    data = request.args.get('Search_n')
    f_id =  DAO('foodwiki').get_f_id_by_name(data)
    return redirect(url_for("get_food", f_id=str(f_id[0])))


@app.route("/like_click")
def like():
    return render_template('Like.html')

@app.route("/dislike_click")
def dislike():
    return render_template('Like.html')


	    	
if __name__ == "__main__":
	app.run(threaded=True, port=3078, host='0.0.0.0')
