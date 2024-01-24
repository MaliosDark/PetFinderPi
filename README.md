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

3. Install dependencies:
**( when available. Pips for installation are inside start.py )**

   ```bash
   pip install -r requirements.txt

   ```

## Usage

1. Run the main script:

   ```bash
   python start.py
   ```

### **   The script will detect motion, capture images, classify animals, and predict locations using reinforcement learning. ** ###

2. Monitor the logs:

   Check the `logs/event_history.txt` file for a detailed history of events.

## Contributing

👩‍💻👨‍💻 Contributions are welcome! Feel free to open issues and pull requests.

## License

This project is licensed under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html) - see the [LICENSE](LICENSE) file for details.
