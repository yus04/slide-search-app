from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import os

def upload_content(azure_storage_account: str, azure_storage_key: str, container_name: str):

    # Azure Storage アカウントの接続文字列
    connection_string = f"DefaultEndpointsProtocol=https;AccountName={azure_storage_account};AccountKey={azure_storage_key};"

    # Blob Service Client の作成
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # コンテナが存在しない場合は作成する
    container_client = blob_service_client.get_container_client(container_name)

    # アップロードする画像ファイルがあるディレクトリパス
    directory_path = "../data/"

    # ディレクトリ内のすべてのファイルを取得してアップロード
    for filename in os.listdir(directory_path):
        if filename.endswith(".jpg"):
            # ローカルのファイルパス
            local_file_path = os.path.join(directory_path, filename)
            
            # Blob に対応するクライアントを作成
            blob_client = blob_service_client.get_blob_client(container = container_name, blob = filename)
            
            # ファイルを Blob にアップロード
            with open(local_file_path, "rb") as data:
                blob_client.upload_blob(data, overwrite=True)
            
            print(f"{filename} uploaded successfully.")
