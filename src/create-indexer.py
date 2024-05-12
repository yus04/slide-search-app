import os
import requests
from dotenv import load_dotenv

# .envファイルから環境変数をロード
load_dotenv()

# 環境変数を取得
AI_SEARCH_SERVICE_NAME = os.getenv("AI_SEARCH_SERVICE_NAME")
AI_SEARCH_ADMIN_KEY = os.getenv("AI_SEARCH_ADMIN_KEY")

# エンドポイントURLと管理者キーを設定
endpoint_url = f"https://{AI_SEARCH_SERVICE_NAME}.search.windows.net/indexers?api-version=2023-10-01-Preview"

# リクエストヘッダーを設定
headers = {
    "Content-Type": "application/json",
    "api-key": AI_SEARCH_ADMIN_KEY
}

# リクエストボディを設定
payload = {
    "name": "sharepoint-indexer",
    "dataSourceName": "sharepoint-datasource",
    "skillsetName": "sharepoint-skillset",
    "targetIndexName": "sharepoint-index",
    "parameters": {
        "configuration": {
            "dataToExtract": "contentAndMetadata",
            "parsingMode": "default",
            "imageAction": "generateNormalizedImagePerPage",
            "allowSkillsetToReadFileData": True
        }
    }
}

# リクエストを送信
response = requests.post(endpoint_url, json=payload, headers=headers)

# レスポンスを処理
if response.status_code == 201:
    print("インデクサーが作成されました。")
else:
    print(f"エラー: {response.status_code}, {response.text}")