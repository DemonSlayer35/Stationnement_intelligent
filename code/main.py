import threading
from ClassCamera import ParkingDetector

def detection(camera):
    parking = ParkingDetector(camera)
    parking.detect()

if __name__ == "__main__":
    camera1 = 1  # Remplacez cette valeur par la source de la première caméra
    camera2 = 2  # Remplacez cette valeur par la source de la deuxième caméra

    # Créez deux threads pour les deux sources de caméra
    stationnement1 = threading.Thread(target=detection, args=(camera1,))
    stationnement2 = threading.Thread(target=detection, args=(camera2,)) 

    # Démarrez les deux threads
    stationnement1.start()
    stationnement2.start()
    stationnement1.join()
    stationnement2.join()