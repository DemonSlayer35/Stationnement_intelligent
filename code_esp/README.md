## Installation.md 
* Ce fichier contient les procédures d'installation du board ESP32 et des librairies pour le code dans l'IDE Arduino.

## Procedure.md
* Procédure pour faire rouler l'ESP en mode point d'accès avec un portail captif affichant le schéma du stationnement

## code_esp.ino
* Code à téléverser dans l'ESP32 pour générer un point d'accès qui sert la page Web du stationnement intelligent via un portail captif.
* L'ESP est mis en mode point d'accès et en mode station.
* Le côté station se connecte au réseau spécifié. Cette connexion servira à la récupération des données MQTT depuis le broker.
Il faut donc que le broker soit connecté au même réseau.
* Le côté point d'accès permet aux usagers de se connecter à l'ESP.
* Via un serveur DNS, les usagers connectés au point d'accès sont redirigés vers le portail captif.
* Lorsqu'un message (la liste de places libres) est reçu par MQTT, le point de terminaison (endpoint) HTTP à l'adresse "/content" est mis à jour avec
le contenu de la nouvelle liste.
* Ainsi, lorsque le code javascript effectue (aux 2 secondes) une requête GET vers "/content", il reçoit une réponse contenant le contenu de la liste sous forme de JSON.

## data
* Dossier contenant les fichiers pour la page Web à téléverser dans le système de fichiers de l'ESP.
