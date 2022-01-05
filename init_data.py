import glob
import os
import sqlite3
from sqlite3 import Error
import pandas as pd
import matplotlib.pyplot as plt
import random

from app import detect

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def create_detect(conn, Detect):
    sql = ''' INSERT INTO Detect(LoaiXe,Path,x1,y1,x2,y2,x3,y3,x4,y4,TrangThai)
              VALUES(?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, Detect)
    conn.commit()
    return cur.lastrowid

def create_orc(conn, ORC):
    sql = ''' INSERT INTO ORC(LoaiXe,Path,LoaiBienSo,PlateLine1,PlateLine2,Status,VehiclePath)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, ORC)
    conn.commit()
    return cur.lastrowid

def select_detects(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM Detect")
    Detects = cur.fetchall()
    return Detects
def init_data_from_csv(csv_path) :
    database = "./database.db"
    current_csv = pd.read_csv(csv_path)
    con = create_connection(database)
    with con:
        for item in current_csv.values:
            new_Detect = (item[2],item[1][3:],item[5],item[6],item[7],item[8],item[9],item[10],item[11],item[12],'raw')
            if((item[5]+item[6]+item[7]+item[8]+item[9]+item[10]+item[11]+item[12])==0):
                new_Detect = (item[2],item[1][3:],'','','','','','','','','raw')
            new_Detect_id = create_detect(con,new_Detect)
            if(item[3] == 'no'):
                break
            new_ORC = (item[2],item[4][3:],'2',item[13],item[14],'raw',new_Detect_id)
            if(pd.isnull(item[14])):
                if(pd.isnull(item[13])):
                    new_ORC = (item[2],item[4][3:],'0',item[13],item[14],'raw',new_Detect_id)
                else:
                    new_ORC = (item[2],item[4][3:],'1',item[13],item[14],'raw',new_Detect_id)
            create_orc(con,new_ORC)
            print(new_Detect)
if __name__ == '__main__':
    
    for x in os.listdir("./static/dataset/"):
        init_data_from_csv("./static/dataset/"+x+"/car.csv")
            