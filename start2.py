#start.py

import cv2
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import requests
import serial
import numpy as np
import os
from animal_functions import predict_animal, encode_animal, get_time_of_day
from reinforcement_learning import ReinforcementLearningModel  # Importa la clase

# Configuración de pines GPIO
GPIO.setmode(GPIO.BOARD)
PIR_PIN = 11
GPIO.setup(PIR_PIN, GPIO.IN)

# Configuración de la cámara
camera = cv2.VideoCapture(0)
camera.set(3, 640)  # Ancho
camera.set(4, 480)  # Alto

# Configuración del escáner RFID
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

# Configuración del sensor de temperatura DHT
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4  # Ajusta el pin GPIO al que está conectado el sensor

# URL del servidor para enviar datos
server_url = "http://tu-servidor.com/guardar-datos"
image_folder = "images"

# Historial de eventos
event_history = []

# Crea una instancia del modelo de aprendizaje por refuerzo
rl_model = ReinforcementLearningModel(input_size=4)  # Ajusta el tamaño según tus características de entrada

def save_event_history():
    with open("logs/event_history.txt", "a") as file:
        for event in event_history:
            file.write(f"{event['timestamp']} - {event['evento']}\n")

try:
    while True:
        try:
            if GPIO.input(PIR_PIN):
                # Registro de evento: Detección de movimiento
                event_history.append({"timestamp": time.strftime("%Y%m%d%H%M%S"), "evento": "Detección de movimiento"})

                # Al detectar movimiento, capturar imagen
                ret, frame = camera.read()
                timestamp = time.strftime("%Y%m%d%H%M%S")
                image_path = f"{image_folder}{timestamp}.jpg"
                cv2.imwrite(image_path, frame)

                # Leer el RFID
                rfid_data = ser.readline().decode('utf-8').strip()

                # Identificar el tipo de animal
                animal_class, confidence = predict_animal(frame)  # Ajusta según tu función predict_animal

                # Obtener temperatura
                humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

                # Realizar predicción con el modelo de aprendizaje por refuerzo
                features = np.array([confidence, temperature, encode_animal(animal_class)[0][0], get_time_of_day()[0][0]])
                prediction = rl_model.predict(features)

                # Actualizar el modelo de aprendizaje por refuerzo
                target = 0.9  # Ajusta según tus necesidades
                rl_model.update(features, target)

                # Envía solo la imagen al servidor
                files = {'file': open(image_path, 'rb')}
                payload = {"animal": animal_class, "rfid": rfid_data, "confidence": confidence, "temperatura": temperature}
                response = requests.post(server_url, files=files, data=payload)

                # Registro de evento: Envío de datos al servidor
                event_history.append({"timestamp": time.strftime("%Y%m%d%H%M%S"), "evento": "Envío de datos al servidor"})

                print("Datos enviados al servidor")

                # Eliminar la imagen después de enviar los datos
                os.remove(image_path)
                print(f"Imagen {image_path} eliminada")

                time.sleep(10)  # Esperar 10 segundos antes de la siguiente detección

        except Exception as e:
            print(f"Error: {e}")

except KeyboardInterrupt:
    GPIO.cleanup()
    save_event_history()
    camera.release()
