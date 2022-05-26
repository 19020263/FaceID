import base64
import pickle
import numpy as np
import cv2
import os, os.path
import datetime
import requests

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, "images/n_d_dung")

face_cascade = cv2.CascadeClassifier('data\haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("./recognizers/face-trainner.yml")

labels = {"person_name": 1}
with open("pickles/face-labels.pickle", 'rb') as f:
	og_labels = pickle.load(f)
	labels = {v:k for k,v in og_labels.items()}

cap = cv2.VideoCapture(0)

while(True):

    ret, frame = cap.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    for (x, y, w, h) in faces:
        #print(f"x: {x}; y: {y}; w: {w}; h: {h}")
        roi_gray = gray[y:y+h, x:x+w]
        id_, conf = recognizer.predict(roi_gray)
        if conf >= 45 and conf <= 85:
            #print(id_)
            #print(labels[id_])
            name = labels[id_]
            font = cv2.FONT_HERSHEY_SIMPLEX
            color = (0, 255, 0)
            stroke = 2
            cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)

        color = (255, 0, 0) #BGR 0 - 255
        stroke = 2
        end_cord_x = x + w
        end_cord_y = y + h
        cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)

    cv2.imshow('frame',frame)
    if cv2.waitKey(20) & 0xFF == ord('g'):
        img_item = "images/face-images.png"
        cv2.imwrite(img_item, frame)
        with open("images/face-images.png", 'rb') as f:
            img = base64.b64encode(f.read())
        if name:
            
            params = {
              "params": {
                "name": name,
                "img": img.decode("utf-8")
              }
            }
            r =  requests.get('http://127.0.0.1:8069/faceid/create', json=params)
            if r:
                print("Send request success!!!")
            else:
                print("Error!!!")
        else:
            print("Name is not defined")
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()