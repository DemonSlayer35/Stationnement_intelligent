import paho.mqtt.client as mqtt # pip install paho-mqtt
import json
import time

def publish_mqtt(topic, payload):
    # Créez un client MQTT
    client = mqtt.Client()

    # Connectez le client au broker MQTT
    client.connect("localhost", 1883, 60)

    # Création d'un dictionnaire pour stocker les données
    data = {}

    # Ajout des tags pour le parking A
    data['parking'] = 'A'

    # Ajout d'un tag pour le temps
    data['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    # Ajout des tags pour chaque place de parking
    for i in range(len(payload)):
        data[f'place {i+1}'] = 'libre' if payload[i] < 1 else 'occupé'

    # Convertir le dictionnaire en JSON
    json_data = json.dumps(data)

    # Publiez le payload sur le topic spécifié
    client.publish(topic, json_data)

    # Délai d'attente de 1 seconde
    time.sleep(1)

    # Déconnectez le client MQTT
    client.disconnect()


places = [1] * 18
places[0] = 0

# Itération pour changer les valeurs de la liste
i = 0
while True:
    # Affichage de la liste
    #print(places)
    
    if i == 17:
        places[0] = 0
        places[i] = 1
        i = 0
        continue
    else:
        # Changement de la valeur d'un élément de la liste
        places[i + 1] = places[i]
        places[i] = 1
    
    # Envoyer les données MQTT
    publish_mqtt("parking/A", places)

    i += 1