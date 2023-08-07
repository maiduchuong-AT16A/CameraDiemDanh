from pickle import TRUE
from tkinter.ttk import Style
from tokenize import Name
from django.shortcuts import render
import cv2
import os
import pandas as pd
import datetime
from pandas import DataFrame
from PIL import Image,ImageDraw, ImageFont
import numpy as np

# Create your views here.
from django.http import HttpResponse, StreamingHttpResponse
from .models import DataCam as data_webcam

df = pd.read_csv('txt.csv')
list=[]
listID = df['ID']
date_object = datetime.date.today()
for i in range (df.__len__()):
    list.append([listID[i],0,0])
    

def index(request):
    return render(request,"index.html")

def AddFace(request):
    return render(request,'add.html')

def write(request):
    if request.method == "POST":
        date_object = datetime.date.today()
        str = date_object.__str__()
        listWrite = []
        for i in range(0,df.__len__()):
            listWrite.append(list[i][2])
        print(listWrite)
        df[str]=listWrite
        export_csv = df.to_csv (r'txt.csv', index = None, header=True) #ghi vào file
        print(df)
        list.clear()
        for i in range (df.__len__()):
            list.append([listID[i],0,0])
        return render(request,"index.html")
    else:
        return render(request,"error.html")

#thêm dữ liệu
def requestFaceID(request):
    if request.method == "POST":
        global IdAdd 
        global Id
        global name
        Id = request.POST['ID']
        IdAdd = Id
        name = request.POST['Name']
        '''Data_list = data_webcam.objects.filter().order_by('Id')
        for i in Data_list:
            print(type(i))
            if(int(i) == int(Id)):
                return render(request,"error.html")'''
        return render(request,"addface.html")
    else:
        return render(request,"error.html")


def requestInsertMySql(request):
    #Data_list = data_webcam.objects.filter().order_by('Id')
    # for i in Data_list:
    #     print(type(i))
    #     if(int(str(i)[2:]) == Id):
    #         face = data_webcam.objects.update(Id = Id,name = name)
    #         return render(request,"add.html")
    # face = data_webcam.objects.update(Id = Id,name = name)
    face = data_webcam.objects.create(Id = Id,name = name)
    face.save()
    tranning()
    return render(request,"add.html")
   
       

#xác định tên của id
def getProfile(Id):
    Data_list = data_webcam.objects.filter().order_by('Id')
    profile = None
    for row in Data_list:
        if(int((row.Id)[2:]) == int(Id)):
            profile=locDau(str(row.name))

    return profile

recognizer = cv2.face.LBPHFaceRecognizer_create() #cái này dùng để train dữ liệu
face_cascades = cv2.CascadeClassifier("C:\\Users\\ACER\\PycharmProjects\\hello\\venv\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml")
recognizer.read("recognizer\\trainingData.yml")#dữ liệu đc mã hóa file yml
path = "dataSet"



#nhận diện khuân mạt
def stream():
    cap = cv2.VideoCapture(0) 

    while True:
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascades.detectMultiScale(gray,1.1,10)

        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(w+x+10,y+h+10),(0,255,0),2)

            roi_gray = gray[y:y+h+10,x:x+w+10]

            id,confidence = recognizer.predict(roi_gray)
            

            name = None
            if(confidence<40):
                profile=getProfile(id)
                if profile != None:
                    name = str(profile)
                    for i in range(listID.__len__()):
                        if(list[i][1] > 80):
                            list[i][2]=1
                        if (int(id) == int(str(listID[i])[2:]) and list[i][1] <=80):
                            list[i][1]+=1
                        print(list)
            else:
                name = "Unknow"
            cv2.putText(frame, name, (x + 20, y+h + 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


        if not ret:
            print("Error: failed to capture image")
            break

        cv2.imwrite('video.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('video.jpg', 'rb').read() + b'\r\n')

def video_feed(request):
    return StreamingHttpResponse(stream(), content_type='multipart/x-mixed-replace; boundary=frame')


def addData():
    cap = cv2.VideoCapture(0)
    sampleNum = 0
    
    while True:
        ret, frame = cap.read()

        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        faces = face_cascades.detectMultiScale(gray,1.1,10)

        for(x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w+15,y+h+15),(0,255,0),2)

            #tao forder
            if not os.path.exists('dataSet'):
                os.makedirs('dataSet')
            sampleNum = sampleNum+1

            cv2.imwrite('dataSet/User.'+str(IdAdd)+'.'+str(sampleNum)+'.jpg',gray[y: y+h+15,x: x+w+15])

        cv2.imwrite('video.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('video.jpg', 'rb').read() + b'\r\n')

        if sampleNum>50:
            break

def video_add(request):
    return StreamingHttpResponse(addData(), content_type='multipart/x-mixed-replace; boundary=frame')


    

def write_file(ID):
    '''date_object = datetime.date.today()
    for i in range (df.__len__()):
        list.append(0)
    for i in range(listID.__len__()):
        if ID == listID[i]:
            list[i] = 1
    
    id = int(input("Enter ID:"))
    if(id == 1):
        str = date_object.__str__()
        df[str]=list
        export_csv = df.to_csv (r'txt.csv', index = None, header=True) #ghi vào file
        print(df)'''



def getImageWithId(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    print(imagePaths)

    faces = []
    IDs = []

    for image in imagePaths:
        faceImg = Image.open(image).convert('L')
        faceNp = np.array(faceImg, 'uint8')

        Id = int((image.split("\\")[1].split('.')[1])[2:])
        faces.append(faceNp)
        IDs.append(Id)

    return faces,IDs

def tranning():
    faces,Ids = getImageWithId(path)
    print(Ids)
    recognizer.train(faces, np.array(Ids))

    if not os.path.exists('recognizer'):
        os.makedirs('recognizer')
    recognizer.save("recognizer\\trainingData.yml")

def locDau(str):
    VietnameseSigns = ["aAeEoOuUiIdDyY", "áàạảãâấầậẩẫăắằặẳẵ", "ÁÀẠẢÃÂẤẦẬẨẪĂẮẰẶẲẴ", "éèẹẻẽêếềệểễ", "ÉÈẸẺẼÊẾỀỆỂỄ",
                       "óòọỏõôốồộổỗơớờợởỡ",
                       "ÓÒỌỎÕÔỐỒỘỔỖƠỚỜỢỞỠ", "úùụủũưứừựửữ", "ÚÙỤỦŨƯỨỪỰỬỮ", "íìịỉĩ", "ÍÌỊỈĨ", "đ", "Đ", "ýỳỵỷỹ", "ÝỲỴỶỸ"]
    for i in range(1,VietnameseSigns.__len__()):
        for j in range(0,VietnameseSigns[i].__len__()):
            str = str.replace((VietnameseSigns[i])[j], (VietnameseSigns[0])[i - 1])
    return str
