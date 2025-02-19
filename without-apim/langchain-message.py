import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# Azure OpenAI の認証情報を設定
LANGCHAIN_AOAI_ENDPOINT = os.getenv("LANGCHAIN_AOAI_ENDPOINT")
LANGCHAIN_AOAI_API_VERSION = os.getenv("LANGCHAIN_AOAI_API_VERSION")
LANGCHAIN_AOAI_DEPLOYMENT_NAME = os.getenv("LANGCHAIN_AOAI_DEPLOYMENT_NAME")
LANGCHAIN_AOAI_API_KEY = os.getenv("LANGCHAIN_AOAI_API_KEY")

# LangChain を通じて Azure OpenAI のチャットモデルを初期化
model = AzureChatOpenAI(
    azure_endpoint = LANGCHAIN_AOAI_ENDPOINT,
    openai_api_version = LANGCHAIN_AOAI_API_VERSION,
    deployment_name = LANGCHAIN_AOAI_DEPLOYMENT_NAME,
    openai_api_key = LANGCHAIN_AOAI_API_KEY,
    temperature = 0.7,
)

# 翻訳のためのチャットプロンプトテンプレートを作成
system_template = "Translate the following from English into {language}"
prompt_template = ChatPromptTemplate.from_messages(
    [("system", system_template), ("user", "{text}")]
)

# 翻訳用の入力を定義
input_data = {
    "language": "Japanese",
    "text": "Hello, how are you?"
}

# テンプレートを使用してプロンプトをフォーマット
formatted_prompt = prompt_template.invoke(input_data)

# フォーマットされたプロンプトを用いてモデルを呼び出す
response = model.invoke(formatted_prompt)
print("翻訳後：", response.content)
