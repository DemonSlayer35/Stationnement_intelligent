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

while cap.isOpened():
    try:
        ret, frame = cap.read()
        #cv2.imshow('frame', frame)
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break
        #img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        results = model(frame)
        liste = results.xyxy[0].tolist()
        for x in range(len(liste)):
            value_argon = (liste[x][5])
            value_conf = liste[x][4]
        print(results)
        

    except:
        print("An exception occurred")
    time.sleep(5)
    cv2.destroyAllWindows()
