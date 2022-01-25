from itertools import count
from flask import Flask
from flask import request, url_for
from flask import render_template
from flask import redirect, Response
from flask import render_template, redirect, session
from flask_session import Session
import glob
import sqlite3
from sqlite3 import Error
import json
import  os

imgs_per_page = 5
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
PERMANENT_SESSION_LIFETIME = 1800

app.config.update(SECRET_KEY=os.urandom(24))

app.config.from_object(__name__)
Session(app)


@app.route("/detect/")
@app.route('/detect/<page>', methods=['POST', 'GET'])
def detect(page=None):
    if 'username' in session:
        detects = select_detects()
        if request.method == 'GET':
            if page:
                if str(page).isdigit():
                    page = int(page)
                    if page*imgs_per_page < len(detects):
                        return render_template('detect.html', imgs=detects[(page-1)*imgs_per_page:page*imgs_per_page], max_lenght=len(detects), cur_page=page)
                    else:
                        if page*imgs_per_page > len(detects)+imgs_per_page:
                            return render_template('detect.html', imgs=detects[0:imgs_per_page], max_lenght=len(detects), cur_page=page)
                        return render_template('detect.html', imgs=detects[(page-1)*imgs_per_page:], max_lenght=len(detects), cur_page=page)
                else:
                    return render_template('detect.html', imgs=detects[0:imgs_per_page], max_lenght=len(detects), cur_page=page)
            else:
                return render_template('detect.html', imgs=detects[0:imgs_per_page], max_lenght=len(detects), cur_page=page)
        if request.method == 'POST':
            jObject = json.loads(request.form['data'])
            detects_pos = jObject['detects']
            update_detects(detects_pos)
            resp = Response("saved")
            return resp
    else:
        session['mess'] = ""
        return render_template('login.html')
    


@app.route("/")
def home():
    
    if 'username' in session:
        session["count_detect"] = count_detect(str(session["user_id"]))
        session["count_orc"] = count_orc(str(session["user_id"]))
        return render_template('home.html')
        
    else:
        session['mess'] = ""
        return render_template('login.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("vào post")
        user_name = request.form.get('username')
        pass_word = request.form.get('password')
        print("ok")
        database = "./database.db"
        conn = create_connection(database)
        cur = conn.cursor()
        cur.execute("select * from acc WHERE acc.Username = '"+user_name+"'")
        accs = cur.fetchall()
        print("ok2")
        if(len(accs) == 0):
            session['mess'] = "Tên đăng nhập không tồn tại"
            return render_template('login.html')
        else:
            if(accs[0][2] == pass_word):
                session['username'] = user_name
                session['password'] = pass_word
                session['name'] = accs[0][3]
                session['user_id'] = accs[0][0]
                session["count_detect"] = count_detect(accs[0][0])
                session["count_orc"] = count_orc(accs[0][0])
                return render_template('home.html')
            else:
                session['mess'] = "Mật khẩu không chính xác vui lòng kiểm tra lại"
                return render_template('login.html')
    else:
        session['mess'] = ""
        return render_template('login.html')
@app.route('/logout')
def logout():
   session.pop('username', None)
   session.pop('password', None)
   session.pop('name', None)
   return redirect(url_for('home'))
@app.route("/orc/")
@app.route('/orc/<page>', methods=['POST', 'GET'])
def orc(page=None):
    if 'username' in session:
        ORC = select_ORC()
        if request.method == 'GET':
            if page:
                if str(page).isdigit():
                    page = int(page)
                    if page * 10 < len(ORC):
                        return render_template('orc.html', imgs=ORC[(page - 1) * 10:page * 10],
                                            max_lenght=len(ORC), cur_page=page)
                    else:
                        if page * 10 > len(ORC) + 10:
                            return render_template('orc.html', imgs=ORC[0:10], max_lenght=len(ORC), cur_page=page)
                        return render_template('orc.html', imgs=ORC[(page - 1) * 10:], max_lenght=len(ORC),
                                            cur_page=page)
                else:
                    return render_template('orc.html', imgs=ORC[0:10], max_lenght=len(ORC), cur_page=page)
            else:
                return render_template('orc.html', imgs=ORC[0:10], max_lenght=len(ORC), cur_page=page)
        if request.method == 'POST':
            jObject = json.loads(request.form['data'])
            ORC_pos = jObject['ORC']
            update_ORC(ORC_pos)
            resp = Response("saved")
            return resp
    else:
        session['mess'] = ""
        return render_template('login.html')
    


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def select_detects():
    database = "./database.db"
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Detect")
    Detects = cur.fetchall()
    conn.commit
    return Detects


def update_detects(up_detects):
    database = "./database.db"
    conn = create_connection(database)
    sql = ''' UPDATE Detect
              SET Loaixe = ? ,
                  Path = ? ,
                  x1 = ?,
                  y1 = ?,
                  x2 = ?,
                  y2 = ?,
                  x3 = ?,
                  y3 = ?,
                  x4 = ?,
                  y4 = ?,
                  TrangThai = ? ,
                  acc_id = ?
              WHERE ID = ?'''
    cur = conn.cursor()
    for detect in up_detects:
        conn.execute(sql, (detect[1], detect[2], detect[3], detect[4], detect[5],
                     detect[6], detect[7], detect[8], detect[9], detect[10], detect[11],session['user_id'], detect[0]))
        conn.commit()


def select_ORC():
    database = "./database.db"
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("SELECT * FROM ORC")
    ORC = cur.fetchall()
    conn.commit
    return ORC


def update_ORC(up_ORC):
    database = "./database.db"
    conn = create_connection(database)
    sql = ''' UPDATE ORC
              SET LoaiXe = ? ,
                    Path = ? ,
                  LoaiBienSo = ? ,
                  PlateLine1 = ?,
                  PlateLine2 = ?,
                  Status = ?,
                  acc_id
              WHERE ID = ?'''
    cur = conn.cursor()
    for para in up_ORC:
        conn.execute(sql, (para[1], para[2], para[3], para[4], para[5],
                     para[6],session['user_id'], para[0]))
        conn.commit()

def  count_detect(id):
    database = "./database.db"
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("select count(ID) FROM Detect WHERE Detect.acc_id = '"+str(id)+"'")
    count = cur.fetchone()
    conn.commit
    return count[0]
def  count_orc(id):
    database = "./database.db"
    conn = create_connection(database)
    cur = conn.cursor()
    cur.execute("select count(ID) FROM ORC WHERE ORC.acc_id = '"+str(id)+"'")
    count = cur.fetchone()
    conn.commit
    return count[0]
    
if __name__ == '__main__':
    app.debug = True
    app.run()
