# Stationnement intelligent
Projet de fin de DEC en TSO (Etienne Dubé et Mohammad Barin Wahidi)

## Pour démarrer le projet, il faut d'abord suivre les étapes d'installation des fichiers Installation.md 
(Stationnement_intelligent/Installation.md et Stationnement_intelligent/code_esp/Installation.md)
https://github.com/DemonSlayer35/Stationnement_intelligent/blob/main/Installation.md et
https://github.com/DemonSlayer35/Stationnement_intelligent/blob/main/code_esp/Installation.md

## Ensuite, il faut suivre les étapes d'opération des fichiers Procedure.md
(Stationnement_intelligent/page_web/Procedure.md et Stationnement_intelligent/code_esp/Procedure.md)
https://github.com/DemonSlayer35/Stationnement_intelligent/blob/main/page_web/Procedure.md et https://github.com/DemonSlayer35/Stationnement_intelligent/blob/main/code_esp/Procedure.md

## Installation.md 
* Ce fichier contient les procédures d'installation de la suite Yolov5 et les étapes pour l'entraînement de l'IA ainsi que la détection d'objets.

## KiCad
* Ce dossier contient le projet KiCad (schéma électrique, PCB et fichiers de fabrication) de l'ESP32 pour la barrière de stationnement.

## code 
* Ce dossier contient les scripts en Python pour la détection des images avec la caméra et l'affichage du stationnement sur un écran.
* Le code envoie les résultats de la détection d'emplacements libres par MQTT au broker pour la construction de la page Web du stationnement.

## code_esp
* Ce dossier contient le code (code_esp.ino) à téléverser dans l'ESP, ainsi que les fichiers (dans le dossier /data) à téléverser dans le système de fichiers de l'ESP32. 
* Le code de l'ESP génère un point d'accès qui sert la page Web du stationnement intelligent via un portail captif.

## data_parking 
* Ce dossier contient les images de stationnement pour l'entraînement de l'IA et les étiquettes correspondantes (vide, plein, logo).
* Sont aussi inclus les modèles résultants de l'entraînement qui permettent de détecter les étiquettes voulues.

## page_web
* Ce dossier contient les fichiers de code pour la génération de la page Web affichant les places de stationnement.

## stl
* Ce dossier contient les fichiers 3D de la barrière.

## schema.drawio
* Ce fichier est un schéma bloc du fonctionnement du projet de stationnement intelligent (à ouvrir avec draw.io)
