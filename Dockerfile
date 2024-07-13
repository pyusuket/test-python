# ベースイメージとしてPython 3.10を使用
FROM python:3.10

# 作業ディレクトリを設定
WORKDIR /app

# 必要なシステムライブラリをインストール
RUN apt-get update && apt-get install -y \
  libpq-dev \
  gcc \
  python3-dev \
  && rm -rf /var/lib/apt/lists/*

# 必要なライブラリをインストールするためのrequirements.txtをコピー
COPY requirements.txt .

# ライブラリのインストール
RUN pip install --upgrade pip \
  && pip install -r requirements.txt

# Google Cloud SDKのインストール
RUN curl -sSL https://sdk.cloud.google.com | bash
ENV PATH $PATH:/root/google-cloud-sdk/bin

# プロジェクトファイルをコンテナにコピー
COPY . .

# 認証情報ファイルをコピー
COPY service_account_key.json /app/service_account_key.json

# ポート8000を開放
EXPOSE 8000

# コンテナ起動時に実行するコマンド（Django開発サーバーを起動）
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
