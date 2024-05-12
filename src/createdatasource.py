# import os
# import requests
# from dotenv import load_dotenv

# # .envファイルから環境変数をロード
# load_dotenv()

# # 環境変数を取得
# AZURE_SEARCH_SERVICE = os.getenv("AZURE_SEARCH_SERVICE")
# AZURE_SEARCH_SERVICE_KEY = os.getenv("AZURE_SEARCH_SERVICE_KEY")
# AZURE_STORAGE_ACCOUNT = os.getenv("AZURE_STORAGE_ACCOUNT")
# AZURE_STORAGE_CONTAINER = os.getenv("AZURE_STORAGE_CONTAINER")
# AZURE_STORAGE_KEY = os.getenv("AZURE_STORAGE_KEY")

# # connectionString = f"DefaultEndpointsProtocol=https;AccountName=${AZURE_STORAGE_ACCOUNT};AccountKey=${AZURE_STORAGE_KEY};EndpointSuffix=core.windows.net"
# connectionString = f"DefaultEndpointsProtocol=https;AccountName={AZURE_STORAGE_ACCOUNT};AccountKey={AZURE_STORAGE_KEY};"

# # for debug
# print("AZURE_SEARCH_SERVICE:", AZURE_SEARCH_SERVICE)
# print("AZURE_SEARCH_SERVICE_KEY:", AZURE_SEARCH_SERVICE_KEY)
# print("AZURE_STORAGE_ACCOUNT:", AZURE_STORAGE_ACCOUNT)
# print("AZURE_STORAGE_CONTAINER:", AZURE_STORAGE_CONTAINER)
# print("AZURE_STORAGE_KEY:", AZURE_STORAGE_KEY)
# print("connectionString:", connectionString)
# # for debug

# # エンドポイントURLと管理者キーを設定
# endpoint_url = f"https://{AZURE_SEARCH_SERVICE}.search.windows.net/datasources?api-version=2023-10-01-Preview"

# # リクエストヘッダーを設定
# headers = {
#     "Content-Type": "application/json",
#     "api-key": AZURE_SEARCH_SERVICE_KEY
# }

# # リクエストボディを設定
# payload = {
#     "name": "slide-search-app-datasource",
#     "type": "azureblob",
#     "credentials": {
#         "connectionString": connectionString
#     },
#     "container": {
#         "name": AZURE_STORAGE_CONTAINER
#     }
# }

# # リクエストを送信
# response = requests.post(endpoint_url, json=payload, headers=headers)

# # レスポンスを処理
# if response.status_code == 201:
#     print("データソースが作成されました。")
# else:
#     print(f"エラー: {response.status_code}, {response.text}")

# import os
# import requests
# from dotenv import load_dotenv

# # .envファイルから環境変数をロード
# load_dotenv()

# # 環境変数を取得
# AZURE_SEARCH_SERVICE = os.getenv("AZURE_SEARCH_SERVICE")
# AZURE_SEARCH_SERVICE_KEY = os.getenv("AZURE_SEARCH_SERVICE_KEY")
# AZURE_STORAGE_ACCOUNT = os.getenv("AZURE_STORAGE_ACCOUNT")
# AZURE_STORAGE_CONTAINER = os.getenv("AZURE_STORAGE_CONTAINER")
# AZURE_STORAGE_KEY = os.getenv("AZURE_STORAGE_KEY")

# # connectionString = f"DefaultEndpointsProtocol=https;AccountName=${AZURE_STORAGE_ACCOUNT};AccountKey=${AZURE_STORAGE_KEY};EndpointSuffix=core.windows.net"
# connectionString = f"DefaultEndpointsProtocol=https;AccountName={AZURE_STORAGE_ACCOUNT};AccountKey={AZURE_STORAGE_KEY};"

# # for debug
# print("AZURE_SEARCH_SERVICE:", AZURE_SEARCH_SERVICE)
# print("AZURE_SEARCH_SERVICE_KEY:", AZURE_SEARCH_SERVICE_KEY)
# print("AZURE_STORAGE_ACCOUNT:", AZURE_STORAGE_ACCOUNT)
# print("AZURE_STORAGE_CONTAINER:", AZURE_STORAGE_CONTAINER)
# print("AZURE_STORAGE_KEY:", AZURE_STORAGE_KEY)
# print("connectionString:", connectionString)
# # for debug

import requests

def create_datasource(
        azure_search_service: str,
        azure_search_service_key: str,
        azure_storage_account: str,
        azure_storage_container: str,
        azure_storage_key: str
    ) -> None:
    # エンドポイントURLと管理者キーを設定
    endpoint_url = f"https://{azure_search_service}.search.windows.net/datasources?api-version=2023-10-01-Preview"

    # Blob Storage の接続文字列
    connectionString = f"DefaultEndpointsProtocol=https;AccountName={azure_storage_account};AccountKey={azure_storage_key};"

    # リクエストヘッダーを設定
    headers = {
        "Content-Type": "application/json",
        "api-key": azure_search_service_key
    }

    # リクエストボディを設定
    payload = {
        "name": "slide-search-app-datasource",
        "type": "azureblob",
        "credentials": {
            "connectionString": connectionString
        },
        "container": {
            "name": azure_storage_container
        }
    }

    # リクエストを送信
    response = requests.post(endpoint_url, json=payload, headers=headers)

    # レスポンスを処理
    if response.status_code == 201:
        print("データソースが作成されました。")
    else:
        print(f"エラー: {response.status_code}, {response.text}")
        exit(1)
