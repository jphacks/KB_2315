#include <Arduino.h>
#include <M5Core2.h>

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
#include <HTTPClient.h>
#include <config.h>
AsyncWebServer server(80);

#define DHT1 27
#define DHT2 19
#define DHT3 25
#define FAN 26
// 25, 27, 32

#define DHTTYPE DHT22 // DHT 22 (AM2302)

DHT_Unified ShoesSensor1(DHT1, DHTTYPE);
DHT_Unified ShoesSensor2(DHT2, DHTTYPE);
DHT_Unified RoomSensor(DHT3, DHTTYPE);

uint32_t delayMS;
HTTPClient http;

float ShoesTemp1, ShoesTemp2, RoomTemp;
float ShoesHumi1, ShoesHumi2, RoomHumi;

int count = 0;

void setup() {
  M5.begin();
  //Serial.begin(115200);
  // Initialize device.
  ShoesSensor1.begin();
  ShoesSensor2.begin();
  RoomSensor.begin();
  sensor_t sensor;
  delayMS = sensor.min_delay;
  pinMode(FAN, OUTPUT);

  digitalWrite(FAN,1);

  // WiFi Setup

#if STATIC_IP
  WiFi.config(ip, gateway, subnet);
#endif

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    //Serial.println("Connecting to WiFi...");
    M5.Lcd.fillScreen(BLACK);  // 画面の塗りつぶし
    M5.Lcd.setCursor(0, 0);  // 文字列の書き出し位置
    M5.Lcd.setTextSize(3);  // 文字サイズを設定  
    M5.Lcd.printf("Connecting to WiFi...");  // シリアルモニタ
  }
  //Serial.println("Connected to WiFi");
  M5.Lcd.fillScreen(BLACK);  // 画面の塗りつぶし
  M5.Lcd.setCursor(0, 0);  // 文字列の書き出し位置
  M5.Lcd.setTextSize(3);  // 文字サイズを設定  
  M5.Lcd.printf("Connected to WiFi"); 

  // リクエストに応じてJSON形式のデータを返すエンドポイントの設定
  server.on("/data", HTTP_GET, [](AsyncWebServerRequest *request) {
    String jsonData = "";
    jsonData += "{\n";
    jsonData += "  \"sensor1\": {\n";
    jsonData += "    \"temperature\": " + String(ShoesTemp1, 2) + ",\n";
    jsonData += "    \"humidity\": " + String(ShoesHumi1, 2) + "\n";
    jsonData += "  },\n";
    jsonData += "  \"sensor2\": {\n";
    jsonData += "    \"temperature\": " + String(ShoesTemp2, 2) + ",\n";
    jsonData += "    \"humidity\": " + String(ShoesHumi2, 2) + "\n";
    jsonData += "  },\n";
    jsonData += "  \"sensor3\": {\n";
    jsonData += "    \"temperature\": " + String(RoomTemp, 2) + ",\n";
    jsonData += "    \"humidity\": " + String(RoomHumi, 2) + "\n";
    jsonData += "  }\n";
    jsonData += "}\n";
    request->send(200, "application/json", jsonData);
  });

  // サーバーの開始
  server.begin();
}

int send_to_server(int id, bool status) {
  http.begin(HOST_URL);
  http.addHeader("Content-Type", "application/json");
  int st = http.POST("{\"id\":" + String(id) + ",\"status\":" + String(status) +
                     "}");
  http.end();
  return st;
}

void loop() {
  Serial.println(WiFi.localIP());
  // Delay between measurements.
  delay(delayMS);
  // Get temperature event and print its value.
  sensors_event_t event;
  // ShoesSensor1

  ShoesSensor1.temperature().getEvent(&event);
  if (isnan(event.temperature)) {
    //Serial.println(F("Error reading temperature!"));
    M5.Lcd.printf("Error reading ShoesTemp1!");
  } else {
    ShoesTemp1 = event.temperature;
  }
  // Get humidity event and print its value.
  ShoesSensor1.humidity().getEvent(&event);
  if (isnan(event.relative_humidity)) {
    //Serial.println(F("Error reading humidity!"));
    M5.Lcd.printf("Error reading ShoesHumi1!");
  } else {
    ShoesHumi1 = event.relative_humidity;
  }

  // ShoesSensor2
  ShoesSensor2.temperature().getEvent(&event);
  if (isnan(event.temperature)) {
    //Serial.println(F("Error reading temperature!"));
    M5.Lcd.printf("Error reading ShoesTemp2!");
  } else {
    ShoesTemp2 = event.temperature;
  }
  // Get humidity event and print its value.
  ShoesSensor2.humidity().getEvent(&event);
  if (isnan(event.relative_humidity)) {
    //Serial.println(F("Error reading humidity!"));
    M5.Lcd.printf("Error reading ShoesHumi2!");   
  } else {
    ShoesHumi2 = event.relative_humidity;
  }

  // RoomSensor
  RoomSensor.temperature().getEvent(&event);
  if (isnan(event.temperature)) {
    //Serial.println(F("Error reading temperature!"));
    M5.Lcd.printf("Error reading RoomTemp!");   
  } else {
    RoomTemp = event.temperature;
  }
  // Get humidity event and print its value.
  RoomSensor.humidity().getEvent(&event);
  if (isnan(event.relative_humidity)) {
    //Serial.println(F("Error reading humidity!"));
    M5.Lcd.printf("Error reading RoomHumi!");    
  } else {
    RoomHumi = event.relative_humidity;
  }
  //Serial.printf("Temperature: %f *C \t Humidity: %f %% \n", ShoesTemp1,
                //ShoesHumi1);
  M5.Lcd.fillScreen(BLACK);  // 画面の塗りつぶし
  M5.Lcd.setCursor(0, 0);  // 文字列の書き出し位置
  M5.Lcd.setTextSize(3);  // 文字サイズを設定  
  M5.Lcd.printf("ShoesTemp1: %f *C \t ShoesHumi1: %f %% \n", ShoesTemp1,
                ShoesHumi1);
  M5.Lcd.printf("ShoesTemp2: %f *C \t ShoesHumi2: %f %% \n", ShoesTemp2,
                ShoesHumi2);
  M5.Lcd.printf("RoomTemp: %f *C \t ShoesHumi2: %f %% \n", RoomTemp,
                ShoesHumi2);
  count++;
  if(count>=500)
  {
    analogWrite(FAN, 128);  
  }   
}
