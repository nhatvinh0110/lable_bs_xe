from flask import Flask
from flask import request,url_for
from flask import render_template
from flask import redirect,Response
import sqlite3
import json

app = Flask(__name__)

@app.route("/")
@app.route('/<img_path>', methods=['POST', 'GET'])
def mainpage(img_path=None):
    if request.method == 'GET':
        if img_path:
            return render_template('draw.html')
        else:
            return render_template('draw.html')
	
	
    if request.method == 'POST':
        print("p1: " + request.form['p1']);
        resp = Response("saved")
        return resp

if __name__ == '__main__':
    app.debug = True
    app.run()
