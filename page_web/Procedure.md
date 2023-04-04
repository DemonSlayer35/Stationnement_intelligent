# Procédure pour faire rouler la page Web contenant le schéma du stationnement accessible à tous

1. Installer paho-mqtt (client MQTT) avec ```pip install paho-mqtt``` dans une console cmd.
Télécharger NGINX à partir du site officiel : https://nginx.org/en/download.html, puis décompresser le dossier.

2. Récupérer les fichiers page_web.html, script.js et camera.py.

3. Créer un dossier js (pour les fichiers JavaScript) dans le répertoire de NGINX et y déposer script.js :

![image](https://user-images.githubusercontent.com/89463240/218909744-715d9c85-c67a-40bb-b4e8-0f75b28a148b.png)

4. Placer le fichier page_web.html dans le dossier html de NGINX.

5. Ouvrir le fichier nginx.conf (configuration de NGINX) situé dans le dossier conf de NGINX :

![image](https://user-images.githubusercontent.com/89463240/218909025-491fdb17-2edd-4e4a-b218-e89fd8c54dd2.png)

6. Dans la section non-commentée qui commence par server{listen 80;, ajouter un bloc pour la location du dossier JavaScript comme suit :

![image](https://user-images.githubusercontent.com/89463240/218909527-c1ef1d6e-9860-4eb6-ac28-eef17fd967b4.png)

(Mettre le chemin correspondant en conséquence.)

7. Enregistrer le fichier et fermer nginx.conf (Notez qu'il faut repartir nginx.exe à chaque modification.)

8. Modifier le fichier script.js en entrant l'adresse IP de l'hôte pour la connexion MQTT et le bon nom de topic:
```
// Créez un nouveau client MQTT
const client = new Paho.Client("10.240.9.128", 8080, "myclientid_");
const topic = "parking/A";
```
     
9. Enregistrer le fichier et repartir nginx.exe

10. Assurez-vous que la bonne caméra est utilisée dans le fichier camera.py 
  - ```cap = cv2.VideoCapture(0)  # 0 = Webcam intégrée ; 1 = Caméra USB```

11. Démarrer NGINX en double-cliquant sur nginx.exe (C'est normal si rien ne s'affiche.)
  - Si vous voulez être sûr que NGINX fonctionne, aller à l'adresse localhost et vous devriez voir la page index.html suivante :

![image](https://user-images.githubusercontent.com/89463240/218911227-9a593f26-bed6-46c0-88f8-f0511b6e5e75.png)

12. Télécharger Mosquitto à partir du site officiel : [https://nginx.org/en/download.html](https://mosquitto.org/download/).

13. Ouvrir le fichier de configuration de Mosquitto (mosquitto.conf) et ajouter les lignes suivantes à la fin du fichier:
```
listener 1883
listener 8080 
protocol websockets
allow_anonymous true
socket_domain ipv4
```
![image](https://user-images.githubusercontent.com/89463240/223537293-a6bda1dd-a7c2-478f-a99b-b880ac6a1df0.png)

14. Démarrer le serveur Mosquitto avec la commande ```mosquitto -c mosquitto.conf``` dans une console cmd.

15. Exécuter le fichier 📷camera.py depuis une console cmd avec ```py camera.py```.
  - Cela va démarrer la détection des emplacements de stationnement. Après chaque cycle de 20 frames, la liste est mise à jour sur le serveur Mosquitto
  à [l'adresse IP de l'hôte]:1883
  (Les autres usagers aussi peuvent accéder à la page qui va se mettre à jour avec les données à [l'adresse IP de l'hôte]:8080/).

16. Accéder au 🕸️site Web à [l'adresse IP de l'hôte]/page_web.html

![image](https://user-images.githubusercontent.com/89463240/229799847-bbabdcea-edff-41ef-8f00-d739b08939c4.png)
