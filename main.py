import pywhatkit
from datetime import datetime
import time
import cv2



def llamar():
    try:
        current_time = datetime.now()  
        seconds = time.time()+60
        date = datetime.fromtimestamp(seconds)
        hora_actual = current_time.strftime("%H:%M:%S")
        mensaje = f"ALERTA: ALGUIEN ENTRÓ A TU HABITACIÓN. Hora de detección: {hora_actual}"
        
        pywhatkit.sendwhatmsg("+5491130925820", 
                            mensaje,
                            date.hour, date.minute)
    except:
        print("Error al enviar el mensaje, vamos a reintentarlo")

def detectarMov():
    
    cap= cv2.VideoCapture("http://192.168.0.243:4747/video") #Aca indicamos que tenemos que usar nuestra camara principal

    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    while cap.isOpened():
        gray1= cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2= cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        diff= cv2.absdiff(gray1, gray2) #Calculamos la diferencia entre el frame 1 y frame 2 (Será un bucle infinito)
        _, thresh = cv2.threshold(diff, 25,255, cv2.THRESH_BINARY)
        dilated= cv2.dilate(thresh, None, iterations=3)
        contours= cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours: 
            if cv2.contourArea(contour) < 500:
                continue
            x,y,w,h = cv2.boundingRect(contour)
            cv2.rectangle(frame1, (x,y), (x+w, y+h), (0,255,0), 2) 
        
        cv2.imshow("Detección de movimiento", frame1)
        frame1=frame2
        ret, frame2= cap.read()

        if cv2.waitKey(10) & 0xFF == ord('q'): 
            break
        cap.release()
        cv2.destroyAllWindows()

def main():
    detectarMov()
    
    

# Punto de entrada del programa
if __name__ == "__main__":
    main()