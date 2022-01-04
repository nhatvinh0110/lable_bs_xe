from flask import Flask
from flask import request, url_for
from flask import render_template
from flask import redirect, Response
import glob
import sqlite3
from sqlite3 import Error
import json

imgs_per_page = 5
app = Flask(__name__)


@app.route("/detect/")
@app.route('/detect/<page>', methods=['POST', 'GET'])
def detect(page=None):
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


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/orc/")
@app.route('/orc/<page>', methods=['POST', 'GET'])
def orc(page=None):
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
                  TrangThai = ?
              WHERE ID = ?'''
    cur = conn.cursor()
    for detect in up_detects:
        conn.execute(sql, (detect[1], detect[2], detect[3], detect[4], detect[5],
                     detect[6], detect[7], detect[8], detect[9], detect[10], detect[11], detect[0]))
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
                  Status = ? 
              WHERE ID = ?'''
    cur = conn.cursor()
    for para in up_ORC:
        conn.execute(sql, (para[1], para[2], para[3], para[4], para[5],
                     para[6], para[0]))
        conn.commit()


if __name__ == '__main__':
    app.debug = True
    app.run()
