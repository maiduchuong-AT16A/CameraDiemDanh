from email.mime import image
import cv2
import numpy as np
import os
from PIL import Image

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("C:\\Users\\ACER\\PycharmProjects\\hello\\venv\\Lib\\site-packages\\cv2\\data\\haarcascade_frontalface_default.xml")
path = "dataSet"

def getImageWithId(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    #print(imagePaths)

    faces = []
    IDs = []

    for image in imagePaths:
        faceImg = Image.open(image).convert('L')
        faceNp = np.array(faceImg, 'uint8')
        Id = int(image.split("\\")[1].split('.')[1])
        
        faces.append(faceNp)
        IDs.append(Id)

        '''cv2.imshow("frame",faceNp)
        cv2.waitKey(1)'''
    return faces,IDs
faces,Ids = getImageWithId(path)

#recognizer.train(faces, np.array(Ids))
print(Ids)
'''if not os.path.exists('recognizer'):
    os.makedirs('recognizer')
recognizer.save("recognizer\\trainingData.yml")'''

cv2.destroyAllWindows()