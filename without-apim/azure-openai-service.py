import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

aoai_service_name = os.getenv("AOAI_SERVICE_NAME")
aoai_api_version = os.getenv("AOAI_API_VERSION")
aoai_api_key = os.getenv("AOAI_API_KEY")

# 以下を変更してください
model_deploy_name = ""
messages = [
    {"role": "system", "content": "あなたは役に立つアシスタントです。"},
    {"role": "user", "content": "Azure OpenAI Service とは何ですか？"},
]

aoai_client = AzureOpenAI(
    azure_endpoint = f"https://{aoai_service_name}.openai.azure.com",
    api_version = aoai_api_version,
    api_key = aoai_api_key
)

response = aoai_client.chat.completions.create(
    model = model_deploy_name,
    messages = messages
)

print(response.choices[0].message.content)
