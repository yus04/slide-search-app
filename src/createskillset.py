# import os
# import requests
# from dotenv import load_dotenv

# # .envファイルから環境変数をロード
# load_dotenv()

# # 環境変数を取得
# AZURE_SEARCH_SERVICE = os.getenv("AZURE_SEARCH_SERVICE")
# AZURE_SEARCH_SERVICE_KEY = os.getenv("AZURE_SEARCH_SERVICE_KEY")
# AZURE_FUNCTIONS = os.getenv("AZURE_FUNCTIONS")
# # AZURE_FUNCTIONS_KEY = os.getenv("AZURE_FUNCTIONS_KEY")

# # for debug
# print("AZURE_SEARCH_SERVICE:", AZURE_SEARCH_SERVICE)
# print("AZURE_SEARCH_SERVICE_KEY:", AZURE_SEARCH_SERVICE_KEY)
# print("AZURE_FUNCTIONS:", AZURE_FUNCTIONS)
# # for debug

# # エンドポイントURLと管理者キーを設定
# endpoint_url = f"https://{AZURE_SEARCH_SERVICE}.search.windows.net/skillsets/sharepoint-skillset?api-version=2023-10-01-Preview"

# # リクエストヘッダーを設定
# headers = {
#     "Content-Type": "application/json",
#     "api-key": AZURE_SEARCH_SERVICE_KEY
# }

# # リクエストボディを設定
# payload = {
#     "name": "slide-search-app-skillset",
#     "skills": [
#         {
#             "@odata.type": "#Microsoft.Skills.Vision.OcrSkill",
#             "name": "#1",
#             "description": None,
#             "context": "/document/normalized_images/*",
#             "textExtractionAlgorithm": None,
#             "lineEnding": "Space",
#             "defaultLanguageCode": "ja",
#             "detectOrientation": True,
#             "inputs": [
#                 {
#                     "name": "image",
#                     "source": "/document/normalized_images/*"
#                 }
#             ],
#             "outputs": [
#                 {
#                     "name": "text",
#                     "targetName": "text"
#                 }
#             ]
#         },
#         {
#             "@odata.type": "#Microsoft.Skills.Custom.WebApiSkill",
#             "name": "#2",
#             "description": None,
#             "context": "/document/normalized_images/*",
#             # "uri": f"https://${AZURE_FUNCTIONS}.azurewebsites.net/api/http_trigger?code=${AZURE_FUNCTIONS_KEY}",
#             "uri": f"https://${AZURE_FUNCTIONS}.azurewebsites.net/api/http_trigger",
#             "httpMethod": "post",
#             "timeout": "PT3M50S",
#             "batchSize": 1,
#             "degreeOfParallelism": 1,
#             "authResourceId": None,
#             "inputs": [
#                 {
#                     "name": "image_path",
#                     "source": "/document/metadata_storage_path"
#                 }
#             ],
#             "outputs": [
#                 {
#                     "name": "design_feature",
#                     "targetName": "design_feature"
#                 },
#                 {
#                     "name": "design_type",
#                     "targetName": "design_type"
#                 },
#                 {
#                     "name": "logo",
#                     "targetName": "logo"
#                 },
#                 {
#                     "name": "icon",
#                     "targetName": "icon"
#                 },
#                 {
#                     "name": "person",
#                     "targetName": "person"
#                 },
#                 {
#                     "name": "color",
#                     "targetName": "color"
#                 }
#             ],
#             "httpHeaders": {},
#             "authIdentity": None
#         }
#     ],
# }

# # リクエストを送信
# response = requests.put(endpoint_url, json=payload, headers=headers)

# # レスポンスを処理
# if response.status_code == 201:
#     print("スキルセットが作成されました。")
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
# AZURE_FUNCTIONS = os.getenv("AZURE_FUNCTIONS")
# # AZURE_FUNCTIONS_KEY = os.getenv("AZURE_FUNCTIONS_KEY")

# # for debug
# print("AZURE_SEARCH_SERVICE:", AZURE_SEARCH_SERVICE)
# print("AZURE_SEARCH_SERVICE_KEY:", AZURE_SEARCH_SERVICE_KEY)
# print("AZURE_FUNCTIONS:", AZURE_FUNCTIONS)
# # for debug

import requests

def create_skillset(azure_search_service: str, azure_search_service_key: str, azure_functions: str) -> None:
    # エンドポイントURLと管理者キーを設定
    endpoint_url = f"https://{azure_search_service}.search.windows.net/skillsets/slide-search-app-skillset?api-version=2023-10-01-Preview"

    # リクエストヘッダーを設定
    headers = {
        "Content-Type": "application/json",
        "api-key": azure_search_service_key
    }

    # リクエストボディを設定
    payload = {
        "name": "slide-search-app-skillset",
        "skills": [
            {
                "@odata.type": "#Microsoft.Skills.Vision.OcrSkill",
                "name": "#1",
                "description": None,
                "context": "/document/normalized_images/*",
                "textExtractionAlgorithm": None,
                "lineEnding": "Space",
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
                    }
                ]
            },
            {
                "@odata.type": "#Microsoft.Skills.Custom.WebApiSkill",
                "name": "#2",
                "description": None,
                "context": "/document/normalized_images/*",
                "uri": f"https://${AZURE_FUNCTIONS}.azurewebsites.net/api/http_trigger?code=${AZURE_FUNCTIONS_KEY}",
                # "uri": f"https://${azure_functions}.azurewebsites.net/api/http_trigger",
                "httpMethod": "post",
                "timeout": "PT3M50S",
                "batchSize": 1,
                "degreeOfParallelism": 1,
                "authResourceId": None,
                "inputs": [
                    {
                        "name": "image_path",
                        "source": "/document/metadata_storage_path"
                    }
                ],
                "outputs": [
                    {
                        "name": "design_feature",
                        "targetName": "design_feature"
                    },
                    {
                        "name": "design_type",
                        "targetName": "design_type"
                    },
                    {
                        "name": "logo",
                        "targetName": "logo"
                    },
                    {
                        "name": "icon",
                        "targetName": "icon"
                    },
                    {
                        "name": "person",
                        "targetName": "person"
                    },
                    {
                        "name": "color",
                        "targetName": "color"
                    }
                ],
                "httpHeaders": {},
                "authIdentity": None
            }
        ],
    }

    # リクエストを送信
    response = requests.put(endpoint_url, json=payload, headers=headers)

    # レスポンスを処理
    if response.status_code == 201:
        print("スキルセットが作成されました。")
    else:
        print(f"エラー: {response.status_code}, {response.text}")
        exit(1)
