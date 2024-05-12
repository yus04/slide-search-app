import os
import requests
from dotenv import load_dotenv

# .envファイルから環境変数をロード
load_dotenv()

# 環境変数を取得
AI_SEARCH_SERVICE_NAME = os.getenv("AI_SEARCH_SERVICE_NAME")
AI_SEARCH_ADMIN_KEY = os.getenv("AI_SEARCH_ADMIN_KEY")
AOAI_ENDPOINT = os.getenv("AOAI_ENDPOINT")
AOAI_DEPLOYMENT_ID = os.getenv("AOAI_DEPLOYMENT_ID")
AOAI_API_KEY = os.getenv("AOAI_API_KEY")

# エンドポイントURLと管理者キーを設定
endpoint_url = f"https://{AI_SEARCH_SERVICE_NAME}.search.windows.net/skillsets/sharepoint-skillset?api-version=2023-10-01-Preview"

# リクエストヘッダーを設定
headers = {
    "Content-Type": "application/json",
    "api-key": AI_SEARCH_ADMIN_KEY
}

# リクエストボディを設定
payload = {
    "name": "sharepoint-skillset",
        "skills": [
        {
            "@odata.type": "#Microsoft.Skills.Vision.OcrSkill",
            "context": "/document/normalized_images/*",
            "defaultLanguageCode": "ja",
            "detectOrientation": True,
            "inputs": [
                {
                    "name": "image",
                    "source": "/document/normalized_images/*"
                }
            ],
            "outputs": [
                {
                    "name": "text",
                    "targetName": "text"
                },
                {
                    "name": "layoutText",
                    "targetName": "layoutText"
                }
            ]
        },
        {
            "@odata.type": "#Microsoft.Skills.Text.SplitSkill",
            "context": "/document/normalized_images/*",
            "textSplitMode": "pages",
            "maximumPageLength": 300,
            "pageOverlapLength": 50,
            "defaultLanguageCode": "ja",
            "inputs": [
                {
                    "name": "text",
                    "source": "/document/normalized_images/*/text"
                }
            ],
            "outputs": [
                {
                    "name": "textItems",
                    "targetName": "chunks"
                }
            ]
        },
        {
            "@odata.type": "#Microsoft.Skills.Text.AzureOpenAIEmbeddingSkill",
            "context": "/document/normalized_images/*/chunks/*",
            "resourceUri": AOAI_ENDPOINT,
            "deploymentId": AOAI_DEPLOYMENT_ID,
            "apiKey": AOAI_API_KEY,
            "inputs": [
                {
                    "name": "text",
                    "source": "/document/normalized_images/*/chunks/*"
                }
            ],
            "outputs": [
                {
                    "name": "embedding",
                    "targetName": "vector"
                }
            ]
        }
    ],
    "indexProjections": {
        "selectors": [
            {
                "targetIndexName": "sharepoint-index",
                "parentKeyFieldName": "parentKey",
                "sourceContext": "/document/normalized_images/*/chunks/*",
                "mappings": [
                    {
                        "name": "page",
                        "source": "/document/normalized_images/*/pageNumber"
                    },
                    {
                        "name": "text",
                        "source": "/document/normalized_images/*/chunks/*"
                    },
                    {
                        "name": "textVector",
                        "source": "/document/normalized_images/*/chunks/*/vector"
                    },
                    {
                        "name": "metadata_storage_path",
                        "source": "/document/metadata_storage_path"
                    },
                    {
                        "name": "metadata_storage_name",
                        "source": "/document/metadata_storage_name"
                    }
                ]
            }
        ],
        "parameters": {
            "projectionMode": "skipIndexingParentDocuments"
        }
    }
}

# リクエストを送信
response = requests.put(endpoint_url, json=payload, headers=headers)

# レスポンスを処理
if response.status_code == 201:
    print("スキルセットが作成されました。")
else:
    print(f"エラー: {response.status_code}, {response.text}")