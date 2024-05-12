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
endpoint_url = f"https://{AI_SEARCH_SERVICE_NAME}.search.windows.net/indexes?api-version=2023-10-01-Preview"

# リクエストヘッダーを設定
headers = {
    "Content-Type": "application/json",
    "api-key": AI_SEARCH_ADMIN_KEY
}

# リクエストボディを設定
payload = {
    "name": "sharepoint-index",
    "fields": [
        {"name": "id", "type": "Edm.String", "key": True, "searchable": True, "filterable": False, "sortable": False, "facetable": False, "analyzer": "keyword"},
        {"name": "parentKey", "type": "Edm.String", "searchable": False, "filterable": True, "sortable": False, "facetable": False},
        {"name": "metadata_storage_path", "type": "Edm.String", "searchable": False, "filterable": True, "sortable": False, "facetable": False},
        {"name": "metadata_storage_name", "type": "Edm.String", "searchable": False, "filterable": True, "sortable": False, "facetable": False},
        {"name": "page", "type": "Edm.Int32", "searchable": False, "filterable": False, "sortable": True, "facetable": False},
        {"name": "text", "type": "Edm.String", "searchable": True, "filterable": False, "sortable": False, "facetable": False, "analyzer": "ja.microsoft"},
        {"name": "textVector", "type": "Collection(Edm.Single)", "searchable": True, "dimensions": 1536, "vectorSearchProfile": "vectorProfile"}
    ],
    "vectorSearch": {
        "algorithms": [
            {"name": "hnsw", "kind": "hnsw", "hnswParameters": {"m": 4, "efConstruction": 400, "efSearch": 500, "metric": "cosine"}}
        ],
        "vectorizers": [
            {"name": "azureOpenAI", "kind": "azureOpenAI", "azureOpenAIParameters": {"resourceUri": AOAI_ENDPOINT, "deploymentId": AOAI_DEPLOYMENT_ID, "apiKey": AOAI_API_KEY}}
        ],
        "profiles": [
            {"name": "vectorProfile", "algorithm": "hnsw", "vectorizer": "azureOpenAI"}
        ]
    },
    "similarity": {"@odata.type": "#Microsoft.Azure.Search.BM25Similarity", "k1": 1.2, "b": 0.75}
}

# リクエストを送信
response = requests.post(endpoint_url, json=payload, headers=headers)

# レスポンスを処理
if response.status_code == 201:
    print("インデックスが作成されました。")
else:
    print(f"エラー: {response.status_code}, {response.text}")