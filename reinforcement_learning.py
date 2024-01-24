
#reinforcement_learning.py



import numpy as np
from sklearn.linear_model import SGDRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import os

class ReinforcementLearningModel:
    def __init__(self, input_size):
        self.input_size = input_size
        self.model = make_pipeline(StandardScaler(), SGDRegressor())

        # Cargar el modelo previo si existe
        self.load_model()

    def predict(self, state):
        return self.model.predict([state])[0]

    def update(self, state, target):
        self.model.partial_fit([state], [target])

    def save_model(self):
        with open("rl_model.npy", "wb") as file:
            np.save(file, self.model.named_steps['sgdregressor'].coef_)

    def load_model(self):
        if os.path.exists("rl_model.npy"):
            with open("rl_model.npy", "rb") as file:
                weights = np.load(file)
                self.model.named_steps['sgdregressor'].coef_ = weights

# Ejemplo de uso
if __name__ == "__main__":
    model = ReinforcementLearningModel(input_size=4)  # Ajusta el tamaño según tus características de entrada

    # Ejemplo de predicción
    state = [0.8, 25, 0, 0]  # Ejemplo de estado, ajusta según tus características
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
