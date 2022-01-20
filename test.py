import glob
import os
import sqlite3
from sqlite3 import Error
import pandas as pd
import matplotlib.pyplot as plt
import random
import shutil

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def Update_detects(img_name,id_driver):
    database = "./database.db"
    conn = create_connection(database)
    sql = ''' UPDATE Detect
              SET driver_link = ?
              WHERE Path LIKE ?'''
    cur = conn.cursor()
    conn.execute(sql, (id_driver,'%'+img_name+'%'))
    conn.commit()
def Update_ORC(img_name,id_driver):
    database = "./database.db"
    conn = create_connection(database)
    sql = ''' UPDATE ORC
              SET driver_link = ?
              WHERE Path LIKE ?'''
    cur = conn.cursor()
    conn.execute(sql, (id_driver,'%'+img_name+'%'))
    conn.commit()
if __name__ == '__main__':
    current_csv = pd.read_csv('./static/dataset/driver_2.csv')
    for item in current_csv.values:
        if(len(item[6]) >= 5):
            Update_detects(item[0],item[1])
            print(item[0]," ",item[1])
        else:
            Update_ORC(item[0],item[1])
            print(item[0]," ",item[1])