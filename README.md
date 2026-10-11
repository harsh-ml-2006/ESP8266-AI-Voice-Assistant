# ESP8266 AI Voice Chatbot
An intelligent two-way voice assistant utilizing ESP8266, I2S Audio, TCP Networking, and Google Gemini API.

## Team Members
* Harsh Kumar 
* Sagnik 
* Shayan 
* Shristi 
* Santanu 

## Hardware Setup
* NodeMCU ESP8266
* INMP441 I2S Microphone (VCC -> 3.3V, GND -> GND, WS -> D4, SCK -> D8, SD -> RX)
* MAX98357A I2S DAC Audio Amplifier (Speaker Output)

## Software Stack
* **Microcontroller:** C++ / Arduino IDE (WiFi Client, I2S Audio Streaming)
* **Backend Server:** Python 3 (TCP Socket Server)
* **AI & Processing:** Google Generative AI (Gemini Flash), SpeechRecognition, Edge-TTS

## How to Run
1. Update `config.py` with your active API keys.
2. Run `server.py` to start the TCP listener on port 5000.
3. Power on the ESP8266 module to establish the connection and start streaming raw PCM audio.
