#!/bin/bash

echo ""
echo "Loading azd .env file from current environment"
echo ""

# config.json ファイルのパス
config_file="./.azure/config.json"

# config.json ファイルが存在するか確認
if [ -f "$config_file" ]; then
    # defaultEnvironment の値を jq を使って取得
    default_environment=$(jq -r '.defaultEnvironment' "$config_file")
else
    echo "エラー: config.json ファイルが見つかりません。"
    exit 1
fi

# .env ファイルのパス
env_file="./.azure/$default_environment/.env"

# .env ファイルが存在するか確認
if [ -f "$env_file" ]; then
    # .env ファイルから各行を読み込んで環境変数として設定
    while IFS='=' read -r key value; do
        # 空行やコメント行は無視
        if [[ $key && $key != "#"* ]]; then
            # 環境変数を設定
            value=$(sed 's/^"\(.*\)"$/\1/' <<< $value)
            export $key=$value
        fi
    done < "$env_file"
else
    echo "エラー: .env ファイルが見つかりません。"
    exit 1
fi

# 必要なパッケージを requirements.txt からインストールする
echo 'Installing required packages...'
python -m pip install -r ./src/requirements.txt

# Azure AI Search のデータソース、インデックス、スキルセット、インデクサーの作成
echo 'Setup AI Search...'
python './src/setupaisearch.py'

# # データソースを作成するスクリプトを実行する
# echo 'Creating datasource...'
# python ./src/create-datasource.py

# # インデックスを作成するスクリプトを実行する
# echo 'Creating index...'
# python ./src/create-index.py

# # スキルセットを作成するスクリプトを実行する
# echo 'Creating skillset...'
# python ./src/create-skillset.py

# # インデクサを作成するスクリプトを実行する
# echo 'Creating indexer...'
# python ./src/create-indexer.py
