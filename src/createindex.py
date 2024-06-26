import requests

def create_index(azure_search_service: str, azure_search_service_key: str) -> None:
    # エンドポイントURLと管理者キーを設定
    endpoint_url = f"https://{azure_search_service}.search.windows.net/indexes?api-version=2023-10-01-Preview"

    # リクエストヘッダーを設定
    headers = {
        "Content-Type": "application/json",
        "api-key": azure_search_service_key
    }

    # リクエストボディを設定
    payload = {
        "name": "slide-search-app-index",
        "fields": [
            {
                "name": "id",
                "type": "Edm.String",
                "searchable": False,
                "filterable": False,
                "retrievable": True,
                "sortable": False,
                "facetable": False,
                "key": True,
                "indexAnalyzer": None,
                "searchAnalyzer": None,
                "analyzer": None,
                "normalizer": None,
                "dimensions": None,
                "vectorSearchProfile": None,
                "synonymMaps": []
            },
            {
                "name": "text",
                "type": "Edm.String",
                "searchable": True,
                "filterable": False,
                "retrievable": True,
                "sortable": False,
                "facetable": False,
                "key": False,
                "indexAnalyzer": None,
                "searchAnalyzer": None,
                "analyzer": "ja.lucene",
                "normalizer": None,
                "dimensions": None,
                "vectorSearchProfile": None,
                "synonymMaps": []
            },
            {
                "name": "explanation",
                "type": "Edm.String",
                "searchable": True,
                "filterable": True,
                "retrievable": True,
                "sortable": False,
                "facetable": False,
                "key": False,
                "indexAnalyzer": None,
                "searchAnalyzer": None,
                "analyzer": "ja.lucene",
                "normalizer": None,
                "dimensions": None,
                "vectorSearchProfile": None,
                "synonymMaps": []
            },
            {
                "name": "illustration",
                "type": "Edm.String",
                "searchable": True,
                "filterable": True,
                "retrievable": True,
                "sortable": False,
                "facetable": False,
                "key": False,
                "indexAnalyzer": None,
                "searchAnalyzer": None,
                "analyzer": "ja.lucene",
                "normalizer": None,
                "dimensions": None,
                "vectorSearchProfile": None,
                "synonymMaps": []
            },
            {
                "name": "photo",
                "type": "Edm.String",
                "searchable": True,
                "filterable": True,
                "retrievable": True,
                "sortable": False,
                "facetable": False,
                "key": False,
                "indexAnalyzer": None,
                "searchAnalyzer": None,
                "analyzer": "ja.lucene",
                "normalizer": None,
                "dimensions": None,
                "vectorSearchProfile": None,
                "synonymMaps": []
            },
            {
                "name": "design",
                "type": "Edm.String",
                "searchable": True,
                "filterable": True,
                "retrievable": True,
                "sortable": False,
                "facetable": False,
                "key": False,
                "indexAnalyzer": None,
                "searchAnalyzer": None,
                "analyzer": "ja.lucene",
                "normalizer": None,
                "dimensions": None,
                "vectorSearchProfile": None,
                "synonymMaps": []
            },
            {
                "name": "logo",
                "type": "Edm.String",
                "searchable": True,
                "filterable": True,
                "retrievable": True,
                "sortable": False,
                "facetable": False,
                "key": False,
                "indexAnalyzer": None,
                "searchAnalyzer": None,
                "analyzer": "ja.lucene",
                "normalizer": None,
                "dimensions": None,
                "vectorSearchProfile": None,
                "synonymMaps": []
            },
            {
                "name": "metadata_storage_name",
                "type": "Edm.String",
                "searchable": False,
                "filterable": False,
                "retrievable": True,
                "sortable": False,
                "facetable": False,
                "key": False,
                "indexAnalyzer": None,
                "searchAnalyzer": None,
                "analyzer": None,
                "normalizer": None,
                "dimensions": None,
                "vectorSearchProfile": None,
                "synonymMaps": []
            },
            {
                "name": "metadata_storage_path",
                "type": "Edm.String",
                "searchable": False,
                "filterable": False,
                "retrievable": True,
                "sortable": False,
                "facetable": False,
                "key": False,
                "indexAnalyzer": None,
                "searchAnalyzer": None,
                "analyzer": None,
                "normalizer": None,
                "dimensions": None,
                "vectorSearchProfile": None,
                "synonymMaps": []
            },
            {
                "name": "metadata_storage_last_modified",
                "type": "Edm.String",
                "searchable": False,
                "filterable": False,
                "retrievable": True,
                "sortable": False,
                "facetable": False,
                "key": False,
                "indexAnalyzer": None,
                "searchAnalyzer": None,
                "analyzer": None,
                "normalizer": None,
                "dimensions": None,
                "vectorSearchProfile": None,
                "synonymMaps": []
            }
        ],
        "similarity": {"@odata.type": "#Microsoft.Azure.Search.BM25Similarity"}
    }

    # リクエストを送信
    response = requests.post(endpoint_url, json=payload, headers=headers)

    # レスポンスを処理
    if response.status_code == 201:
        print("インデックスが作成されました。")
    else:
        print(f"エラー: {response.status_code}, {response.text}")
        exit(1)
