# Arduino 版の簡単な説明

## include

### config.h

- デバイスやセンサの設定を記述する
- base_config.h コピーし，config.h として利用する
- 基本的に値をいじらなくても何とかなる
- センサの設定
  - それぞれ，温度と湿度の条件判定に利用する

    ``` cpp
    #define GAP_TEMP 1.0
    #define GAP_HUM 15.0
    ```

- デバイス IDID

  ``` cpp
  const int DEVICE_ID = 1;
  ```

### secret.h

- WiFi の接続情報など，機密情報を記述する
- base_secret.h コピーし，secret.h として利用する
- WiFi の接続設定（必須部分）

    ``` cpp
    #define WIFI_SSID ""
    #define WIFI_PASSWORD ""
    #define HOST_URL ""
    ```

- WiFi で固定IPアドレスを用いる際に設定する部分（任意）
- STATAIC_IP を 1 にする
- 以下の形式で，IPアドレス，ゲートウェイ，サブネットマスクをそれぞれ設定する

    ``` cpp
    #define STATIC_IP 0
    const IPAddress ip(192, 168, 10, 89);
    const IPAddress gateway(192, 168, 10, 1);
    const IPAddress subnet(255, 255, 255, 0);
    ```
