
#start.py


# pip install RPi.GPIO
# pip install picamera
# pip install requests
# pip install pyserial
# pip install numpy
# pip install Adafruit_DHT
# sudo apt-get install libopenblas-base



import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import requests
import serial
import base64
import json
import logging
import numpy as np
from reinforcement_learning import ReinforcementLearningModel 


# Configuración de pines GPIO
GPIO.setmode(GPIO.BOARD)
PIR_PIN = 11
GPIO.setup(PIR_PIN, GPIO.IN)

# Configuración del escáner RFID
##ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

# Configuración del sensor de temperatura DHT
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4  # Ajusta el pin GPIO al que está conectado el sensor

# URL del servidor para enviar datos
server_url = "http://192.168.68.16:5000/verify_rfid"

# Historial de eventos
event_history = []

# Configuración del registro
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Crea una instancia del modelo de aprendizaje por refuerzo
rl_model = ReinforcementLearningModel(input_size=4)

# Ajustes dinámicos
tiempo_espera = 1  # Tiempo de espera inicial entre detecciones
umbral_temperatura_alta = 30.0  # Umbral de temperatura inicial para considerarla como "alta"

def cleanup_resources():
    global umbral_temperatura_alta  
    global tiempo_espera  
    """
    Función para liberar los recursos GPIO al finalizar o interrumpir el programa.
    """
    GPIO.cleanup()
    save_event_history()
    rl_model.save_model()


def get_public_ip():
    try:
        # Utiliza api.ipify.org para obtener la IP pública
        response = requests.get('https://api.ipify.org?format=json')
        public_ip = response.json().get('ip', 'Desconocido')
        return public_ip
    except Exception as e:
        print(f"Error al obtener la IP pública: {e}")
        return 'Desconocido'


def save_event_history():
    with open("logs/event_history.txt", "a") as file:
        for event in event_history:
            file.write(f"{event['timestamp']} - {event['evento']}\n")

# Ajustes dinámicos
tiempo_espera = 1  # Tiempo de espera inicial entre detecciones
umbral_temperatura_alta = 30.0  # Umbral de temperatura inicial para considerarla como "alta"
umbral_temperatura_alta_local = umbral_temperatura_alta  # Mover esta línea aquí

try:
    while True:
        try:
            tiempo_espera_local = tiempo_espera
            
            if GPIO.input(PIR_PIN):
                # Registro de evento: Detección de movimiento
                event_history.append({"timestamp": time.strftime("%Y%m%d%H%M%S"), "evento": "Detección de movimiento"})
                print("Detección de movimiento")

                # Obtener la IP pública
                public_ip = get_public_ip()

                # Leer el RFID
                ##rfid_data = ser.readline().decode('utf-8').strip()

                # Obtener temperatura
                humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

                # Verificar si la lectura del sensor de temperatura fue exitosa
                if humidity is not None and temperature is not None:
                    # Ajustes dinámicos
                    motion_detected = True  # Puedes ajustar esto dependiendo de cómo detectes el movimiento
                    rl_model.adjust_dynamic_settings(temperature, motion_detected)

                    print(f"Tiempo de espera ajustado a {tiempo_espera} segundos")
                    time.sleep(tiempo_espera)  # Esperar el tiempo ajustado antes de la siguiente detección

                    print(f"Tiempo de espera ajustado a {tiempo_espera} segundos")
                    time.sleep(tiempo_espera)  # Esperar el tiempo ajustado antes de la siguiente detección

                    # Realizar el resto de las operaciones solo si la lectura fue exitosa
                    features = np.array([0.0, 0.0, 0.0, 0.0])  # Ajusta según tus características
                    prediction = rl_model.predict(features)

                    # Actualizar el modelo de aprendizaje por refuerzo
                    target = 0.9  # Ajusta según tus necesidades
                    rl_model.update(features, target)

                    # Enviar datos al servidor
                    payload = {
                        ##"rfid": rfid_data,
                        "temperature": temperature,
                        "prediction": prediction,
                        "public_ip": public_ip,
                        "humidity": humidity,
                    }
                    response = requests.post(server_url, json=payload)

                    # Registro de evento: Envío de datos al servidor
                    event_history.append({"timestamp": time.strftime("%Y%m%d%H%M%S"), "evento": "Envío de datos al servidor"})

                    print("Datos enviados al servidor")

                    # Ajustes dinámicos
                    if temperature > umbral_temperatura_alta:
                        tiempo_espera = max(tiempo_espera - 1, 1)  # Reducir el tiempo de espera si la temperatura es alta
                    else:
                        tiempo_espera = min(tiempo_espera + 1, 30)  # Aumentar el tiempo de espera si la temperatura es normal

                    print(f"Tiempo de espera ajustado a {tiempo_espera} segundos")
                    print(f"Tiempo de espera ajustado a {tiempo_espera_local} segundos")  # Utiliza la variable local
                    time.sleep(tiempo_espera_local)  # Utiliza la variable local antes de la siguiente detección
                else:
                    # Si la lectura del sensor de temperatura no fue exitosa, puedes manejarlo de alguna manera
                    logger.error("Error al leer el sensor de temperatura")
                    tiempo_espera = tiempo_espera_local

                time.sleep(tiempo_espera)  # Esperar el tiempo ajustado antes de la siguiente detección
                
        except Exception as e:
            logger.error(f"Error: {e}")

except KeyboardInterrupt:
    GPIO.cleanup()
    cleanup_resources()
    save_event_history()