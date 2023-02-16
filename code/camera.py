import cv2 # OpenCV
import numpy as np
import torch
import time
import math

model = torch.hub.load('C:/yolov5', 'custom', path='C:/yolov5/Stationnement_intelligent/data_parking/bestv5m.pt', source='local')
model.conf = 0.45  # Confiance minimale pour utilisation

cap = cv2.VideoCapture(1)  # 0 = Webcam intégrée ; 1 = Camera USB

#values_x = [[41, 205], [66, 202], [92, 205], [102, 212], [113, 218], [124, 221], [131, 227], [142, 233], [146, 234], [303, 393], [310, 397], [312, 406], [314, 414], [313, 425], [320, 431], [319, 444], [324, 463], [325, 487]]
#values_y = [[377, 480], [313, 406], [254, 339], [212, 284], [166, 232], [127, 193], [95, 150], [66, 117], [38, 83], [29, 84], [62, 113], [88, 148], [121, 187], [166, 221], [201, 285], [256, 321], [298, 393], [367, 471]]

values_x = []
values_y = []
parkingLot = []
sortedLot = []

moyenne = [0] * 18


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
            x1, y1, x2, y2 = [int(i) for i in i[:4]]
            coorLogo.append([(x1 + x2) / 2, (y1 + y2) / 2])
        elif i[5] == 0:
            x1, y1, x2, y2 = [int(i) for i in i[:4]]
            parkingLot.append([(x1 + x2) / 2, (y1 + y2) / 2])
    coorLogo = sorted(coorLogo, key=lambda coord: coord[1],reverse=True)
    print(coorLogo)

    for i in range(len(liste)):
        liste[i] = liste[i][:-2]
    
    #parkingLot = list(zip(liste, parkingLot))

    angle = (math.degrees(math.atan2(coorLogo[0][0]-coorLogo[1][0],coorLogo[0][1]-coorLogo[1][1]))) 
    print("L'angle est de ",angle)
    def classement(coord):
        x,y = coord[0]-coorLogo[1][0], coord[1] - coorLogo[1][1]
        print(((math.degrees(math.atan2(y, x))) + 360) % 360)
        return (((math.degrees(math.atan2(y, x))) + 360 - 90+ angle) % 360)
    sortedLot = sorted(parkingLot,key=classement)
    print(parkingLot)
    print(sortedLot)
    print("fin du trie")


    combined_list = list(zip(liste, parkingLot, sortedLot))
    print(combined_list)
    sorted_list = sorted(combined_list, key=lambda x: sortedLot.index(x[2]))
    print(sorted_list)
    sorted_coords_rectangles = [x[0] for x in sorted_list]
    print(sorted_coords_rectangles)


    



    for x in range(len(sortedLot)):
        cv2.putText(frame,str(x),(int(sortedLot[x][0]),int(sortedLot[x][1])),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2,cv2.LINE_AA)
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

    print(moyenne)
    cv2.imshow("Détection d'objets", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    if cv2.waitKey(1) == 27:  # 27 est la valeur de la touche "Esc"
        break

cap.release()
cv2.destroyAllWindows()