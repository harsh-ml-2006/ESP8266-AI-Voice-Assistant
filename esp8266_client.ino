// esp8266_client.ino - Shayan's Contribution
// ==========================================
// ESP8266 TCP Client and I2S Audio Interface
// ==========================================
#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <I2S.h>

const char* ssid = "oppo";
const char* password = "123456789";
const char* host = "10.126.188.224"; 
const uint16_t port = 5000;

WiFiClient client;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✅ Network Connected!");

  // Initialize I2S Hardware Interface
  i2s_begin();
  i2s_set_rate(16000); 
}

void loop() {
  // Maintain TCP Connection
  if (!client.connected()) {
    if (!client.connect(host, port)) {
      delay(1000);
      return;
    }
  }

  // 1. Microphone Input (Read I2S)
  int16_t left_sample = 0, right_sample = 0;
  i2s_read_sample(&left_sample, &right_sample, true);
  
  // Noise Reduction filter
  int16_t clean_sample = left_sample >> 2; 
  client.write((const uint8_t*)&clean_sample, sizeof(clean_sample));

  // 2. Speaker Output (Write I2S)
  if (client.available()) {
    uint8_t buffer[1024];
    int bytesRead = client.read(buffer, sizeof(buffer));
    
    for (int i = 0; i < bytesRead; i += 2) {
      int16_t sample = (buffer[i+1] << 8) | buffer[i]; 
      uint32_t sample32 = ((uint32_t)(uint16_t)sample) << 16;
      sample32 |= ((uint32_t)(uint16_t)sample); 
      i2s_write_sample(sample32);
    }
  }
}
