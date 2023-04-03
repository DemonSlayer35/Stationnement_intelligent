## Installer le board ESP32 dans l’IDE Arduino. (https://randomnerdtutorials.com/installing-the-esp32-board-in-arduino-ide-windows-instructions/)
1.	Dans l'IDE Arduino (pas 2.0), aller dans Fichier> Préférences

![image](https://user-images.githubusercontent.com/89463240/228365218-8526f81f-c23b-4dda-a570-b5eb5e57da7c.png)

 
2.	Entrer l'adresse suivante dans le champ “URL de gestionnaire de cartes supplémentaires” :
https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
Puis, cliquer sur le bouton “OK”:

 ![image](https://user-images.githubusercontent.com/89463240/228366378-ed489a3a-9a9a-40d8-a1a9-e98153258acf.png)
 
3.	Ouvrir le Gestionnaire de carte. Aller dans Outils > Type de carte > Gestionnaire de carte

 ![image](https://user-images.githubusercontent.com/89463240/228366440-efc16bad-bf68-4de1-941f-8936bcfccf1f.png)

4.	Chercher ESP32 et appuyer sur le bouton Installer de “esp32 by Espressif Systems“:

 ![image](https://user-images.githubusercontent.com/89463240/228366484-715ab89d-7758-4ec4-a002-9ca02955c95c.png)

 
## Installer ESP32 Filesystem Uploader dans l’IDE Arduino (https://randomnerdtutorials.com/install-esp32-filesystem-uploader-arduino-ide/)

1) Aller à l'adresse suivante https://github.com/me-no-dev/arduino-esp32fs-plugin/releases/ et télécharger le dossier compressé ESP32FS-1.0.zip

 ![image](https://user-images.githubusercontent.com/89463240/228367129-3a848fa5-9a1c-4664-ad9b-d5b9c5790841.png)
 
2) Trouver le dossier des croquis. Dans l'IDE Arduino, aller dans Fichier > Préférences et afficher le dossier des croquis.
Par exemple, le chemin peut ressembler à cela: C:\Users\user\Documents\Arduino.

 ![image](https://user-images.githubusercontent.com/89463240/228367172-ee0d1585-5164-49ee-b805-59dfabe1f69e.png)
 
3) Aller dans le dossier des croquis et créer un dossier tools.

 ![image](https://user-images.githubusercontent.com/89463240/228367262-c871d724-9a2f-4f6e-96ee-26b7b8632233.png)
 
4) Décompresser le dossier .zip. Ouvrez-le et copiez le dossier ESP32FS dans le dossier tools précédemment créé.
La structure de fichier devrait ressembler à: <Dossier-des-croquis>/tools/ESP32FS/tool/esp32fs.jar
  
 ![image](https://user-images.githubusercontent.com/89463240/228367647-3e1a9e7e-64cd-46e6-afd6-314ddc10b835.png)
 
5) Finalement, redémarrer (rouvrir) l'IDE Arduino. Pour vérifier si le plugin a été installé correctement, ouvrir l'IDE Arduino.
Sélectionner votre board ESP32, aller dans Outils et vérifier que vous avez l'option “ESP32 Sketch Data Upload“.
  
 ![image](https://user-images.githubusercontent.com/89463240/228367741-ed689fbd-0fcd-4f06-aa3e-e6abb9479fc4.png)

Pour le MQTT, il faut installer la libraire PubSubClient via Outils > Gérer les bibliothèques

 ![image](https://user-images.githubusercontent.com/89463240/228368532-a11e78ec-05fb-4dc7-8f83-ec50c57eb2cf.png)
  
## Installer la librairie ESPAsyncWebServer
 
1) Cliquer sur ce lien https://github.com/me-no-dev/ESPAsyncWebServer/archive/master.zip pour télécharger la librairie.
 
2) Décompresser le dossier .zip. Vous devriez obtenir un dossier ESPAsyncWebServer-master.
 
3) Renommer le dossier ESPAsyncWebServer-master en ESPAsyncWebServer.
 
4) Déplacer le dossier ESPAsyncWebServer vers votre dossier de libraires pour l'IDE Arduino.
Par exemple, le chemin peut ressembler à cela: C:\Users\user\Documents\Arduino\libraries.
 
![image](https://user-images.githubusercontent.com/89463240/229601575-35975a78-fbc0-4346-9110-a2d85399cbdd.png)
 
## Installer la librairie Async TCP
 
1) Cliquer sur ce lien https://github.com/me-no-dev/AsyncTCP/archive/master.zip pour télécharger la librairie.
 
2) Décompresser le dossier .zip. Vous devriez obtenir un dossier AsyncTCP-master.
 
3) Renommer le dossier AsyncTCP-master en AsyncTCP.
 
4) Déplacer le dossier AsyncTCP vers votre dossier de libraires pour l'IDE Arduino.
Par exemple, le chemin peut ressembler à cela: C:\Users\user\Documents\Arduino\libraries.
 
![image](https://user-images.githubusercontent.com/89463240/229600926-301b9736-afe6-4281-a08d-d4d12bfa896c.png)
