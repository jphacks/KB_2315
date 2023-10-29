# 革靴メンテなんです

[![IMAGE ALT TEXT HERE](https://jphacks.com/wp-content/uploads/2023/07/JPHACKS2023_ogp.png)](https://www.youtube.com/watch?v=yYRQEdfGjEg)

## 製品概要

### leather shoes × Tech

革靴メンテなんです！!は革靴手入れ支援アプリです。家から帰ってきてシューズキーパーを入れるタイミングを適切に指示、誘導してくれるので、靴本来の匂いと革靴の型が変化しないを実現します。このアプリがあれば初心者でも気軽に靴をいい状態に維持できます。

### 背景(製品開発のきっかけ、課題等）

開発メンバーは３人とも学部、修士、博士の最終学年で周りはビジネスマンの方々も多い共通点がありました。

* 「革靴の革の匂いと型を崩さない大人の履き方に憧れる！！」（革靴大好き）
* 「エンジニアは革靴履かないし縁もゆかりもないですし....」(革靴初心者)
* このように各学位生活の中で、革靴に対する手入れをやる人、やらない人の意識の差が激しいことがわかってきました。

#### 革靴メンテなんですはそんな経験者と初心者をつなげます

* 革靴のメンテナンス/革靴にシューズキーパを入れるタイミング迷っているあなた、革靴を複数持っている方々へ。

### 製品説明（具体的な製品の説明）

### 特長

#### 1. 特長1：匂い × 革靴の型を崩さない

#### 2. 特長2：革靴の状態を把握できる


### 解決出来ること

* 革靴の匂いを自然に解消できる
* 革靴の型を崩さない
* 革靴を履いた日を把握できる
*

### 今後の展望
/　革靴の整理・アプリケーション化
/  100人分ビジネスマンの革靴8時間分湿度取得
/  データ可視化（サーバ側で収集したデータを用いて，靴や靴のユーザの状態を管理）
/ 各SNSへの拡大（今後、Slack, WhatsApp, Discord)
/ 企業との連携（ビックデータ・統計）

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
  * [ESP32 Devkit C](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/hw-reference/esp32/get-started-devkitc.html)
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
* 内外の気温・湿度変化を情報として可視化して通知できる機能
* 匂いの原因となる雑菌を繁殖させない且つ革靴本来の型を維持できる技術

#### ビジネスモデル・収益化
1. 革靴コミュニティからの認知・革靴業界へのデータ分析協賛
  * [靴磨き選手権](https://web.hh-online.jp/hankyu-mens/contents/h/shoeshine/)

2. アプリケーション化

3. evidence収集
