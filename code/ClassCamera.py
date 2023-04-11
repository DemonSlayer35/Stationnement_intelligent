import cv2  # OpenCV
import numpy as np
import torch
import time
import math
import paho.mqtt.client as mqtt  # pip install paho-mqtt
import json


class ParkingDetector:
    def __init__(self, camera):
        self.model = torch.hub.load('C:/yolov5', 'custom', path='C:/yolov5/Stationnement_intelligent/data_parking/bestv5m.pt', source='local')
        self.model.conf = 0.35  # Confiance minimale pour utilisation

        self.cap = cv2.VideoCapture(camera)  # 0 = Webcam intégrée ; 1 = Camera USB

        self.values_x = []
        self.values_y = []
        self.parkingLot = []
        self.sortedLot = []

        self.moyenne = [0] * 18

    def publish_mqtt(self, topic, payload):
        try:
            # Créez un client MQTT
            client = mqtt.Client()

            # Connectez le client au broker MQTT
            client.connect("10.240.9.128", 1883, 5)#10.240.9.128  localhost   8080

            places = [{"id": i+1, "etat": 'libre' if payload[i] < 1 else 'occupe'} for i in range(len(payload))]

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

            # Déconnectez le client MQTT
            client.disconnect()
        except:
            print("Serveur indisponible")

    def positionnement(self):
        global parkingLot, values_x, values_y, sortedLot
        coorLogo = []
        while True:
            ret, frame = self.cap.read()
            results = self.model(frame)
            liste = results.xyxy[0].tolist()
            nbLogo = [sublist for sublist in liste if sublist[5] == 2]
            nbParkingVide = [sublist for sublist in liste if sublist[5] == 0]
            print(len(nbLogo), len(nbParkingVide))
            if len(nbLogo) == 2 and len(nbParkingVide) == 18:
                break

        print(results)
        for i in liste:
            if i[5] == 2:
                x1, y1, x2, y2 = [round(i) for i in i[:4]]
                coorLogo.append([(x1 + x2) / 2, (y1 + y2) / 2])

            elif i[5] == 0:
                x1, y1, x2, y2 = [round(i) for i in i[:4]]
                self.parkingLot.append([round((x1 + x2) / 2), round((y1 + y2) / 2)])
        coorLogo = sorted(coorLogo, key=lambda coord: coord[1], reverse=True)
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
        liste = list(zip(liste, self.parkingLot))

        angle = (math.degrees(math.atan2(coorLogo[0][0] - coorLogo[1][0], coorLogo[0][1] - coorLogo[1][1])))
        print("L'angle est de ", angle)

        def classement(coord):
            x, y = coord[0] - coorLogo[1][0], coord[1] - coorLogo[1][1]
            print(((math.degrees(math.atan2(y, x))) + 360) % 360)
            return (((math.degrees(math.atan2(y, x))) + 360 - 90 + angle) % 360)

        self.sortedLot = sorted(liste, key=lambda x: classement(x[1]))
        print(self.parkingLot)
        print(self.sortedLot)
        print("fin du trie")

        for i in range(len(self.sortedLot)):
            self.values_x.append(self.sortedLot[i][0][:4:2])
            self.values_y.append(self.sortedLot[i][0][1:4:2])
        # breakpoint()
        for x in range(len(self.sortedLot)):
            cv2.putText(frame, str(x), (int(self.sortedLot[x][1][0]), int(self.sortedLot[x][1][1])), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.imshow("Détection d'objets", frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def detect(self):
        for i in range(50):
            ret, frame = self.cap.read()  # Les première images ne sont pas traitable
        self.positionnement()
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break
            j = 0

            while (j < 20):

                results = self.model(frame)
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

                    for i in range(len(self.values_x)):
                        if self.values_x[i][0] <= emplacement[0] <= self.values_x[i][1] and self.values_y[i][0] <= emplacement[1] <= self.values_y[i][1]:
                            self.moyenne[i] += x[5]

                j += 1

            frame = np.array(frame)
            for i in range(len(self.values_x)):
                self.moyenne[i] /= 20
                color = (255, 0, 0) if self.moyenne[i] <= 0.5 else (0, 255, 0)
                cv2.rectangle(frame, (self.values_x[i][0], self.values_y[i][0]), (self.values_x[i][1], self.values_y[i][1]), color, 2)
                if self.moyenne[i] > 0.5:
                    print("La voiture se trouve dans le parking", i + 1)
            self.publish_mqtt("parking/A", self.moyenne)
            print(self.moyenne)
            for x in range(len(self.moyenne)):
                self.moyenne[x] = 0
            """cv2.imshow("Détection d'objets", frame)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            if cv2.waitKey(1) == 27:  # 27 est la valeur de la touche "Esc"
                break """

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    detector = ParkingDetector()
    detector.detect()
