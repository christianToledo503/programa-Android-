import cv2
import numpy as np
from pyzbar.pyzbar import decode

# Cambia el índice de la cámara si es necesario
cap = cv2.VideoCapture(0)

# Ancho de la cámara
cap.set(3, 640)
cap.set(4, 480)

# Leer credenciales.txt
with open('credenciales.txt') as f:
    # Lee y separa en un arreglo los datos 
    mydatalist = f.read().splitlines()

# Mientras el bucle 
while True:
    success, img = cap.read()

    if not success:
        print("Error: No se pudo leer el fotograma.")
        break

    # Verifica si la decodificación fue exitosa
    decoded_objects = decode(img)
    
    for barcode in decoded_objects:
        mydata = barcode.data.decode('utf-8')
        print(mydata)

        if mydata in mydatalist:
            myoutput = 'listo'
            color = (0, 255, 0)
        else: 
            myoutput = 'No esta'
            color = (0, 0, 255)

        # Coordenada del barcode    
        pts = np.array([barcode.polygon], np.int32)
        pts = pts.reshape((-1, 1, 2))
        
        cv2.polylines(img, [pts], True, color, 5)  # Dibuja el polígono

        # Muestra el resultado en la esquina superior izquierda
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, myoutput, (10, 30), font, 1, color, 2, cv2.LINE_AA)
        
         # se arma un segundo rectangulo
        #pts2= barcode.rect 
        #cv2.putText(img, # fuente
        #            myoutput,
        #            (pts2[0],pts2[1]),
        #            cv2.FONT_HERSHEY_SIMPLEX,
        #            0.9, #tamaño de la letra
        #            color, # color de la letra
         #           3)# espesor de la letra
    cv2.imshow('Result', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()

print(mydatalist)
