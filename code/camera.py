#----------------------------------------------------------------------------
# Created By  : Etienne Dubé & Mohammad Barin Wahidi
# Created Date: 6 février 2023
# version ='1.0'
# ---------------------------------------------------------------------------
""" Projet utilisant un modèle entrainé avec YOLOv5 pour reconnaitre des places de stationnement vides et occupées. Le programme utilise OpenCV pour récupérer les images en provenance d'une caméra, 
les images sont ensuite analysées par le modèle en utilisant PyTorch. Le programme commence par trier dans l'ordre désiré les places de stationnement. Ensuite, le programme analyse, en boucle, les images. 
Les données sont envoyées par protocole MQTT à un serveur externe d'où les données peuvent être traitées pour les afficher aux utilisateurs."""
# ---------------------------------------------------------------------------

import cv2 # OpenCV pour la manipulation d'images et de vidéos
import numpy as np # Numpy pour les opérations mathématiques
import torch  # PyTorch pour le deep learning
import time  # Pour la gestion du temps
import math  # Pour les fonctions mathématiques
import paho.mqtt.client as mqtt  # Pour la communication MQTT (installé avec `pip install paho-mqtt`)
import json # Pour manipuler les données JSON


# Charger le modèle personnalisé YOLOv5
model = torch.hub.load('C:/yolov5', 'custom', path='C:/yolov5/Stationnement_intelligent/data_parking/bestv5m.pt', source='local')
model.conf = 0.35                                                           #Confiance minimale pour utilisation

# Ouvrir la vidéo de la caméra
cap = cv2.VideoCapture(1)                                                   #0 = Webcam intégrée ; 1 = Camera USB (dans le cas de ma configuration, si pas de caméra intégré 0=caméra USB)

# Initialiser les listes pour stocker les données
NB_PARKING = 18                                                             #Nombre d'emplacements dans le stationnement
parkingLot = []                                                             #Pour les emplacements de stationnements trouvés par le modèle d'entrainement
sortedLot = []                                                              #Pour les emplacements de stationnements triés à partir de parkingLot dans l'ordre désiré
values_x = []                                                               #Contient les deux valeurs X de (x,y,x,y) dans sortedLot
values_y = []                                                               #Contient les deux valeurs y de (x,y,x,y) dans sortedLot
moyenne = [0] * NB_PARKING                                                  #Un tableau pour faire une moyenne de x nombres d'images avant de les afficher

