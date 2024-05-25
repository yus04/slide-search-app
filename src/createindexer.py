import requests

def create_indexer(azure_search_service: str, azure_search_service_key: str) -> None:
    # エンドポイントURLと管理者キーを設定
    endpoint_url = f"https://{azure_search_service}.search.windows.net/indexers?api-version=2023-10-01-Preview"

    # リクエストヘッダーを設定
    headers = {
        "Content-Type": "application/json",
        "api-key": azure_search_service_key
    }

    # リクエストボディを設定
    payload = {
        "name": "slide-search-app-indexer",
        "dataSourceName": "slide-search-app-datasource",
        "skillsetName": "slide-search-app-skillset",
        "targetIndexName": "slide-search-app-index",
        "parameters": {
            "configuration": {
                "dataToExtract": "contentAndMetadata",
                "parsingMode": "default",
                "imageAction": "generateNormalizedImagePerPage",
                "allowSkillsetToReadFileData": True
            }
        },
        "fieldMappings": [],
        "outputFieldMappings": [
            {
                "sourceFieldName": "/document/normalized_images/0/text",
                "targetFieldName": "text"
            },
            {
                "sourceFieldName": "/document/normalized_images/0/explanation",
                "targetFieldName": "explanation"
            },
            {
                "sourceFieldName": "/document/normalized_images/0/illustration",
                "targetFieldName": "illustration"
            },
            {
                "sourceFieldName": "/document/normalized_images/0/photo",
                "targetFieldName": "photo"
            },
            {
                "sourceFieldName": "/document/normalized_images/0/design",
                "targetFieldName": "design"
                },
            {
                "sourceFieldName": "/document/normalized_images/0/logo",
                "targetFieldName": "logo"
            }
        ],
    }

    # リクエストを送信
    response = requests.post(endpoint_url, json=payload, headers=headers)

    # レスポンスを処理
    if response.status_code == 201:
        print("インデクサーが作成されました。")
    else:
        print(f"エラー: {response.status_code}, {response.text}")
        exit(1)
