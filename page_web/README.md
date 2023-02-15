## app.py
* Le fichier app.py est un programme Python qui utilise le framework Flask pour créer une API web. 
L'API permet à un utilisateur de récupérer et de mettre à jour une liste de 18 valeurs appelée moyenne.

* Lorsqu'un utilisateur envoie une requête GET à la route "/moyenne", l'API renvoie la liste moyenne sous forme de JSON.

* Lorsqu'un utilisateur envoie une requête POST à la route "/moyenne" avec une liste de 18 valeurs, 
l'API met à jour la liste moyenne avec les nouvelles valeurs et renvoie la liste mise à jour sous forme de JSON.

* Le module flask_cors est également utilisé pour permettre l'accès à l'API depuis n'importe quel site web,
en contournant les restrictions de sécurité normalement en place pour les requêtes effectuées à partir de sites tiers.

* Il faut installer flask avec ```pip install flask``` et flask_cors avec ```pip install -U flask-cors```.

## page_web.html
* Ce fichier HTML contient une page web qui affiche un canvas avec une bordure noire. 

* Le canvas a une largeur de 1152 pixels et une hauteur de 648 pixels. 

* Le script JavaScript situé dans le fichier "C:/nginx-1.23.3/js/script.js" est chargé sur la page web.

## script.js
* Ce fichier JavaScript est utilisé pour dessiner une grille de parkings sur un canvas HTML et
pour récupérer une liste de disponibilité de ces parkings à partir d'une API REST (de app.py).

* Il commence par définir les dimensions de l'écran de dessin et la variable "liste" qui sera utilisée pour stocker les données récupérées depuis l'API.

* Ensuite, il va récupérer les données de l'API () en utilisant l'URL de l'API (IP de l'hôte:5000/moyenne).

* Les parkings disponibles sont remplis de vert et les parkings occupés sont remplis de rouge. Les numéros de parking sont également affichés à l'intérieur des rectangles.

* Toutes les 5 secondes, les données affichées sur le canvas HTML sont mises à jour.
