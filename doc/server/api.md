# API ドキュメント

## /api/line

- line API との通信用

### /api/line/callback

- line API から受け取った内容をもとに，イベント処理を行う
- カルーセルや返信などは，内容に応じて分岐させている

## /api/sensor

- Arduino などのエッジデバイスからのデータを受け取る

### /api/sensor POST

- Arduino から Json でデータを受け取る
    例：

    ```json
    {
        "device_id": 1, // (デバイスID)[../arduino/include.md#config.h]
        "session_id": "1a2b3c-...", // セッションID: UUID
        "external_temperature": 20.0, // 外気温度
        "external_humidity": 20.0,// 外気湿度
        "interlnal_temperature": 20.0, // 靴内温度
        "interlnal_humidity": 20.0,// 靴内湿度
        "drying": 0, // 乾燥状態: true / false
    }
    
    ```

""

## /api/session

- セッション発行用API
  - エッジデバイスからの要求を想定
  - セッションIDを発行し，Lineに靴の乾燥の旨を通知
  - `/api/session/?device_id=1`

## /api/shoe

- 靴検索用API
  - 靴のid と靴の名前（部分一致）で可能
  - `/api/shoe/?id=1?name=靴`
