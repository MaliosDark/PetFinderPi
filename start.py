# pip install RPi.GPIO
# pip install picamera
# pip install requests
# pip install pyserial
# pip install tensorflow
# pip install Adafruit_DHT


#start.py

from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import picamera
import requests
import serial
import tensorflow as tf
import numpy as np
import os
from reinforcement_learning import ReinforcementLearningModel  
from animal_functions import predict_animal, encode_animal, get_time_of_day

# Configuración de pines GPIO
GPIO.setmode(GPIO.BOARD)
PIR_PIN = 11
GPIO.setup(PIR_PIN, GPIO.IN)

# Configuración de la cámara
camera = picamera.PiCamera()

# Configuración del escáner RFID
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

# Configuración del modelo de clasificación de animales
model = MobileNetV2(weights='imagenet')

# Configuración del sensor de temperatura DHT
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4  # Ajusta el pin GPIO al que está conectado el sensor

# Historial de eventos
event_history = []

# URL del servidor para enviar datos
server_url = "http://tu-servidor.com/guardar-datos"
image_folder = "images"

def save_event_history():
    with open("logs/event_history.txt", "a") as file:
        for event in event_history:
            file.write(f"{event['timestamp']} - {event['evento']}\n")

# Crear una instancia del modelo de aprendizaje por refuerzo
rl_model = ReinforcementLearningModel(input_size=4)  # Ajusta el tamaño según tus características de entrada

try:
    while True:
        try:
            if GPIO.input(PIR_PIN):
                # Registro de evento: Detección de movimiento
                event_history.append({"timestamp": time.strftime("%Y%m%d%H%M%S"), "evento": "Detección de movimiento"})

                # Al detectar movimiento, capturar imagen
                timestamp = time.strftime("%Y%m%d%H%M%S")
                image_path = f"{image_folder}{timestamp}.jpg"
                camera.capture(image_path)

                # Leer el RFID
                rfid_data = ser.readline().decode('utf-8').strip()
                # Enviar el RFID al servidor para verificar
                response = requests.post(server_url + '/verify_rfid', data={'rfid_data': rfid_data})

                if response.status_code == 200:
                    print("RFID verificado exitosamente en el servidor")
                else:
                    print(f"Error al verificar RFID en el servidor: {response.status_code}")


                # Identificar el tipo de animal
                animal_class, confidence = predict_animal(model, image_path)

                # Obtener temperatura
                humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

                # Registro de evento: Identificación de animal
                event_history.append({"timestamp": time.strftime("%Y%m%d%H%M%S"), "evento": f"Identificación de {animal_class}"})

                # Registro de evento: Detección de temperatura
                event_history.append({"timestamp": time.strftime("%Y%m%d%H%M%S"), "evento": f"Detección de temperatura: {temperature}°C"})

                # Enviar datos al servidor
                payload = {"animal": animal_class, "imagen": image_path, "rfid": rfid_data, "confidence": confidence, "temperatura": temperature}
                response = requests.post(server_url, data=payload)

                # Registro de evento: Envío de datos al servidor
                event_history.append({"timestamp": time.strftime("%Y%m%d%H%M%S"), "evento": "Envío de datos al servidor"})

                print("Datos enviados al servidor")


                # Eliminar la imagen después de enviar los datos
                os.remove(image_path)
                print(f"Imagen {image_path} eliminada")

                time.sleep(10)  # Esperar 10 segundos antes de la siguiente detección

                # Obtener características para el modelo de aprendizaje por refuerzo
                animal_encoded = encode_animal(animal_class)
                time_of_day = get_time_of_day()
                features = np.array([[confidence, temperature, animal_encoded[0][0], time_of_day]])

                # Realizar predicción con el modelo de aprendizaje por refuerzo
                prediction = rl_model.predict(features.reshape(1, -1))

                # Actualizar el modelo de aprendizaje por refuerzo según sea necesario
                target = 0.9  # Ajusta según tus necesidades
                rl_model.update(features.reshape(1, -1), target)

                # Registro de evento: Predicción de ubicación
                event_history.append({"timestamp": time.strftime("%Y%m%d%H%M%S"), "evento": f"Predicción de ubicación: {prediction}"})

        except Exception as e:
            print(f"Error: {e}")

except KeyboardInterrupt:
    GPIO.cleanup()
    save_event_history()