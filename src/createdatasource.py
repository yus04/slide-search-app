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
