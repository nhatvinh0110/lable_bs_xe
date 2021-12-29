import glob
import os
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn
def create_detect(conn, Detect):
    sql = ''' INSERT INTO Detect(LoaiXe,Path,TrangThai)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, Detect)
    conn.commit()
    return cur.lastrowid
def select_detects(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM Detect")
    Detects = cur.fetchall()
    return Detects
if __name__ == '__main__':
    database = "./database.db"
    con = create_connection(database)
    with con:
        for img in glob.glob("./static/vehicle/car/*.jpg"):
            print(os.path.basename(img))
            Detect = ('oto','./vehicle/car/'+os.path.basename(img),'raw')
            Detect_id = create_detect(con,Detect)
        detects = select_detects(con)
        for detect in detects:
            print(detect[0])
            