import cv2
import numpy as np
import sqlite3
import os
from mysql.connector import MySQLConnection, Error
 
# Hàm kết nối
def connect():
    """ Kết nối MySQL bằng module MySQLConnection """
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'demo',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '3306',
            }
}
 
    # Biến lưu trữ kết nối
    conn = None
 
    try:
        conn = MySQLConnection(DATABASES)
 
        if conn.is_connected():
            return conn
 
    except Error as error:
        print(error)
 
    return conn
 
# Test thử
conn = connect()

def insertOrUpdate(id, name):

    conn = sqlite3.connect("D:\SQLite\pythonCamera.db")
    query = "SELECT * FROM people WHERE ID=" + str(id)
    cusror = conn.execute(query)

    isRecordExist = 0

    for row in cusror:
        isRecordExist=1

    if(isRecordExist==0):
        query = "INSERT INTO people(ID,Name) VALUES("+str(id)+",'"+str(name)+"')"
    else:
        query = "UPDATE people SET Name = '"+str(name)+"' WHERE ID="+str(id)

    conn.execute(query)
    conn.commit()
    conn.close()

def insert(ID, name):
    query = "INSERT INTO datacam(ID,name) "\
            "VALUES(%s,%s)"
    args = (ID, name)
 
    try:
 
        conn = connect()
 
        cursor = conn.cursor()
        cursor.execute(query, args)
 
        if cursor.lastrowid:
            print('ID insert là:', cursor.lastrowid)
        else:
            print('Insert thất bại')
 
        conn.commit()
    except Error as error:
        print(error)
 
    finally:
        # Đóng kết nối
        cursor.close()
        conn.close()

face_cascade = cv2.CascadeClassifier("C:\\Users\\ACER\\PycharmProjects\\hello\\venv\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml")

cap = cv2.VideoCapture(0)

id = input("Enter ID:")
name = input("Enter Name:")
#insertOrUpdate(id,name)
insert(id,name)
sampleNum = 0

while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray,1.1,10)

    for(x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

        #tao forder
        if not os.path.exists('dataSet'):
            os.makedirs('dataSet')
        sampleNum = sampleNum+1

        cv2.imwrite('dataSet/User.'+str(id)+'.'+str(sampleNum)+'.jpg',gray[y: y+h,x: x+w])
        cv2.imshow("frame",frame)
        cv2.waitKey(1)

    if sampleNum>100:
        break

cap.release()
cv2.destroyAllWindow()

