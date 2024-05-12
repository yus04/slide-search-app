import azure.functions as func
import logging
import json
import os
from openai import AzureOpenAI

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

AZURE_OPENAI_SERVICE = os.environ.get("AZURE_OPENAI_SERVICE")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
GPT_DEPLOYMENT = os.environ.get("GPT_DEPLOYMENT")
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
                あなたは企画書のデザインに関する特徴を分析する人です。
                以下の項目について分析し、指定された json 形式で出力してください。
                ただし、該当しない特徴については空文字で回答して下さい。

                ## 分析項目
                ・デザインの特徴 (30 文字程度)
                ・デザインの種類 (グラフの種類(棒、円、折れ線、散布図)、表、カレンダー、組織図)
                ・ロゴの企業名
                ・アイコンの種類
                ・有名人の名前
                ・色の種類

                ## 回答 json 形式
                {"design_feature":"","design_type":"","logo":"","icon":"","person":"","color":""}
            """},
            {"role":"user","content":[
                {
                    "type": "image_url",
                    "image_url": image_path
                }
            ]}
        ]

        response = openai_client.chat.completions.create(
            model=GPT_DEPLOYMENT,
            # response_format={"type":"json_object"}, 
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
            "design_feature": res_dict.get("design_feature", ""),
            "design_type": res_dict.get("design_type", ""),
            "logo": res_dict.get("logo", ""),
            "icon": res_dict.get("icon", ""),
            "person": res_dict.get("person", ""),
            "color": res_dict.get("color", "")
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


# import azure.functions as func
# import logging

# app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

# @app.route(route="http_trigger_backup")
# def http_trigger_backup(req: func.HttpRequest) -> func.HttpResponse:
#     logging.info('Python HTTP trigger function processed a request.')

#     name = req.params.get('name')
#     if not name:
#         try:
#             req_body = req.get_json()
#         except ValueError:
#             pass
#         else:
#             name = req_body.get('name')

#     if name:
#         return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
#     else:
#         return func.HttpResponse(
#              "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
#              status_code=200
#         )
