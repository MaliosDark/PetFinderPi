# reinforcement_learning.py

import numpy as np
import os

class ReinforcementLearningModel:
    def __init__(self, input_size):
        self.weights = np.zeros(input_size)
        self.learning_rate = 0.1  # Tasa de aprendizaje inicial

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

    def save_model(self):
        """
        Guarda el modelo en un archivo.
        """
        model_data = {"weights": self.weights, "learning_rate": self.learning_rate}
        model_folder = "models"
        os.makedirs(model_folder, exist_ok=True)
        model_path = os.path.join(model_folder, "rl_model.npy")

        with open(model_path, "wb") as file:
            np.save(file, model_data)
        print(f"Modelo guardado en: {model_path}")

    def load_model(self):
        """
        Carga el modelo desde un archivo si existe.
        """
        model_folder = "models"
        model_path = os.path.join(model_folder, "rl_model.npy")

        if os.path.exists(model_path):
            with open(model_path, "rb") as file:
                data = np.load(file, allow_pickle=True).item()
                self.weights = data["weights"]
                self.learning_rate = data["learning_rate"]
                print(f"Modelo cargado desde: {model_path}")

# Ejemplo de uso
if __name__ == "__main__":
    model = ReinforcementLearningModel(input_size=4)  # Ajusta el tamaño según tus características de entrada

    # Ejemplo de predicción
    state = np.array([0.8, 25, 0, 0])  # Ejemplo de estado, ajusta según tus características
    prediction = model.predict(state)
    print(f"Predicción inicial: {prediction}")

    # Ejemplo de actualización
    target = 0.9  # Valor objetivo, ajusta según tus necesidades
    model.update(state, target)

    # Guardar el modelo actualizado
    model.save_model()

    # Predicción después de la actualización
    updated_prediction = model.predict(state)
    print(f"Predicción después de la actualización: {updated_prediction}")
