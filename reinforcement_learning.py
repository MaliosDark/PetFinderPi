# reinforcement_learning.py
# Autor: Andryu Schittone
# Descripción: Implementación de un modelo de aprendizaje por refuerzo para el sistema PetFinderPi.
# Licencia: GPL3
# Versión: 1.0

import numpy as np
import os
import json
import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import requests
import serial



class ReinforcementLearningModel:
    def __init__(self, input_size):
        self.weights = np.zeros(input_size)
        self.learning_rate = 0.1  # Tasa de aprendizaje inicial
        self.model_folder = "models"
        self.model_path = os.path.join(self.model_folder, "rl_model.json")
        self.event_history = []

        # Cargar el modelo previo si existe
        self.load_model()

    def predict(self, state):
        return np.dot(state, self.weights)

    def update(self, state, target):
        """
        Actualiza el modelo de aprendizaje por refuerzo.
        """
        prediction = self.predict(state)
        error = target - prediction
        self.weights += self.learning_rate * error * state

        # Ajustar la tasa de aprendizaje automáticamente
        if abs(error) > 0.2:
            self.learning_rate *= 0.9  # Reducir la tasa de aprendizaje si el error es grande
        else:
            self.learning_rate *= 1.1  # Aumentar la tasa de aprendizaje si el error es pequeño

        # Guardar el modelo actualizado automáticamente
        self.save_model()

    def save_model(self):
        """
        Guarda el modelo en un archivo.
        """
        try:
            model_data = {"weights": self.weights.tolist(), "learning_rate": self.learning_rate}
            os.makedirs(self.model_folder, exist_ok=True)
            with open(self.model_path, "w") as file:
                json.dump(model_data, file, indent=2)
            print(f"Modelo guardado en: {self.model_path}")
        except Exception as e:
            print(f"Error al guardar el modelo: {e}")

    def load_model(self):
        """
        Carga el modelo desde un archivo si existe.
        """
        try:
            if os.path.exists(self.model_path):
                with open(self.model_path, "r") as file:
                    data = json.load(file)
                    self.weights = np.array(data["weights"])
                    self.learning_rate = data["learning_rate"]
                    print(f"Modelo cargado desde: {self.model_path}")
        except Exception as e:
            print(f"Error al cargar el modelo: {e}")

    def read_sensor(self, sensor, pin):
        """
        Lee los datos del sensor y maneja posibles fallos de lectura.
        """
        try:
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            return humidity, temperature
        except Exception as e:
            print(f"Error al leer el sensor {sensor}: {e}")
            return None, None

    def main_loop(self, PIR_PIN, DHT_SENSOR, server_url, tiempo_espera, umbral_temperatura_alta):
        """
        Bucle principal del programa.
        """
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(PIR_PIN, GPIO.IN)

        # Configuración del escáner RFID
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

        while True:
            try:
                if GPIO.input(PIR_PIN):
                    self.handle_motion_detection(PIR_PIN, DHT_SENSOR, server_url, tiempo_espera, umbral_temperatura_alta, ser)

            except Exception as e:
                print(f"Error: {e}")

    def handle_motion_detection(self, PIR_PIN, DHT_SENSOR, server_url, tiempo_espera, umbral_temperatura_alta, ser):
        """
        Maneja la detección de movimiento.
        """
        self.event_history.append({"timestamp": time.strftime("%Y%m%d%H%M%S"), "evento": "Detección de movimiento"})

        public_ip = self.get_public_ip()
        rfid_data = ser.readline().decode('utf-8').strip()

        humidity, temperature = self.read_sensor(DHT_SENSOR, DHT_PIN)

        if humidity is not None and temperature is not None:
            self.handle_successful_sensor_read(humidity, temperature, rfid_data, public_ip, server_url)
        else:
            self.handle_failed_sensor_read()

        time.sleep(tiempo_espera)

    def handle_successful_sensor_read(self, humidity, temperature, rfid_data, public_ip, server_url):
        """
        Maneja la lectura exitosa del sensor.
        """
        features = np.array([0.0, 0.0, 0.0, 0.0])  # Ajusta según tus características
        prediction = self.predict(features)
        target = 0.9  # Ajusta según tus necesidades
        self.update(features, target)

        payload = {
            "rfid": rfid_data,
            "temperature": temperature,
            "prediction": prediction,
            "public_ip": public_ip
        }
        self.send_data_to_server(payload, server_url)

        self.adjust_dynamic_settings(temperature)

    def handle_failed_sensor_read(self):
        """
        Maneja la lectura fallida del sensor.
        """
        print("Error al leer el sensor de temperatura")

    def send_data_to_server(self, payload, server_url):
        """
        Envía los datos al servidor y registra el evento.
        """
        try:
            payload["public_ip"] = self.get_public_ip()  # Agrega la IP pública al payload
            response = requests.post(server_url, json=payload)
            self.event_history.append({"timestamp": time.strftime("%Y%m%d%H%M%S"), "evento": "Envío de datos al servidor"})
            print("Datos enviados al servidor")

        except Exception as e:
            print(f"Error al enviar datos al servidor: {e}")

    def adjust_dynamic_settings(self, temperature):
        """
        Ajusta dinámicamente la configuración basada en la temperatura.
        """
        global tiempo_espera
        if temperature > umbral_temperatura_alta:
            tiempo_espera = max(tiempo_espera - 1, 5)
        else:
            tiempo_espera = min(tiempo_espera + 1, 20)
        print(f"Tiempo de espera ajustado a {tiempo_espera} segundos")

    def get_public_ip(self):
        try:
            # Utiliza api.ipify.org para obtener la IP pública
            response = requests.get('https://api.ipify.org?format=json')
            public_ip = response.json().get('ip', 'Desconocido')
            return public_ip
        except Exception as e:
            print(f"Error al obtener la IP pública: {e}")
            return 'Desconocido'

# Ejemplo de uso
if __name__ == "__main__":
    PIR_PIN = 11
    DHT_SENSOR = Adafruit_DHT.DHT11
    DHT_PIN = 4
    server_url = "http://192.168.68.16:5000/verify_rfid"
    tiempo_espera = 10
    umbral_temperatura_alta = 30.0
    

    model = ReinforcementLearningModel(input_size=4)  # Ajusta el tamaño según tus características de entrada
    model.main_loop(PIR_PIN, DHT_SENSOR, server_url, tiempo_espera, umbral_temperatura_alta)
