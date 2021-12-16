from flask import Flask
from flask import request, url_for
from flask import render_template
from flask import redirect, Response
import glob
import sqlite3
from sqlite3 import Error
import json


app = Flask(__name__)


@app.route("/")
@app.route('/<page>', methods=['POST', 'GET'])
def mainpage(page=None):
    detects = select_detects()
    if request.method == 'GET':
        if page:
            if str(page).isdigit():
                page = int(page)
                if page*10 < len(detects):
                    return render_template('index.html', imgs=detects[(page-1)*10:page*10],max_lenght = len(detects),cur_page= page)
                else:
                    if page*10 > len(detects)+10 :
                        return render_template('index.html', imgs=detects[0:10],max_lenght = len(detects),cur_page= page)
                    return render_template('index.html', imgs=detects[(page-1)*10:],max_lenght = len(detects),cur_page= page)
            else:
                return render_template('index.html', imgs=detects[0:10],max_lenght = len(detects),cur_page= page)
        else:
            return render_template('index.html', imgs=detects[0:10],max_lenght = len(detects),cur_page= page)        
    if request.method == 'POST':
        jObject = json.loads(request.form['data'])
        detects_pos = jObject['detects']
        update_detects(detects_pos)
        resp = Response("saved")
        return resp
@app.route("/home/")
def home():
    return render_template('home.html')

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


if __name__ == '__main__':
    app.debug = True
    app.run()
