#include <Arduino.h>

// put function declarations here:
// Unified Sensor Library Example
// Written by Tony DiCola for Adafruit Industries
// Released under an MIT license.

// REQUIRES the following Arduino libraries:
// - DHT Sensor Library: https://github.com/adafruit/DHT-sensor-library
// - Adafruit Unified Sensor Lib: https://github.com/adafruit/Adafruit_Sensor
#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>
#include <ESPAsyncWebServer.h>
#include <config.h>
AsyncWebServer server(80);

#define DHT1 5
#define DHT2 16
#define DHT3 19
// 25, 27, 32

#define DHTTYPE DHT22 // DHT 22 (AM2302)

DHT_Unified dht1(DHT1, DHTTYPE);
DHT_Unified dht2(DHT2, DHTTYPE);
DHT_Unified dht3(DHT3, DHTTYPE);

uint32_t delayMS;

float temperature1, temperature2, temperature3;
float humidity1, humidity2, humidity3;

void setup() {
  Serial.begin(115200);
  // Initialize device.
  dht1.begin();
  dht2.begin();
  dht3.begin();
  sensor_t sensor;
  delayMS = sensor.min_delay / 1000;

  // WiFi Setup

#if STATIC_IP
  WiFi.config(ip, gateway, subnet);
#endif

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  // リクエストに応じてJSON形式のデータを返すエンドポイントの設定
  server.on("/data", HTTP_GET, [](AsyncWebServerRequest *request) {
    String jsonData = "";
    jsonData += "{\n";
    jsonData += "  \"sensor1\": {\n";
    jsonData += "    \"temperature\": " + String(temperature1, 2) + ",\n";
    jsonData += "    \"humidity\": " + String(humidity1, 2) + "\n";
    jsonData += "  },\n";
    jsonData += "  \"sensor2\": {\n";
    jsonData += "    \"temperature\": " + String(temperature2, 2) + ",\n";
    jsonData += "    \"humidity\": " + String(humidity2, 2) + "\n";
    jsonData += "  },\n";
    jsonData += "  \"sensor3\": {\n";
    jsonData += "    \"temperature\": " + String(temperature3, 2) + ",\n";
    jsonData += "    \"humidity\": " + String(humidity3, 2) + "\n";
    jsonData += "  }\n";
    jsonData += "}\n";
    request->send(200, "application/json", jsonData);
  });

  // サーバーの開始
  server.begin();
}

void loop() {
  Serial.println(WiFi.localIP());
  // Delay between measurements.
  delay(delayMS);
  // Get temperature event and print its value.
  sensors_event_t event;
  // DHT1

  dht1.temperature().getEvent(&event);
  if (isnan(event.temperature)) {
    Serial.println(F("Error reading temperature!"));
  } else {
    temperature1 = event.temperature;
  }
  // Get humidity event and print its value.
  dht1.humidity().getEvent(&event);
  if (isnan(event.relative_humidity)) {
    Serial.println(F("Error reading humidity!"));
  } else {
    humidity1 = event.relative_humidity;
  }

  // DHT2
  dht2.temperature().getEvent(&event);
  if (isnan(event.temperature)) {
    Serial.println(F("Error reading temperature!"));
  } else {
    temperature2 = event.temperature;
  }
  // Get humidity event and print its value.
  dht2.humidity().getEvent(&event);
  if (isnan(event.relative_humidity)) {
    Serial.println(F("Error reading humidity!"));
  } else {
    humidity2 = event.relative_humidity;
  }

  // DHT3
  dht3.temperature().getEvent(&event);
  if (isnan(event.temperature)) {
    Serial.println(F("Error reading temperature!"));
  } else {
    temperature3 = event.temperature;
  }
  // Get humidity event and print its value.
  dht3.humidity().getEvent(&event);
  if (isnan(event.relative_humidity)) {
    Serial.println(F("Error reading humidity!"));
  } else {
    humidity3 = event.relative_humidity;
  }

  // Serial.printf("Temperature: %f *C \t Humidity: %f %% \n", humidity,
  //               temperature);
}
