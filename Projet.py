import cv2 #OpenCV
from time import sleep
import time
from datetime import datetime
import torch
from matplotlib import pyplot as plt
from scipy import ndimage
import numpy as np
import os
from PIL import Image
#import detect

confiance = 0.45
path = '/'
model_name='best.pt'
#model = detect
model = torch.hub.load(os.getcwd(), 'custom', source='local', path = model_name)
model.conf = confiance # confiance minimale pour utilisation

cap = cv2.VideoCapture(1) # 0 = Webcam integre ; 1 = Camera USB

def parking(coordinate,frame):
    liste = results.xyxy[0].tolist()
    print(coordinate)
    for x in liste:
        if x[5]==0.0:
            x1, y1, x2, y2 = x[:4]
            emplacement = [(x[0]+x[2])/2,(x[1]+x[3])/2]
            print(emplacement)
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)  # Dessiner le rectangle
            cv2.imshow("Détection d'objets", frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
    tete = 90
    #print(coordinate)
    


while cap.isOpened():
    try:
        ret, frame = cap.read()
        #cv2.imshow('frame', frame)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break
        #img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        results = model(frame)
        #liste = results.xyxy[0].tolist()
        #for x in range(len(liste)):
        #    value_argon = (liste[x][5])
        #    value_conf = liste[x][4]
        #print(results)
        #frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        #parking(results,frame)

        liste = results.xyxy[0].tolist()
        print(results)
        for x in liste:
            if x[5]==0.0:
                x1, y1, x2, y2 = [int(x) for x in x[:4]]
                emplacement = [(x1+x2)/2,(y1+y2)/2]
                print(emplacement)
                frame = np.array(frame)
                cv2.rectangle(frame, (x1, y1), (x2,y2), (255, 0, 0), 2)  # Dessiner le rectangle
            if x[5]==1.0:
                x1, y1, x2, y2 = [int(x) for x in x[:4]]
                emplacement = [(x1+x2)/2,(y1+y2)/2]
                print(emplacement)
                frame = np.array(frame)
                cv2.rectangle(frame, (x1, y1), (x2,y2), (0, 255, 0), 2)  # Dessiner le rectangle
        cv2.imshow("Détection d'objets", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()



        

    except:
        print("An exception occurred")
    #time.sleep(10)
    #cv2.destroyAllWindows()