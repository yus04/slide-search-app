import os
import requests
from dotenv import load_dotenv

# .envファイルから環境変数をロード
load_dotenv()

# 環境変数を取得
AI_SEARCH_SERVICE_NAME = os.getenv("AI_SEARCH_SERVICE_NAME")
AI_SEARCH_ADMIN_KEY = os.getenv("AI_SEARCH_ADMIN_KEY")
SHAREPOINT_ENDPOINT = os.getenv("SHAREPOINT_ENDPOINT")
APPLICATION_ID = os.getenv("APPLICATION_ID")
APPLICATION_SECRET = os.getenv("APPLICATION_SECRET")
TENANT_ID = os.getenv("TENANT_ID")

# エンドポイントURLと管理者キーを設定
endpoint_url = f"https://{AI_SEARCH_SERVICE_NAME}.search.windows.net/datasources?api-version=2023-10-01-Preview"

# リクエストヘッダーを設定
headers = {
    "Content-Type": "application/json",
    "api-key": AI_SEARCH_ADMIN_KEY
}

# リクエストボディを設定
payload = {
    "name": "sharepoint-datasource",
    "type": "sharepoint",
    "credentials": {
        "connectionString": f"SharePointOnlineEndpoint={SHAREPOINT_ENDPOINT};ApplicationId={APPLICATION_ID};ApplicationSecret={APPLICATION_SECRET};TenantId={TENANT_ID}"
    },
    "container": {
        "name": "defaultSiteLibrary"
    }
}

# リクエストを送信
response = requests.post(endpoint_url, json=payload, headers=headers)

# レスポンスを処理
if response.status_code == 201:
    print("データソースが作成されました。")
else:
    print(f"エラー: {response.status_code}, {response.text}")