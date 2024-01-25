#animal_functions.py

from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input, decode_predictions
from tensorflow.keras.preprocessing import image
import numpy as np
import cv2

# Configuración del modelo de clasificación de animales
model = MobileNetV2(weights='imagenet')

def predict_animal(frame):
    # Preprocesar el frame para el modelo
    frame_resized = cv2.resize(frame, (224, 224))
    img_array = np.expand_dims(frame_resized, axis=0)
    img_array = preprocess_input(img_array)

    # Realizar la predicción
    predictions = model.predict(img_array)
    decoded_predictions = decode_predictions(predictions, top=1)[0]
    _, animal_class, animal_confidence = decoded_predictions[0]

    return animal_class, animal_confidence

def encode_animal(animal_class):
    # Codificación básica de la clase del animal
    if animal_class == "perro":
        return np.array([[0.8]])
    elif animal_class == "gato":
        return np.array([[0.5]])
    else:
        return np.array([[0.2]])

def get_time_of_day():
    # Lógica para obtener la hora del día (por ejemplo, basada en la hora actual)
    current_hour = int(time.strftime("%H"))
    if 6 <= current_hour < 12:
        return np.array([[0.8]])  # Mañana
    elif 12 <= current_hour < 18:
        return np.array([[0.5]])  # Tarde
    else:
        return np.array([[0.2]])  # Noche
