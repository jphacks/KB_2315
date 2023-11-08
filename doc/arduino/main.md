# メインコードのざっくりとした説明

## Setup 関数

- M5.begin() と Serial.begin() で初期化

    ``` cpp
    M5.begin();
    Serial.begin(115200);
    ```

- json Exporter の初期化

    ``` cpp
    // リクエストに応じてJSON形式のデータを返すエンドポイントの設定
    server.on("/data", HTTP_GET, [](AsyncWebServerRequest *request) {
        char exporter_plain_json[1536];
        serializeJson(json_doc, exporter_plain_json, sizeof(exporter_plain_json));

        request->send(200, "application/json", exporter_plain_json);
    });

    // サーバーの開始
    server.begin();
    ```

## 標準設計

- 以下に標準的な設計例を示す
- 各変数の設定等は main_func() 関数に格納したため，以下のような記述で動作すると思われる。

    ``` cpp
    void loop () {
        if (millis() - timer > update_interval_sec * 1000) {
            timer = millis();

            // ここでセンサの値を取得，代入する
            // センサ取得は，センサのライブラリに依存する
            RoomTemp = roomsensor.getTemperature;
            RoomHumi = roomsensor.getHumidity;
            ShoeTemp = shoesensor.getTemperature;
            ShoeHumi = shoesensor.getHumidiry;

            main_func();
        }
    }
    ```
