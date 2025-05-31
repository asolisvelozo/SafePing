import pywhatkit
from datetime import datetime
import time
import cv2
import numpy as np

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
    video = cv2.VideoCapture("http://192.168.0.101:4747/video")
    i = 0
    while True:
        ret, frame = video.read()
        if ret == False: break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if i == 20:
            bgGray = gray
        if i >= 20:
            dif = cv2.absdiff(gray, bgGray)
            th = cv2.threshold(dif, 40, 255, cv2.THRESH_BINARY)[1]
            cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            #cv2.drawContours(frame, cnts, -1, (0,255,0),2)
            #cv2.imshow('th', th)
            for c in cnts:
                area = cv2.contourArea(c)
                if area > 9000:
                    x,y,w,h = cv2.boundingRect(c)
                    cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0),2)
                    llamar()
                    time.sleep(30)
            cv2.imshow('th', th)

        cv2.imshow('Frame',frame)

        i = i+1
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break
    video.release()

def main():
    detectarMov()
    
    

# Punto de entrada del programa
if __name__ == "__main__":
    main()
    main()
