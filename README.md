# Stationnement intelligent
Projet de fin de DEC en TSO (Etienne Dubé et Mohammad Barin Wahidi)

# Étapes d'installation de YOLOv5 sur Windows avec une carte graphique NVIDIA

1. Télécharger le fichier zip du répertoire de YOLOv5 à l'adresse https://github.com/ultralytics/yolov5
                          ou
   Cloner le répertoire GitHub de YOLOv5 depuis une invite de commandes avec la commande :
    git clone https://github.com/ultralytics/yolov5

2. Installer une version de Python entre 3.7 et 4.0, comme Python 3.9.7 depuis le site de Python :
    https://www.python.org/downloads/release/python-397/

3. Si vous possédez une carte graphique NVIDIA, installer le logiciel Cuda depuis le site de NVIDIA :
    https://developer.nvidia.com/cuda-downloads
    
4. Aller sur le site de PyTorch à l'adresse https://pytorch.org/get-started/locally/

5. Sélectionner les options correspondantes (Stable, Windows, Pip, Python, Cuda 11.7) et copier la commande proposée par PyTorch.

6. Dans l'explorateur de fichiers, trouver le dossier Scripts de Python. Dans mon cas, le fichier se trouve à l'adresse : 
    C:\Users\user\AppData\Local\Programs\Python\Python39\Scripts
    
7. Taper cmd dans la barre d'adresse de l'explorateur de fichiers pour ouvrir l'invite de commandes.

8. Coller la commande de PyTorch dans la console.

9. Ouvrir le dossier YOLOv5 et taper cmd dans la barre d'adresse de l'explorateur de fichiers pour ouvrir l'invite de commandes.

10. Installer les requis de YOLOv5 en tapant la commande :
      pip install -r requirements.txt
      
11. Vérifier la fonctionnalité de l'installation en tapant la commande : 
      python detect.py --source 0
      (Cette commande doit être utilisée à partir du dossier de YOLOv5, car c'est là que le fichier detect.py se trouve.)
      (Cette commande va utiliser la webcam pour détecter les objets avec un script déjà fait.)
    
