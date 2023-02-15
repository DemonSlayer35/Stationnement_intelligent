# Procédure pour faire rouler la page Web contenant le schéma du stationnement accessible à tous

1. Télécharger NGINX à partir du site officiel : https://nginx.org/en/download.html, puis décompresser le dossier.

2. Récupérer les fichiers app.py, page_web.html, script.js et camera.py.

3. Créer un dossier js (pour les fichiers JavaScript) dans le répertoire de NGINX et y déposer script.js :
![image](https://user-images.githubusercontent.com/89463240/218909744-715d9c85-c67a-40bb-b4e8-0f75b28a148b.png)

4. Placer le fichier page_web.html dans le dossier html de NGINX.

5. Ouvrir le fichier nginx.conf (configuration de NGINX) situé dans le dossier conf de NGINX :
![image](https://user-images.githubusercontent.com/89463240/218909025-491fdb17-2edd-4e4a-b218-e89fd8c54dd2.png)

6. Dans la section non-commentée qui commence par server{listen 80;, ajouter un bloc pour la location du dossier JavaScript comme suit :
![image](https://user-images.githubusercontent.com/89463240/218909527-c1ef1d6e-9860-4eb6-ac28-eef17fd967b4.png)
(Mettre le chemin correspondant en conséquence.)

7. Enregistrer le fichier et fermer nginx.conf (Notez qu'il faut repartir nginx.exe à chaque modification.)

8. Modifier le fichier script.js en entrant l'adresse IP de l'hôte dans la fonction getListe() :
* ```// Fonction pour récupérer la liste depuis l'API REST
     async function getListe() {
     const response = await fetch('http://10.0.0.98:5000/moyenne'); //mettre l'adresse du serveur flask
     const data = await response.json();
     liste = JSON.parse(data);```
     
9. Enregistrer le fichier et repartir nginx.exe

10. Assurez-vous que la bonne caméra est utilisée dans le fichier camera.py 
  - ```cap = cv2.VideoCapture(0)  # 0 = Webcam intégrée ; 1 = Caméra USB```

11. Démarrer NGINX en double-cliquant sur nginx.exe (C'est normal si rien ne s'affiche.)
  - Si vous voulez être sûr que NGINX fonctionne, aller à l'adresse localhost et vous devriez voir la page index.html suivante :
![image](https://user-images.githubusercontent.com/89463240/218911227-9a593f26-bed6-46c0-88f8-f0511b6e5e75.png)

12. Exécuter le fichier 🍎app.py avec ```py app.py``` dans une console cmd par exemple (Il est préférable d'ouvrir tous les fichiers avec VS Code.)
  - Cela va créer une API web qui contient l'état des emplacements de stationnement dans une liste.

13. Exécuter le fichier 📷camera.py avec ```py camera.py```.
  - Cela va démarrer la détection des emplacements de stationnement. Après chaque cycle de 20 frames, la liste est mise à jour sur l'API web située
  à localhost:5000/moyenne (Les autres usagers aussi peuvent accéder à la liste à [l'adresse IP de l'hôte]:5000/moyenne).

14. Accéder au 🕸️site Web à [l'adresse IP de l'hôte]/page_web.html
