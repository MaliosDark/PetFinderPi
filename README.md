
## 🐾 **Welcome to PetFinderPi!** 🐾

PetFinderPi is an innovative project designed to assist in the timely location and rescue of lost pets, with a primary focus on dogs and cats. This cutting-edge solution integrates a modular design, harnessing the capabilities of Python and the Raspberry Pi ecosystem to create an efficient and versatile system.

## Key Features:

### 📷 **Automated Image Capture**
PetFinderPi utilizes the Raspberry Pi Camera to automatically capture images upon detecting motion. This feature aids in visually identifying potential lost pets and enhances the search process.

### 🕵️ **Animal Classification using MobileNetV2**
The project incorporates the powerful MobileNetV2 deep learning model to classify and identify animals within captured images. This ensures accurate recognition of lost pets, distinguishing them from other wildlife.

### 🌡️ **Temperature Monitoring with DHT22 Sensor**
PetFinderPi includes a DHT22 temperature sensor to monitor environmental conditions. This valuable data helps understand how temperature variations may impact the behavior of lost animals, optimizing search efforts.

### 🔄 **Reinforcement Learning for Location Prediction**
The system employs a reinforcement learning model to predict potential locations of lost pets. Factors such as confidence from animal classification, temperature, and time of day are considered. This predictive capability enhances the system's effectiveness in locating and rescuing missing pets.

PetFinderPi is not just a project; it's a compassionate solution aimed at reuniting families with their beloved pets. Explore the features, contribute to the code, and join us in making a positive impact on pet welfare! 🐾🏠

## Prerequisites

Before you start, make sure you have:

- 🍓 **Raspberry Pi Configured with Raspbian OS**: Ensure your Raspberry Pi is set up with the Raspbian operating system.

- 📷 **Raspberry Pi Camera Connected**: Attach the Raspberry Pi Camera to capture high-quality images.

- 🌐 **Internet Connection for Data Transmission**: Establish an internet connection for transmitting captured data to a server.

- ⚙️ **RFID Scanner Connected to USB Port**: Connect an RFID scanner to a USB port for additional identification capabilities.

- 🌡️ **DHT22 Temperature Sensor Wired Up**: Set up the DHT22 sensor to measure temperature. ( i`m going to be Updating it to a DHT11 that can check humidity and temperature )


## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/MaliosDark/PetFinderPi.git
   ```

2. Navigate to the project folder:

   ```bash
   cd PetFinderPi
   ```

3. Install dependencies: ( when available. Pips for installation are inside start.py )

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the main script:

   ```bash
   python start.py
   ```

 **The script will detect motion, capture images, classify animals, and predict locations using reinforcement learning.**

2. Monitor the logs:

   Check the `logs/event_history.txt` file for a detailed history of events.

## Contributing

👩‍💻👨‍💻 Contributions are welcome! Feel free to open issues and pull requests.

## License

This project is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html) - see the [LICENSE](LICENSE) file for details.


Running on Raspberry pi 3 x32 i  encounter that i need it to install bazel for use tensorflow




1. **Instalar dependencias necesarias:**
    ```bash
    sudo apt-get install -y pkg-config zip g++ zlib1g-dev unzip python3
    ```

2. **Descargar las fuentes de Bazel:**
    ```bash
    wget https://github.com/bazelbuild/bazel/releases/download/3.7.2/bazel-3.7.2-dist.zip
    ```

3. **Descomprimir el archivo:**
    ```bash
    mkdir bazel
    cd bazel
    unzip ../bazel-3.7.2-dist.zip
    ```

4. **Configurar e instalar Bazel:**
    ```bash
    ./compile.sh
    ```

5. **Mover el ejecutable a un directorio en tu PATH:**
    ```bash
    sudo cp output/bazel /usr/local/bin/
    ```

Después de estos pasos, intenta verificar la versión de Bazel:

```bash
bazel version
```

## Puedes intentar instalar TensorFlow directamente desde las fuentes utilizando el código fuente. Aquí tienes los pasos:

1. **Instalar las dependencias necesarias:**
   ```bash
   sudo apt-get update
   sudo apt-get install -y libhdf5-dev libc-ares-dev libeigen3-dev
   ```

2. **Instalar el compilador de Cython:**
   ```bash
   pip3 install cython
   ```

3. **Clonar el repositorio de TensorFlow para Raspberry Pi:**
   ```bash
   git clone https://github.com/tensorflow/tensorflow.git -b v2.6.0 --depth=1
   ```

   Asegúrate de ajustar la etiqueta de versión (`-b`) según la versión deseada.

4. **Configurar TensorFlow:**
   ```bash
   cd tensorflow
   ./configure
   ```

   Durante la configuración, asegúrate de seleccionar las opciones adecuadas para tu sistema.

5. **Compilar TensorFlow:**
   ```bash
   bazel build --local_ram_resources=2048 --local_cpu_resources=2 --verbose_failures -c opt --copt=-mfpu=neon-vfpv4 --copt=-funsafe-math-optimizations --copt=-ftree-vectorize --copt=-fomit-frame-pointer --copt=-funsafe-math-optimizations --copt=-march=native --copt=-Wno-sign-compare --cxxopt="-D_GLIBCXX_USE_CXX11_ABI=0" //tensorflow/tools/pip_package:build_pip_package
   ```

   Esto tomará un tiempo y es posible que necesites ajustar las opciones según tu configuración.

6. **Generar el paquete de TensorFlow:**
   ```bash
   ./bazel-bin/tensorflow/tools/pip_package/build_pip_package /tmp/tensorflow_pkg
   ```

7. **Instalar TensorFlow desde el paquete generado:**
   ```bash
   pip3 install /tmp/tensorflow_pkg/*.whl
   ```

Estos pasos deberían compilar e instalar TensorFlow en tu Raspberry Pi. Ten en cuenta que la compilación puede llevar bastante tiempo y es posible que necesites espacio libre en disco.