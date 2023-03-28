import cv2 # OpenCV
import numpy as np
import torch
import time
import math
import paho.mqtt.client as mqtt # pip install paho-mqtt
import json

model = torch.hub.load('C:/yolov5', 'custom', path='C:/yolov5/Stationnement_intelligent/data_parking/bestv5m.pt', source='local')
model.conf = 0.35  # Confiance minimale pour utilisation

cap = cv2.VideoCapture(1)  # 0 = Webcam intégrée ; 1 = Camera USB

values_x = []
values_y = []
parkingLot = []
sortedLot = []

moyenne = [0] * 18

def publish_mqtt(topic, payload):
    # Créez un client MQTT
    client = mqtt.Client()

    # Connectez le client au broker MQTT
    client.connect("192.168.0.101", 1883, 60)#10.240.9.128  localhost   8080

    places = [{"id": i+1, "etat": 'libre' if payload[i] <= 0.5 else 'occupe'} for i in range(len(payload))]

    # Création d'un dictionnaire pour stocker les données
    data = {}

    # Ajout des tags pour le parking A
    data['parking'] = 'A'

    # Ajout d'un tag pour le temps
    data['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    data["places"] = places

    # Convertir le dictionnaire en JSON
    json_data = json.dumps(data)

    # Publiez le payload sur le topic spécifié
    client.publish(topic, json_data)

    # Délai d'attente de 1 seconde
    #time.sleep(1)

    # Déconnectez le client MQTT
    client.disconnect()


def positionnement():
    global parkingLot,values_x,values_y,sortedLot
    coorLogo = []
    while True:
        ret, frame = cap.read()
        results = model(frame)
        liste = results.xyxy[0].tolist()
        nbLogo = [sublist for sublist in liste if sublist[5] == 2] 
        nbParkingVide = [sublist for sublist in liste if sublist[5] == 0]
        print(len(nbLogo),len(nbParkingVide))
        if len(nbLogo) == 2 and len(nbParkingVide)==18:
            break

    print(results)
    for i in liste:
        if i[5] == 2:
            x1, y1, x2, y2 = [round(i) for i in i[:4]]
            coorLogo.append([(x1 + x2) / 2, (y1 + y2) / 2])

        elif i[5] == 0:
            x1, y1, x2, y2 = [round(i) for i in i[:4]]
            parkingLot.append([round((x1 + x2) / 2),round((y1 + y2) / 2)])
    coorLogo = sorted(coorLogo, key=lambda coord: coord[1],reverse=True)
    print(coorLogo)
    indexLogo = []
    for i in range(len(liste)):
        if liste[i][5] == 2.0:
            indexLogo.append(i)
        
        for j in range(4):
            liste[i][j] = round(liste[i][j])
    indexLogo = sorted(indexLogo, reverse=True)
    for x in indexLogo:
        liste.pop(x)
    liste = list(zip(liste,parkingLot))

    angle = (math.degrees(math.atan2(coorLogo[0][0]-coorLogo[1][0],coorLogo[0][1]-coorLogo[1][1]))) 
    print("L'angle est de ",angle)
    def classement(coord):
        x,y = coord[0]-coorLogo[1][0], coord[1] - coorLogo[1][1]
        print(((math.degrees(math.atan2(y, x))) + 360) % 360)
        return (((math.degrees(math.atan2(y, x))) + 360 - 90+ angle) % 360)
    
    sortedLot = sorted(liste,key=lambda x: classement(x[1]))
    print(parkingLot)
    print(sortedLot)
    print("fin du trie")

    for i in range(len(sortedLot)):
        values_x.append(sortedLot[i][0][:4:2])
        values_y.append(sortedLot[i][0][1:4:2])
    #breakpoint()
    for x in range(len(sortedLot)):
        cv2.putText(frame,str(x),(int(sortedLot[x][1][0]),int(sortedLot[x][1][1])),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2,cv2.LINE_AA)
    cv2.imshow("Détection d'objets", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



for i in range(50):
    ret, frame = cap.read() # Les première images ne sont pas traitable
positionnement()
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    j = 0
    
    while(j < 20):

        results = model(frame)
        liste = results.xyxy[0].tolist()
        indexLogo = []
        for i in range(len(liste)):
            if liste[i][5] == 2.0:
                indexLogo.append(i)
        indexLogo = sorted(indexLogo, reverse=True)
        for x in indexLogo:
            liste.pop(x)
        for i, x in enumerate(liste):
            x1, y1, x2, y2 = [int(x) for x in x[:4]]
            
            emplacement = [(x1 + x2) / 2, (y1 + y2) / 2]

            for i in range(len(values_x)):
                if values_x[i][0] <= emplacement[0] <= values_x[i][1] and values_y[i][0] <= emplacement[1] <= values_y[i][1]:
                    moyenne[i] += x[5]

        j += 1

    frame = np.array(frame)
    for i in range(len(values_x)):
        moyenne[i] /= 20
        color = (255, 0, 0) if moyenne[i] <= 0.5 else (0, 255, 0)
        cv2.rectangle(frame, (values_x[i][0], values_y[i][0]), (values_x[i][1], values_y[i][1]), color, 2)
        if moyenne[i] > 0.5:
            print("La voiture se trouve dans le parking", i+1)
    publish_mqtt("parking/A", moyenne)
    print(moyenne)
    for x in range(len(moyenne)):
        moyenne[x] = 0
    """cv2.imshow("Détection d'objets", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    if cv2.waitKey(1) == 27:  # 27 est la valeur de la touche "Esc"
        break """

cap.release()
cv2.destroyAllWindows()