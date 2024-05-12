import os
import requests
from dotenv import load_dotenv
from createdatasource import create_datasource
from createindex import create_index
from createskillset import create_skillset
from createindexer import create_indexer

# .envファイルから環境変数をロード
load_dotenv()

# 環境変数を取得
AZURE_SEARCH_SERVICE = os.getenv("AZURE_SEARCH_SERVICE")
AZURE_SEARCH_SERVICE_KEY = os.getenv("AZURE_SEARCH_SERVICE_KEY")
AZURE_STORAGE_ACCOUNT = os.getenv("AZURE_STORAGE_ACCOUNT")
AZURE_STORAGE_CONTAINER = os.getenv("AZURE_STORAGE_CONTAINER")
AZURE_STORAGE_KEY = os.getenv("AZURE_STORAGE_KEY")
AZURE_FUNCTIONS = os.getenv("AZURE_FUNCTIONS")

# データソースの作成
create_datasource(
    AZURE_SEARCH_SERVICE,
    AZURE_SEARCH_SERVICE_KEY,
    AZURE_STORAGE_ACCOUNT,
    AZURE_STORAGE_CONTAINER,
    AZURE_STORAGE_KEY
)

# インデックスの作成
create_index(AZURE_SEARCH_SERVICE, AZURE_SEARCH_SERVICE_KEY)

# スキルセットの作成
create_skillset(AZURE_SEARCH_SERVICE, AZURE_SEARCH_SERVICE_KEY, AZURE_FUNCTIONS)

# インデクサーの作成
create_indexer(AZURE_SEARCH_SERVICE, AZURE_SEARCH_SERVICE_KEY)
