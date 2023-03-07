## app.py (Remplacé par MQTT)
~~* Le fichier app.py est un programme Python qui utilise le framework Flask pour créer une API web. 
L'API permet au fichier camera.py de mettre à jour la liste moyenne de l'état des 18 stationnements.

~~* Lorsqu'un utilisateur envoie une requête GET à la route "/moyenne", l'API renvoie la liste moyenne sous forme de JSON.

~~* Lorsque camera.py envoie une requête POST à la route "/moyenne" avec une liste de 18 valeurs, 
l'API met à jour la liste moyenne avec les nouvelles valeurs et renvoie la liste mise à jour sous forme de JSON.

~~* Le module flask_cors est également utilisé pour permettre l'accès à l'API depuis n'importe quel site web,
en contournant les restrictions de sécurité normalement en place pour les requêtes effectuées à partir de sites tiers.

~~* Il faut installer flask avec ```pip install flask``` et flask_cors avec ```pip install -U flask-cors```.

## page_web.html
* Ce fichier HTML contient une page web qui affiche un canevas avec une texture d'asphalte. 

* Le canevas s'ajuste selon la taille de l'affichage. 

* Le script JavaScript situé dans le fichier "C:/nginx-1.23.3/js/script.js" est chargé sur la page web.

* C'est le script qui se charge de dessiner les emplacements de stationnement.

## script.js
* Ce fichier JavaScript est utilisé pour dessiner une grille de parkings sur un canevas HTML et
pour récupérer une liste de disponibilité de ces parkings à partir d'un serveur MQTT (Mosquitto).

* Il commence par définir les dimensions de l'écran de dessin et la variable "obj" qui sera utilisée pour stocker les données récupérées depuis le topic MQTT.

* Ensuite, il va récupérer les données du topic MQTT en utilisant l'URL du serveur MQTT (IP de l'hôte:8080).

* Les parkings disponibles sont remplis de vert et les parkings occupés sont remplis de rouge. Les numéros de parking sont également affichés à l'intérieur des rectangles.

* Toutes les 2 secondes, les données affichées sur le canvas HTML sont mises à jour.

## test_web.py
* Ce fichier est un script Python pour tester la publication de la liste en MQTT au lieu de Flask.

* Dans le code, il y a une boucle qui change l'état des stationnements aux secondes.
