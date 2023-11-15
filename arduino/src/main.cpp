//#include <Adafruit_Sensor.h>
#include <Arduino.h>
#include <ArduinoJson.h>
#include <ESPAsyncWebServer.h>
#include <HTTPClient.h>
//#include <M5StickC.h>
#include <M5StickCPlus.h>
#include "M5_ENV.h"
#include "UNIT_HBRIDGE.h"

#include <config.h>
#include <secret.h>

AsyncWebServer server(80);

StaticJsonDocument<192> json_doc;
HTTPClient http_session;
HTTPClient http_sensor;
SHT3X unitsht30;
QMP6988 unitqmp6988;
SHT3X hatsht30;
QMP6988 hatqmp6988;
UNIT_HBRIDGE driver;


const int update_interval_sec = 10;

bool drying = false;

long long timer = 0;

float RoomTemp, RoomHumi, RoomPre, ShoeTemp, ShoeHumi, ShoePre;
float volt = 0.0; //デバッグ用
int debug_flag = 0;

void setup() {
  json_doc["device_id"] = DEVICE_ID;

  M5.begin();
  Serial.begin(115200);
  Wire1.end();
  Wire.begin(32,33);  // Wire init, adding the I2C bus.  Wire初始化, 加入i2c总线
  Wire1.begin(0, 26);
  hatsht30.init(0x44, &Wire1);
  unitsht30.init(0x44, &Wire);
  hatqmp6988.init(QMP6988_SLAVE_ADDRESS_L,&Wire1);
  unitqmp6988.init(QMP6988_SLAVE_ADDRESS_H,&Wire);
  driver.begin(&Wire, HBRIDGE_ADDR, 32, 33, 100000L);

  // WiFi Setup

#if STATIC_IP
  WiFi.config(ip, gateway, subnet);
#endif

  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    // Serial.println("Connecting to WiFi...");
    M5.Lcd.fillScreen(BLACK);               // 画面の塗りつぶし
#if 0
    M5.Lcd.setCursor(0, 0);                 // 文字列の書き出し位置
    M5.Lcd.setTextSize(1);                  // 文字サイズを設定
    M5.Lcd.printf("Connecting to WiFi..."); // シリアルモニタ
#endif
    M5.Lcd.setRotation(3);
    M5.Lcd.setTextColor(MAROON, BLACK);  
    M5.Lcd.setCursor(15, 45);
    M5.Lcd.setTextSize(5);         // 文字サイズを設定
    M5.Lcd.printf("Setting");
  }

  M5.Lcd.fillScreen(BLACK);      // 画面の塗りつぶし
#if 0
  M5.Lcd.setCursor(0, 0);        // 文字列の書き出し位置
  M5.Lcd.setTextSize(1);         // 文字サイズを設定
  M5.Lcd.printf("WiFi Success"); // シリアルモニタ
