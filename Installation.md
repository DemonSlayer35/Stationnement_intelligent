# Étapes d'installation de YOLOv5 sur Windows avec une carte graphique NVIDIA
1. Télécharger le fichier zip du répertoire de YOLOv5 à l'adresse https://github.com/ultralytics/yolov5
   ou cloner le répertoire GitHub (si vous avez Git installé sur votre PC) de YOLOv5 depuis une invite de commandes avec la commande :
   
    git clone https://github.com/ultralytics/yolov5

2. Installer une version de Python entre 3.7 et 4.0, comme Python 3.9.7 depuis le site de Python :
    https://www.python.org/downloads/release/python-397/
    
    ![image](https://user-images.githubusercontent.com/89463240/217079449-70af889e-c3e6-4505-b3d2-19bc84895b93.png)

3. Si vous possédez une carte graphique NVIDIA, installer le logiciel Cuda depuis le site de NVIDIA :
    https://developer.nvidia.com/cuda-downloads
    
    ![image](https://user-images.githubusercontent.com/89463240/217079597-6bcd7655-b31d-4ead-a6c1-4c4a29a4c6a1.png)

4. Aller sur le site de PyTorch à l'adresse https://pytorch.org/get-started/locally/

5. Sélectionner les options correspondantes (Stable, Windows, Pip, Python, Cuda 11.7) et copier la commande proposée par PyTorch.

![image](https://user-images.githubusercontent.com/89463240/217079681-8a33c8fa-c6b1-4c1f-9a3d-0e703fdc3f5f.png)

6. Dans l'explorateur de fichiers, trouver le dossier Scripts de Python. Dans mon cas, le fichier se trouve à l'adresse : 
    C:\Users\user\AppData\Local\Programs\Python\Python39\Scripts
    
7. Taper cmd dans la barre d'adresse de l'explorateur de fichiers pour ouvrir l'invite de commandes.
 
![image](https://user-images.githubusercontent.com/89463240/217079938-9d8a3e13-f8e2-457d-8051-8f35c506dedf.png)

8. Coller la commande de PyTorch dans la console.

9. Ouvrir le dossier YOLOv5 et taper cmd dans la barre d'adresse de l'explorateur de fichiers pour ouvrir l'invite de commandes.

10. Installer les requis de YOLOv5 en tapant la commande :
      ```pip install -r requirements.txt```
      
11. Vérifier la fonctionnalité de l'installation en tapant la commande : 
      ```python detect.py --source 0```
      (Cette commande doit être utilisée à partir du dossier de YOLOv5, car c'est là que le fichier detect.py se trouve.)
      (Cette commande va utiliser la webcam pour détecter les objets avec un script déjà fait.)
      
# Création d'un dataset pour l'entraînement de l'intelligence artificielle
1. Installer un logiciel qui permet d'étiqueter des images comme LabelImg avec la commande (depuis une invite de commandes) : 
      ```pip install labelImg```
      (Il faut identifier manuellement avec des étiquettes les objets qu'on veut détecter dans les images choisies. C'est
      là l'utilité d'un logiciel comme LabelImg qui permet de rapidement tracer des rectangles sur des images et qui fournit
      un format de sortie compatible avec YOLOv5.)
      
2. Créer un dossier pour le dataset. Dans ce dossier, créer un dossier pour les images et un autre pour les étiquettes.

![image](https://user-images.githubusercontent.com/89463240/217083315-a7eb631a-94e3-46ff-b341-b584e103f759.png)

3. Ouvrir LabelImg depuis un terminal avec la commande labelimg

4. Dans la barre latérale à gauche, sélectionner le format Yolo. Vous pouvez ouvrir votre dossier d'images avec Open Dir
   et changer le dossier d'enregistrement des étiquettes avec Change Save Dir.

![image](https://user-images.githubusercontent.com/89463240/217080357-236bfc18-899d-40ae-920c-2924421705e5.png)

5. Vous pouvez tracer des rectangles autour des objets dans l'image et assigner une étiquette à chaque rectangle.

![image](https://user-images.githubusercontent.com/89463240/217081390-8417ba8f-8f6f-4fc5-9623-ec851b5d6666.png)

6. Enregistrer vos changements avec le bouton Save.

# Entraînement de l'intelligence artificielle
1. Copier le dossier hyps des hyperparamètres (yolov5\data\hyps) et le coller dans le dossier du dataset.

2. Créer un fichier yml pour le dataset dans le répertoire yolov5

3. Dans le fichier yml, spécifier le chemin des images, le nombre de classes et le nom des classes.
(Les classes correspondent aux étiquettes.)

![image](https://user-images.githubusercontent.com/89463240/217090070-ecd2543e-f5da-4cbd-bb6c-4416c26e8cac.png)

(Dans cette image, le dossier du dataset est nommé data_vache et il est situé dans le répertoire yolov5 sur le PC.)

4. Vous pouvez modifier les hyperparamètres à partir du fichier hyp.scatch.yaml (Ce sont des paramètres qui permettent
   d'améliorer l'entraînement comme la rotation ou la translation des images.)

5. Ouvrir cmd à partir du dossier yolov5 et entraîner l'intelligence en tapant la commande :

```python train.py --img 320 --batch 16 --epochs 50 --data dataset_vache.yml --weights yolov5s.pt --workers 4 --hyp data_vache\hyps\hyp.scratch.yaml```

* img définit la résolution des images 
* batch définit le nombre d'images par section d'entraînement
* epochs définit le nombre de fois que toutes les images passent à travers le réseau de neurones
* data pointe vers le fichier yml à utiliser
* weights définit le modèle à utiliser pour l'entraînement
* workers définit le nombre de coeurs CPU à utiliser
* hyp pointe vers le fichier des hyperparamètres

6. À la fin de l'entraînement, la console affichera le dossier où les résultats ont été enregistrés. En général, c'est
   quelque chose du genre yolov5/runs/train/exp
   
# Test de détection (validation) avec un modèle personnalisé
1. Ouvrir cmd à partir du dossier yolov5 et démarrer la détection en tapant la commande :

```python detect.py --weights runs/train/exp/weights/best.pt --img 320 --conf 0.25 --source data_vache/images/```

(Dans weigths, spécifier le chemin du modèle entraîné.
Dans conf, spécifier le seuil de confiance entre 0 et 1 de l'intelligence pour la détection)

2. Dans la console sera affichée le dossier des résultats. En général, c'est quelque chose du genre
   yolov5/runs/detect/exp
