import os
import requests
import argparse
from dotenv import load_dotenv
from uploadcontent import upload_content
from createdatasource import create_datasource
from createindex import create_index
from createskillset import create_skillset
from createindexer import create_indexer

# .envファイルから環境変数をロード
load_dotenv()

# コマンドライン引数を解析
parser = argparse.ArgumentParser()
parser.add_argument("--azureaiserviceskey", required = True)
parser.add_argument("--containername", required = True)
args = parser.parse_args()

# 環境変数を取得
AZURE_SEARCH_SERVICE = os.getenv("AZURE_SEARCH_SERVICE")
AZURE_SEARCH_SERVICE_KEY = os.getenv("AZURE_SEARCH_SERVICE_KEY")
AZURE_STORAGE_ACCOUNT = os.getenv("AZURE_STORAGE_ACCOUNT")
AZURE_STORAGE_CONTAINER = os.getenv("AZURE_STORAGE_CONTAINER")
AZURE_STORAGE_KEY = os.getenv("AZURE_STORAGE_KEY")
AZURE_FUNCTIONS = os.getenv("AZURE_FUNCTIONS")
AZURE_AI_SERVICES_KEY = args.azureaiserviceskey
CONTAINER_NAME = args.containername

# 画像のアップロード
upload_content(AZURE_STORAGE_ACCOUNT, AZURE_STORAGE_KEY, CONTAINER_NAME)

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
create_skillset(AZURE_SEARCH_SERVICE, AZURE_SEARCH_SERVICE_KEY, AZURE_FUNCTIONS, AZURE_AI_SERVICES_KEY)

# インデクサーの作成
create_indexer(AZURE_SEARCH_SERVICE, AZURE_SEARCH_SERVICE_KEY)
