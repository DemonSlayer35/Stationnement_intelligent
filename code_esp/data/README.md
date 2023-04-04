## captive_portal.html
* Ce fichier HTML contient une page web qui affiche un canevas avec un fond gris. 

* Le canevas s'ajuste selon la taille de l'affichage. 

* Le script JavaScript situé dans le même dossier est chargé sur la page web.

* C'est le script qui se charge de dessiner les emplacements de stationnement.

## script.js
* Ce fichier JavaScript est utilisé pour dessiner une grille de parkings sur un canevas HTML et
pour récupérer une liste de disponibilité de ces parkings à partir d'un serveur MQTT (Mosquitto).

* Il commence par définir les dimensions de l'écran de dessin et la variable "obj" qui sera utilisée pour stocker les données de la liste de places JSON.

* Les parkings disponibles sont remplis de vert et les parkings occupés sont remplis de rouge. Les numéros de parking sont également affichés à l'intérieur des rectangles.

* Toutes les 2 secondes, il va récupérer les données depuis l'endpoint /content pour mettre à jour les données affichées sur le canevas HTML.
