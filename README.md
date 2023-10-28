# Title「革靴メンテナンス/自動bot」

[![IMAGE ALT TEXT HERE](https://jphacks.com/wp-content/uploads/2023/07/JPHACKS2023_ogp.png)](https://www.youtube.com/watch?v=yYRQEdfGjEg)

## 製品概要

* 革靴のメンテナンス/革靴にシューズキーパを入れるタイミング迷っているあなた、革靴を複数持っているあなた、

### 背景(製品開発のきっかけ、課題等）

* 革靴を愛してやまない人々の悩み：革靴の中の匂いを自然に解消したいけど、革靴の型を崩したくない。こんな悩みを持った人はおおいと思います。
* 革靴を愛してやまない人々の悩み：革靴を複数持っているけど、それぞれ把握できない悩み（匂い、置き場所、革の状態）を解消したい。

### 製品説明（具体的な製品の説明）

### 特長

#### 1. 特長1： 「仕事で頑張った脚の臭い × 革靴の型が崩れる」　を解消！！

#### 2. 特長2： 革靴を履いた日の記録・データ化可能

#### 3. 特長3： 

### 解決出来ること

* 革靴の匂いを自然に解消できる
* 革靴の型を崩さない
* 革靴を履いた日を把握できる
*

### 今後の展望

/　革靴の整理・アプリケーション化
/  100人分ビジネスマンの革靴8時間分湿度取得
/  データ可視化(Webserverがjsonに書き出してJypterNotebookでデータ可視化予定)
/ 各SNSへの拡大（今後、Slack, WhatsApp, Discord)
* ビジネス企業との連携

### 注力したこと（こだわり等）

* 「革靴本来の匂い * 型を崩さない」の両方を実現できる点
* 「革靴の状態を把握」できる点

## 開発技術

[![My Skills](https://skillicons.dev/icons?i=arduino,cpp,docker,fastapi,git,github,githubactions,py)](https://skillicons.dev)

### 活用した技術

#### API・データ

* [LINE Message API](https://developers.line.biz/ja/docs/messaging-api/line-bot-sdk/)

#### フレームワーク・ライブラリ・モジュール

* マイコン
  * [PlatformIO](https://platformio.org)
  * [Arduino](https://www.arduino.cc)
* サーバ
  * [FastAPI](https://fastapi.tiangolo.com)
* デプロイ
  * [Docker・Compose](https://www.docker.com)
  
#### デバイス

* マイコン
  * [ESP32](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/hw-reference/esp32/get-started-devkitc.html)
  * <img src=./doc/image/esp32.jpg width="300px">
  * [M5Core2](https://docs.m5stack.com/en/core/core2)
  * <img src=./doc/image/m5core2.webp width="300px">
* センサ
  * [DHT22（温湿度センサ）](http://www.aosong.com/en/products-22.html)
  * <img src=./doc/image/AM2302.jpg width="300px">
* アクチュエータ
  * [Motor Control Shield](https://www.waveshare.com/motor-control-shield.htm)
  * <img src=./doc/image/mcs.jpg width="300px">

### 独自技術

#### ハッカソンで開発した独自機能・技術

* センサ情報をリアルタイムで出力して，時系列としてCSV / Excel で分析できるようにした
* 靴の状態に応じて，換気を行う点

#### 製品に取り入れた研究内容（データ・ソフトウェアなど）（※アカデミック部門の場合のみ提出必須）

* 特になし
