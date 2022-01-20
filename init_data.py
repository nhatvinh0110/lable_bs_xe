import glob
import os
import sqlite3
from sqlite3 import Error
import pandas as pd
import matplotlib.pyplot as plt
import random
import shutil


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
            
            new_Detect = (item[1],item[0][3:],item[4],item[5],item[6],item[7],item[8],item[9],item[10],item[11],'raw')
            if((item[4]+item[5]+item[6]+item[7]+item[8]+item[9]+item[10]+item[11])==0):
                new_Detect = (item[1],item[0][3:],'','','','','','','','','raw')
            new_Detect_id = create_detect(con,new_Detect)
            #shutil.copyfile('static/' + item[0][3:].strip(),'./orc/'+ str(new_Detect_id)+'.jpg')
            if(item[2] == 'no'):
                continue
            new_ORC = (item[1],item[3][3:],'2',item[12],item[13],'raw',new_Detect_id)
            if(pd.isnull(item[13])):
                if(pd.isnull(item[12])):
                    new_ORC = (item[1],item[3][3:],'0',item[12],item[13],'raw',new_Detect_id)
                else:
                    new_ORC = (item[1],item[3][3:],'1',item[12],item[13],'raw',new_Detect_id)
            create_orc(con,new_ORC)
            print(new_Detect + new_ORC)
if __name__ == '__main__':
    init_data_from_csv("./static/dataset/combined_csv.csv")
    # for x in os.listdir("./static/dataset/"):
    #     for csv in os.listdir("./static/dataset/"+x+"/"):
    #         if csv.endswith(".csv"):
    #             init_data_from_csv("./static/dataset/"+x+"/"+csv)
            