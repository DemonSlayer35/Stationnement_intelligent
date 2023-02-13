import cv2 # OpenCV
import numpy as np
import torch

model = torch.hub.load('C:/yolov5', 'custom', path='C:/yolov5/bestv5m.pt', source='local')
model.conf = 0.45  # Confiance minimale pour utilisation

cap = cv2.VideoCapture(1)  # 0 = Webcam intégrée ; 1 = Camera USB

values_x = [[41, 205], [66, 202], [92, 205], [102, 212], [113, 218], [124, 221], [131, 227], [142, 233], [146, 234], [303, 393], [310, 397], [312, 406], [314, 414], [313, 425], [320, 431], [319, 444], [324, 463], [325, 487]]
values_y = [[377, 480], [313, 406], [254, 339], [212, 284], [166, 232], [127, 193], [95, 150], [66, 117], [38, 83], [29, 84], [62, 113], [88, 148], [121, 187], [166, 221], [201, 285], [256, 321], [298, 393], [367, 471]]

moyenne = [0] * 18

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    j = 0
    while(j < 20):

        results = model(frame)
        liste = results.xyxy[0].tolist()

        for i, x in enumerate(liste):
            x1, y1, x2, y2 = [int(x) for x in x[:4]]
            
            emplacement = [(x1 + x2) / 2, (y1 + y2) / 2]

            for i in range(len(values_x)):
                if values_x[i][0] <= emplacement[0] <= values_x[i][1] and values_y[i][0] <= emplacement[1] <= values_y[i][1]:
                    moyenne[i] += x[5]

        j += 1

    frame = np.array(frame)
    for i in range(len(values_x)):
        moyenne[i] /= 20
        color = (255, 0, 0) if moyenne[i] <= 0.5 else (0, 255, 0)
        cv2.rectangle(frame, (values_x[i][0], values_y[i][0]), (values_x[i][1], values_y[i][1]), color, 2)
        if moyenne[i] > 0.5:
            print("La voiture se trouve dans le parking", i+1)

    print(moyenne)
    cv2.imshow("Détection d'objets", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    if cv2.waitKey(1) == 27:  # 27 est la valeur de la touche "Esc"
        break

cap.release()
cv2.destroyAllWindows()