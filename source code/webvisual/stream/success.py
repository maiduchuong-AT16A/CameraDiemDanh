import numpy as np
import cv2
import sqlite3
from PIL import Image

recognizer = cv2.face.LBPHFaceRecognizer_create() #cái này dùng để train dữ liệu
face_cascades = cv2.CascadeClassifier("C:\\Users\\ACER\\PycharmProjects\\hello\\venv\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml")

recognizer.read("recognizer\\trainingData.yml")

#lay thong tin bang id
def getProfile(Id):
    conn = sqlite3.connect("D:\SQLite\pythonCamera.db")
    query = "SELECT * FROM people WHERE ID=" + str(id)
    cusror = conn.execute(query)

    profile = None

    for row in cusror:
        profile=row

    conn.close()
    return profile

#bat cam
cap = cv2.VideoCapture(0)

while True:
    ret,frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascades.detectMultiScale(gray,1.1,10)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(w+x,y+h),(0,255,0),2)

        roi_gray = gray[y:y+h,x:x+w]

        id,confidence = recognizer.predict(roi_gray)
        print(id)
        name = None
        if(confidence<40):
            profile=getProfile(id)
            if profile != None:
                name = str(profile[1])
        else:
            name = "Unknow"

        cv2.putText(frame, name, (x + 10, y+h + 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Camera",frame)
    if cv2.waitKey(1) == ord("q"):  # độ trễ 1/1000s , nếu bấm q sẽ thoát
        break
cap.release()
cv2.destroyAllWindows()