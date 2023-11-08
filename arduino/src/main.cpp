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
HTTPClient http_session;
HTTPClient http_sensor;

const int update_interval_sec = 30;

bool drying = false;

long long timer = 0;

float RoomTemp, RoomHumi, ShoeTemp, ShoeHumi;

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
    M5.Lcd.setTextSize(1);                  // 文字サイズを設定
    M5.Lcd.printf("Connecting to WiFi..."); // シリアルモニタ
  }

  M5.Lcd.fillScreen(BLACK);      // 画面の塗りつぶし
  M5.Lcd.setCursor(0, 0);        // 文字列の書き出し位置
  M5.Lcd.setTextSize(1);         // 文字サイズを設定
  M5.Lcd.printf("WiFi Success"); // シリアルモニタ

  // リクエストに応じてJSON形式のデータを返すエンドポイントの設定
  server.on("/data", HTTP_GET, [](AsyncWebServerRequest *request) {
    char exporter_plain_json[1536];
    serializeJson(json_doc, exporter_plain_json, sizeof(exporter_plain_json));

    request->send(200, "application/json", exporter_plain_json);
  });

  // サーバーの開始
  server.begin();
}

String get_session_id() {
  String url =
      String(HOST_URL) + String("/api/session/?shoe_id=") + String(DEVICE_ID);
  http_session.begin(url);

  int httpCode = http_session.GET();
  String payload = http_session.getString();
  http_session.end();

  StaticJsonDocument<96> resp_json;

  DeserializationError error = deserializeJson(resp_json, payload);

  if (!error) {
    const char *sessionID = resp_json["session_id"];
    Serial.println("Session ID: " + String(sessionID));
    return String(sessionID);
  } else {
    Serial.println("Failed to parse JSON");
    return "";
  }
}

int send_to_server(StaticJsonDocument<192> doc) {
  char sender_plain_json[1536];
  serializeJson(doc, sender_plain_json, sizeof(sender_plain_json));

  String url = String(HOST_URL) + String("/api/sensor/");
  http_sensor.begin(url);

  http_sensor.addHeader("Content-Type", "application/json");

  int st =
      http_sensor.POST((uint8_t *)sender_plain_json, strlen(sender_plain_json));

  http_sensor.end();
  return st;
}

void insert_value() {
  json_doc["external_temperature"] = RoomTemp;
  json_doc["external_humidity"] = RoomHumi;

  json_doc["internal_temperature"] = ShoeTemp;
  json_doc["internal_humidity"] = ShoeHumi;
}

bool is_drying() {
  if (abs(ShoeTemp - RoomTemp) < GAP_TEMP && (ShoeHumi - RoomHumi) > GAP_HUM) {
    return true;
  } else {
    return false;
  }
}

void main_func() {
  insert_value();
  bool current_drying = is_drying();

  if (drying) { // 乾燥実行中
    if (current_drying) {
      // 靴が湿気ている
      send_to_server(json_doc);
    } else {
      // 靴が湿気ていない
      drying = false;
      json_doc["drying"] = drying;
      send_to_server(json_doc);
    }
  } else { // 乾燥未実行
    if (current_drying) {
      // 靴が湿気ている
      drying = true;

      json_doc["drying"] = drying;
      json_doc["session_id"] = get_session_id();
      send_to_server(json_doc);
    }
  }
}

void sample() {
  Serial.println(WiFi.localIP());

  drying = true;
  json_doc["drying"] = drying;

  json_doc["session_id"] = get_session_id();

  for (int i = 0; i < 5; i++) {
    RoomTemp = random(2000, 2500) / 100.00;
    ShoeTemp = random(2000, 2500) / 100.00;

    RoomHumi = random(0000, 4000) / 100.00;
    ShoeHumi = random(4000, 10000) / 100.00;

    insert_value();
    if (i == 4) {
      drying = false;
      json_doc["drying"] = drying;
    }
    Serial.println(send_to_server(json_doc));

    delay(2000);
  }
}

void loop() {
  if (millis() - timer > update_interval_sec * 1000) {
    timer = millis();

    sample();
  }
}