#include <Adafruit_Sensor.h>
#include <Arduino.h>
#include <ArduinoJson.h>
#include <ESPAsyncWebServer.h>
#include <HTTPClient.h>
#include <M5StickC.h>

#include <config.h>
#include <secret.h>

AsyncWebServer server(80);

StaticJsonDocument<192> json_doc;
HTTPClient http;

const int update_interval_sec = 30;

bool drying = false;

float external_temperature, external_humidity, internal_temperature,
    internal_humidity;

void setup() {
  json_doc["device_id"] = DEVICE_ID;

  M5.begin();
  Serial.begin(115200);

  // WiFi Setup

#if STATIC_IP
  WiFi.config(ip, gateway, subnet);
#endif

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    // Serial.println("Connecting to WiFi...");
    M5.Lcd.fillScreen(BLACK);               // 画面の塗りつぶし
    M5.Lcd.setCursor(0, 0);                 // 文字列の書き出し位置
    M5.Lcd.setTextSize(3);                  // 文字サイズを設定
    M5.Lcd.printf("Connecting to WiFi..."); // シリアルモニタ
  }

  // リクエストに応じてJSON形式のデータを返すエンドポイントの設定
  server.on("/data", HTTP_GET, [](AsyncWebServerRequest *request) {
    char exporter_plain_json[1536];
    serializeJson(json_doc, exporter_plain_json, sizeof(exporter_plain_json));

    request->send(200, "application/json", exporter_plain_json);
  });

  // サーバーの開始
  server.begin();
}

String get_session() {
  http.begin(String(HOST_URL) + String("/api/session/?shoe_id=") +
             String(DEVICE_ID));

  int httpCode = http.GET();
  String payload = http.getString();
  http.end();
  return payload;
}

int send_to_server(StaticJsonDocument<192> doc) {
  char sender_plain_json[1536];
  serializeJson(doc, sender_plain_json, sizeof(sender_plain_json));

  http.begin(HOST_URL);
  http.addHeader("Content-Type", "application/json");

  int st = http.POST((uint8_t *)sender_plain_json, strlen(sender_plain_json));

  http.end();
  return st;
}

int speed = 1;

long long timer = 0;

void loop() {
  if (millis() - timer > update_interval_sec * 1000) {
    timer = millis();

    Serial.println(WiFi.localIP());

    Serial.println(get_session());
  };
}
