import pywhatkit
from datetime import datetime
import time
import cv2
import numpy as np
import threading

CAMERA_URL = "http://192.168.0.254:4747/video"
COOLDOWN_SECONDS = 30
MIN_CONTOUR_AREA = 9000
BACKGROUND_CAPTURE_FRAME = 20
PHONE_NUMBER = "+5491130925820"

enviando_mensaje = False
cooldown = False

def enviar_whatsapp(frame):
    global enviando_mensaje
    enviando_mensaje = True
    cv2.imwrite("screenshot.jpg", frame)
    try:
        hora_actual = datetime.now().strftime("%H:%M:%S")
        mensaje = f"⚠️ ALERTA: ALGUIEN ENTRÓ A TU HABITACIÓN. Hora: {hora_actual}"
        print("🟡 Enviando WhatsApp...")
        pywhatkit.sendwhatmsg_instantly(PHONE_NUMBER, mensaje, wait_time=15)
        print("✅ Mensaje enviado.")
    except Exception as e:
        print("❌ Error al enviar el mensaje:", e)
    finally:
        enviando_mensaje = False

def detectarMov():
    global cooldown

    video = cv2.VideoCapture(CAMERA_URL)
    if not video.isOpened():
        print("❌ No se pudo conectar con la cámara.")
        return

    i = 0
    bgGray = None
    th = None
    print("🎥 Cámara conectada. Detectando movimiento...")

    tiempo_ultimo_envio = 0

    while True:
        ret, frame = video.read()
        if not ret:
            print("⚠️ No se pudo leer el frame.")
            time.sleep(1)
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if i == BACKGROUND_CAPTURE_FRAME:
            bgGray = gray
            print("✅ Fondo capturado.")

        if i > BACKGROUND_CAPTURE_FRAME and bgGray is not None and not enviando_mensaje:
            dif = cv2.absdiff(gray, bgGray)
            th = cv2.threshold(dif, 40, 255, cv2.THRESH_BINARY)[1]
            th = cv2.dilate(th, None, iterations=2)
            cnts, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for c in cnts:
                if cv2.contourArea(c) > MIN_CONTOUR_AREA and time.time() - tiempo_ultimo_envio > COOLDOWN_SECONDS:
                    x, y, w, h = cv2.boundingRect(c)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    print("🚨 Movimiento detectado. Enviando WhatsApp...")
                    hilo = threading.Thread(target=enviar_whatsapp, args=(frame.copy(),))
                    hilo.daemon = True
                    hilo.start()

                    tiempo_ultimo_envio = time.time()
                    bgGray = None  # Reiniciar fondo
                    i = 0           # Volver a contar para capturar nuevo fondo
                    break

        cv2.imshow("Video", frame)
        if th is not None:
            cv2.imshow("Movimiento", th)

        key = cv2.waitKey(30) & 0xFF
        if key == ord('q'):
            break

        i += 1

    video.release()
    cv2.destroyAllWindows()

def main():
    detectarMov()

if __name__ == "__main__":
    main()
