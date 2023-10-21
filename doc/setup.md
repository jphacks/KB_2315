# 開発環境の設定方法

## [Rye](https://github.com/mitsuhiko/rye) を利用する場合

1. このリポジトリをクローンする
   `git clone git@github.com:jphacks/KB_2315.git`
   `cd KB_2315`
1. Rye を用いて Python 環境を用意する
   - `rye sync`

## Rye を利用しない場合

1. このリポジトリをクローンする
   `git clone git@github.com:jphacks/KB_2315.git`
   `cd KB_2315`
1. venv を用いて Python 環境を用意する
   - `python -m venv .venv`
1. 仮想環境を有効化する
   - Windows : `.venv\Scripts\activate.bat`
   - Linux/macOS : `source .venv/bin/activate`
1. 依存パッケージをインストールする
   - `python -m pip install -r requirements.lock -r requirements-dev.lock`
