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
                "sourceFieldName": "/document/normalized_images/0/design_feature",
                "targetFieldName": "design_feature"
            },
            {
                "sourceFieldName": "/document/normalized_images/0/design_type",
                "targetFieldName": "design_type"
            },
            {
                "sourceFieldName": "/document/normalized_images/0/logo",
                "targetFieldName": "logo"
            },
            {
                "sourceFieldName": "/document/normalized_images/0/icon",
                "targetFieldName": "icon"
                },
            {
                "sourceFieldName": "/document/normalized_images/0/person",
                "targetFieldName": "person"
            },
            {
                "sourceFieldName": "/document/normalized_images/0/color",
                "targetFieldName": "color"
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
