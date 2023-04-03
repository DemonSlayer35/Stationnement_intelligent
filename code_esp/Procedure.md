# Procédure pour faire rouler l'ESP en mode point d'accès avec un portail captif affichant le schéma du stationnement

1. Récupérer le dossier code_esp.
2. Ouvrir le fichier code_esp.ino dans l'IDE Arduino.
3. Connecter l'ESP à l'ordinateur. Sélectionnner le type de carte (ex. : ESP32-WROOM-DA Module) et le port correspondant.
Assurez-vous aussi de rentrer les identifiants Wi-Fi correspondants ainsi que l'adresse du broker MQTT.

![image](https://user-images.githubusercontent.com/89463240/229603978-58d71221-2377-4d19-8865-b5e488f622d7.png)

4. Téléverser le code à l'intérieur de l'ESP. 
(Si la connexion ne fonctionne pas, il faut appuyer sur le bouton BOOT pendant une seconde environ lorsque la console affiche Connecting...)
5. Aller dans Outils > ESP32 Data Sketch Upload et attendre que les fichiers soient téléchargés dans la mémoire.

![image](https://user-images.githubusercontent.com/89463240/229604207-ad05dd2a-a6f8-4e10-89b3-223e964e955d.png)

6. Un point d'accès nommé Parking devrait apparaître dans la liste des réseaux disponibles. En vous y connectant, le schéma
du stationnment devrait apparaître après quelques secondes.

(Vous pouvez vérifier dans le moniteur série de l'IDE Arduino si tout est fonctionnel.)