#endif
  M5.Lcd.setRotation(3);
  M5.Lcd.setTextColor(RED, BLACK);  
  M5.Lcd.setCursor(15, 45);
  M5.Lcd.setTextSize(5);         // 文字サイズを設定
  M5.Lcd.printf("Setting");
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
      String(HOST_URL) + String("/api/session/?device_id=") + String(DEVICE_ID);
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
  if (abs(ShoeTemp - RoomTemp) > GAP_TEMP && (ShoeHumi - RoomHumi) > GAP_HUM) {
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
      //乾燥続行
      driver.setDriverDirection(1);
      driver.setDriverSpeed8Bits(255);
      send_to_server(json_doc);
      if(debug_flag == 0){
        M5.Lcd.fillScreen(BLACK);
        M5.Lcd.setRotation(3);
        M5.Lcd.setTextColor(GREEN, BLACK);  
        M5.Lcd.setCursor(20, 45);
        M5.Lcd.setTextSize(5);         // 文字サイズを設定
        M5.Lcd.printf("Drying!");
      }
    } else {
      // 靴が湿気ていない
      //乾燥終了
      driver.setDriverDirection(0);
      driver.setDriverSpeed8Bits(0);
      drying = false;
      json_doc["drying"] = drying;
      send_to_server(json_doc);
      if(debug_flag == 0){  
        M5.Lcd.fillScreen(BLACK);
        M5.Lcd.setRotation(3);
        M5.Lcd.setTextColor(BLUE, BLACK);  
        M5.Lcd.setCursor(0, 45);
        M5.Lcd.setTextSize(5);         // 文字サイズを設定
        M5.Lcd.printf("Complete");
      }
    }
  } else { // 乾燥未実行
    if (current_drying) {
      // 靴が湿気ている
      //乾燥開始
      driver.setDriverDirection(1);
      driver.setDriverSpeed8Bits(255);
      drying = true;

      json_doc["drying"] = drying;
      json_doc["session_id"] = get_session_id();
      send_to_server(json_doc);
      if(debug_flag == 0){  
        M5.Lcd.fillScreen(BLACK);
        M5.Lcd.setRotation(3);
        M5.Lcd.setTextColor(GREEN, BLACK);  
        M5.Lcd.setCursor(20, 45);
        M5.Lcd.setTextSize(5);         // 文字サイズを設定
        M5.Lcd.printf("Drying!");
      }
    }
    else{
      if(debug_flag == 0){  
        M5.Lcd.fillScreen(BLACK);
        M5.Lcd.setRotation(3);
        M5.Lcd.setTextColor(ORANGE, BLACK);  
        M5.Lcd.setCursor(20, 45);
        M5.Lcd.setTextSize(5);         // 文字サイズを設定
        M5.Lcd.printf("Waiting");
      }
    }
  }
  if(debug_flag == 1){
  //デバッグ用
    M5.Lcd.setRotation(3);
    M5.Lcd.fillScreen(BLACK);
    M5.Lcd.setCursor(0, 20);
    M5.Lcd.setTextSize(2);
    M5.Lcd.setTextColor(WHITE, BLACK);  
    volt = driver.getAnalogInput(_12bit) / 4095.0f * 3.3f / 0.09f;
    M5.Lcd.printf("Room T:%2.1f, H:%2.0f%%, P:%2.0fPa\r\n",
                  RoomTemp, RoomHumi, RoomPre);
    M5.Lcd.printf("Shoe T:%2.1f, H:%2.0f%%, P:%2.0fPa\r\n",
                  ShoeTemp, ShoeHumi, ShoePre);

    M5.Lcd.printf("Voltage:%.2fV\r\n", volt);  
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

void scan() {
  Serial.println(WiFi.localIP());

  //drying = true;
  json_doc["drying"] = drying;

  json_doc["session_id"] = get_session_id();
  //Hatが室内環境計測
  RoomPre = hatqmp6988.calcPressure(); 
  if (hatsht30.get() == 0) {  
    RoomTemp = hatsht30.cTemp;
    RoomHumi = hatsht30.humidity;
  } else {//温湿度取れない場合は気圧もクリア
      RoomTemp = 0, RoomHumi = 0, RoomPre = 0;
  }
  //Unitが室内環境計測
  ShoePre = unitqmp6988.calcPressure();   
  if (unitsht30.get() == 0) {// 温湿度取得
    ShoeTemp = unitsht30.cTemp;
    ShoeHumi = unitsht30.humidity;
  } else {//温湿度取れない場合は気圧もクリア
      ShoeTemp = 0, ShoeHumi = 0, ShoePre = 0;
  }
  Serial.println(send_to_server(json_doc));

  //delay(2000);
}

void loop() {
    M5.update();
    if (M5.BtnA.wasPressed()) {
      debug_flag = 0;
      main_func();
    } else if (M5.BtnB.wasPressed()) {
      debug_flag = 1;
      main_func();
    }

  if (millis() - timer > update_interval_sec * 1000) {
    timer = millis();

    scan();

    main_func();
  }
}