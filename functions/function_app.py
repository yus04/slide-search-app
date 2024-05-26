import azure.functions as func
import logging
import json
import os
from openai import AzureOpenAI

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

AZURE_OPENAI_SERVICE = os.environ.get("AZURE_OPENAI_SERVICE")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_DEPLOYMENT = os.environ.get("AZURE_OPENAI_DEPLOYMENT")
AZURE_OPENAI_TOKEN = os.environ.get("AZURE_OPENAI_TOKEN")

openai_client = AzureOpenAI(
    azure_endpoint = f"https://{AZURE_OPENAI_SERVICE}.openai.azure.com",
    api_version=AZURE_OPENAI_API_VERSION,
    api_key = AZURE_OPENAI_TOKEN
)


@app.route(route="http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    input_values = req_body.get('values', [])
    output_values = []

    for input_value in input_values:
        image_path = input_value["data"]["image_path"]

        messages = [
            {"role":"system","content":"""
            あなたはプレゼンテーション資料に含まれるものを様々な項目に対して特定する人です。
            以下の分析項目について調査し、指定された json 形式で出力してください。
            資料に含まれるデザインの種類に関しては、デザインの種類の詳細の中から選択してください。
            ただし、該当しない項目については空文字で回答し、該当する項目が複数ある場合は空白スペース区切りで回答して下さい。

            ## 分析項目
            ・資料の説明 (50 文字程度)
            ・資料に含まれているイラスト
            ・資料に含まれている写真にある物
            ・資料に含まれているデザインの種類
            ・資料に含まれているロゴの企業名

            ## デザインの種類の詳細
            ・グラフ (棒、円、折れ線、散布図)
            ・表
            ・リスト
            ・階層図
            ・概念図
            ・カレンダー
            ・ロードマップ
            ・業務フロー図
            ・システム図
            ・ダイアグラム
            ・プロセスマップ

            ## 回答 json 形式
            {"explanation":"","illustration":"","photo":"","design":"","logo":""}
            """},
            {"role":"user","content":[
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_path
                    }
                }
            ]}
        ]

        response = openai_client.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=messages,
            temperature=0.0,
            max_tokens=1000,
            n=1
        )

        res_str = response.choices[0].message.content

        try:
            res_dict = json.loads(res_str)
        except ValueError:
            res_dict = {}

        data = {
            "explanation": res_dict.get("explanation", ""),
            "illustration": res_dict.get("illustration", ""),
            "photo": res_dict.get("photo", ""),
            "design": res_dict.get("design", ""),
            "logo": res_dict.get("logo", "")
        }

        output_value = {}
        output_value["recordId"] = input_value["recordId"]
        output_value["data"] = data
        output_value["errors"] = []
        output_value["warnings"] = []
        output_values.append(output_value)

    return func.HttpResponse(
        body=json.dumps({"values": output_values}),
        status_code=200,
        mimetype="application/json"
    )