def publish_mqtt(topic, payload):
    # Fonction pour le protocole MQTT
    # Param topic : Nom du stationnement
    # Param payload : liste des places libres et occupées

    client = mqtt.Client()                                                  #Créez un client MQTT
    client.connect("192.168.0.101", 1883, 5)                                #Connectez le client au broker MQTT

    places = [{"id": i+1, "etat": 'libre' if payload[i] <= 0.5 else 'occupe'} for i in range(len(payload))]
    data = {}                                                               #Création d'un dictionnaire pour stocker les données
    data['parking'] = 'A'                                                   #Ajout des tags pour le parking A
    data['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  #Ajout d'un tag pour le temps
    data["places"] = places
    json_data = json.dumps(data)                                            #Convertir le dictionnaire en JSON

    client.publish(topic, json_data)                                        #Publiez le payload sur le topic spécifié
    client.disconnect()                                                     #Déconnectez le client MQTT

def positionnement():
    # Fonction pour trier les positions des places de stationnement dans l'ordre voulu
    global parkingLot,values_x,values_y,sortedLot                           #Les variables globales modifiables utilisées (variables cap & model ne sont pas déclarées global, puisqu'elles ne sont pas modifiables)
    coorLogo = [] 
    while True:                                                             #Boucle qui vérifie si le bon nombre de places est détecté avant de continuer
                                                                            
        ret, frame = cap.read()  
        results = model(frame)                                              #L'image est analysée par le modele et les résultats sont retournés sous forme d'objets
        liste = results.xyxy[0].tolist()                                    #Les positions xyxy de tous les stationnements sont retournées sous forme de liste
        nbLogo = [sublist for sublist in liste if sublist[5] == 2]          #Tous les sublists dans la liste sont vérifiés et si la position 5 de la sublist = 2, la sublist est ajoutée à nbLogo
        nbParkingVide = [sublist for sublist in liste if sublist[5] == 0]   
        print(len(nbLogo),len(nbParkingVide))
        if len(nbLogo) == 2 and len(nbParkingVide)==NB_PARKING:             #Vérifie si le bon nombre de logos et de stationnements est présent.
            break

    for i in liste:                                                         #Boucle pour enregistrer les points milieux des logos et des stationnements                                                               
        if i[5] == 2:
            x1, y1, x2, y2 = [round(i) for i in i[:4]]
            coorLogo.append([(x1 + x2) / 2, (y1 + y2) / 2])

        elif i[5] == 0:
            x1, y1, x2, y2 = [round(i) for i in i[:4]]
            parkingLot.append([round((x1 + x2) / 2),round((y1 + y2) / 2)])
    coorLogo = sorted(coorLogo, key=lambda coord: coord[1],reverse=True)    #Trie les logos, le plus près de la caméra est en première position.
    print(coorLogo)
    indexLogo = []
    for i in range(len(liste)):                                             #Boucle qui enregistre le No de l'index dans la liste et arrondit à l'unité les coordonnées de la liste
        if liste[i][5] == 2.0:
            indexLogo.append(i)
        
        for j in range(4):
            liste[i][j] = round(liste[i][j])
    indexLogo = sorted(indexLogo, reverse=True)
    for x in indexLogo:                                                     #Supprime les logos de la liste
        liste.pop(x)
    liste = list(zip(liste,parkingLot))                                     #Combine les deux listes 

    angle = (math.degrees(math.atan2(coorLogo[0][0]-coorLogo[1][0],coorLogo[0][1]-coorLogo[1][1])))     #Récupère l'angle que forment les 2 logos
    print("L'angle est de ",angle)
    def classement(coord):
        #Fonction pour le classement des coordonnées
        x,y = coord[0]-coorLogo[1][0], coord[1] - coorLogo[1][1]
        print(((math.degrees(math.atan2(y, x))) + 360) % 360)
        return (((math.degrees(math.atan2(y, x))) + 360 - 90+ angle) % 360)
    
    sortedLot = sorted(liste,key=lambda x: classement(x[1]))                #Trie les coordonnées de la liste avec la fonction classement
    print(parkingLot)
    print(sortedLot)
    print("fin du tri")

    for i in range(len(sortedLot)):                                         #Boucle pour récupérer toute les données X et Y dans 2 listes
        values_x.append(sortedLot[i][0][:4:2])
        values_y.append(sortedLot[i][0][1:4:2])
    #breakpoint()
    for x in range(len(sortedLot)):                                         #Affiche l'image avec les numéros de stationnement dans l'ordre voulu
        cv2.putText(frame,str(x),(int(sortedLot[x][1][0]),int(sortedLot[x][1][1])),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2,cv2.LINE_AA)
    cv2.imshow("Détection d'objets", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

for i in range(50):
    ret, frame = cap.read()                                                 #Les premières images ne sont pas traitables
positionnement()
while cap.isOpened():                                                       #Boucle principale, affiche les places libres et occupées
    ret, frame = cap.read()
    if not ret:
        break
    j = 0
    
    while(j < 20):                                                          #Calcule la moyenne sur 20 images
        results = model(frame)                                              #L'image est analysée par le modèle et les résultats sont retournés sous forme d'objets
        liste = results.xyxy[0].tolist()
        indexLogo = []
        for i in range(len(liste)):                                         
            if liste[i][5] == 2.0:
                indexLogo.append(i)
        indexLogo = sorted(indexLogo, reverse=True)                         
        for x in indexLogo:                                                 #Retire les logos de la liste
            liste.pop(x)
        for i, x in enumerate(liste):
            x1, y1, x2, y2 = [int(x) for x in x[:4]]
            emplacement = [(x1 + x2) / 2, (y1 + y2) / 2]                    #Calcule les points milieux des éléments de la liste
            for i in range(len(values_x)):                                  #Vérifie si l'élément se trouve dans l'une des places de stationnement
                if values_x[i][0] <= emplacement[0] <= values_x[i][1] and values_y[i][0] <= emplacement[1] <= values_y[i][1]:
                    moyenne[i] += x[5]
        j += 1

    frame = np.array(frame)
    for i in range(len(values_x)):                                          #Boucle qui affiche les places à l'écran
        moyenne[i] /= 20
        color = (255, 0, 0) if moyenne[i] <= 0.5 else (0, 255, 0)
        cv2.rectangle(frame, (values_x[i][0], values_y[i][0]), (values_x[i][1], values_y[i][1]), color, 2) #Place un rectangle à chaque place de stationnement
        if moyenne[i] > 0.5:
            print("La voiture se trouve dans le parking", i+1)              #Écrit dans la console les places occupées
    publish_mqtt("parking/A", moyenne)
    print(moyenne)
    for x in range(len(moyenne)):                                           #Remise à zéro de la liste des moyennes
        moyenne[x] = 0
    """cv2.imshow("Détection d'objets", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    if cv2.waitKey(1) == 27:  # 27 est la valeur de la touche "Esc"
        break """

cap.release()
cv2.destroyAllWindows()