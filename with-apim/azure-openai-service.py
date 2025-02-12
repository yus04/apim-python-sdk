import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv()

apim_base_url_for_aoai = os.getenv("APIM_BASE_URL_FOR_AOAI")
aoai_api_version = os.getenv("AOAI_API_VERSION")
aoai_api_key = os.getenv("AOAI_API_KEY")
ocp_apim_subscription_key = os.getenv("OCP_APIM_SUBSCRIPTION_KEY")

# 以下を変更してください
model_deploy_name = ""
messages = [
    {"role": "system", "content": "あなたは役に立つアシスタントです。"},
    {"role": "user", "content": "Azure OpenAI Service とは何ですか？"},
]

aoai_client = AzureOpenAI(
    azure_endpoint = apim_base_url_for_aoai,
    api_version = aoai_api_version,
    api_key = aoai_api_key
)

response = aoai_client.chat.completions.create(
    model = model_deploy_name,
    messages = messages,
    extra_headers = {
        "Ocp-Apim-Subscription-Key": ocp_apim_subscription_key
    }
)

print(response.choices[0].message.content)
