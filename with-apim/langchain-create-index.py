import os
from dotenv import load_dotenv
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import AzureSearch

def main():
    load_dotenv()

    # AOAI の埋め込みモデルの設定
    APIM_BASE_URL_FOR_LANGCHAIN_AOAI_EMBEDDING_ENDPOINT = os.getenv("APIM_BASE_URL_FOR_LANGCHAIN_AOAI_EMBEDDING_ENDPOINT")
    LANGCHAIN_AOAI_EMBEDDING_DEPLOYMENT = os.getenv("LANGCHAIN_AOAI_EMBEDDING_DEPLOYMENT")
    LANGCHAIN_AOAI_EMBEDDING_API_KEY = os.getenv("LANGCHAIN_AOAI_EMBEDDING_API_KEY")
    LANGCHAIN_AOAI_EMBEDDING_API_VERSION = os.getenv("LANGCHAIN_AOAI_EMBEDDING_API_VERSION")

    # Azure AI Search の認証情報を設定
    APIM_BASE_URL_FOR_LANGCHAIN_AI_SEARCH_ENDPOINT = os.getenv("APIM_BASE_URL_FOR_LANGCHAIN_AI_SEARCH_ENDPOINT")
    LANGCHAIN_AI_SEARCH_API_KEY = os.getenv("LANGCHAIN_AI_SEARCH_API_KEY")
    LANGCHAIN_AI_SEARCH_INDEX_NAME = os.getenv("LANGCHAIN_AI_SEARCH_INDEX_NAME")

    # APIM のサブスクリプションキー
    OCP_APIM_SUBSCRIPTION_KEY = os.getenv("OCP_APIM_SUBSCRIPTION_KEY")

    # 埋め込み関数の初期化
    embedding = AzureOpenAIEmbeddings(
        azure_endpoint = APIM_BASE_URL_FOR_LANGCHAIN_AOAI_EMBEDDING_ENDPOINT,
        azure_deployment = LANGCHAIN_AOAI_EMBEDDING_DEPLOYMENT,
        api_key = LANGCHAIN_AOAI_EMBEDDING_API_KEY,
        api_version = LANGCHAIN_AOAI_EMBEDDING_API_VERSION,
        default_headers = {
            "Ocp-Apim-Subscription-Key": OCP_APIM_SUBSCRIPTION_KEY
        }
    )

    # LangChain の AzureSearch ベクトルストアラッパーを初期化
    vectorstore = AzureSearch(
        azure_search_endpoint = APIM_BASE_URL_FOR_LANGCHAIN_AI_SEARCH_ENDPOINT,
        azure_search_key = LANGCHAIN_AI_SEARCH_API_KEY,
        index_name = LANGCHAIN_AI_SEARCH_INDEX_NAME,
        embedding_function = embedding.embed_query
        # 以下は正しいサブスクリプションキーを使用するための追加のオプションではないので利用できず (0.3.19 時点)
        # additional_search_client_options = {
        #     "headers": {
        #         "Ocp-Apim-Subscription-Key": OCP_APIM_SUBSCRIPTION_KEY
        #     }
        # }
    )
    try:
        # 保存するテキストとメタデータを定義
        texts = [
            "青空の下で広がる大地",
            "青い海と空の境界が溶ける風景",
            "青い夜空に輝く星々"
        ]
        metadatas = [
            {"title": "Document A", "source": "example"},
            {"title": "Document B", "source": "example"},
            {"title": "Document C", "source": "example"}
        ]

        # vectorstore にテキスト（とメタデータ）を保存
        result_ids = vectorstore.add_texts(texts, metadatas)
        print("保存されたドキュメントの ID:")
        print(result_ids)

    finally:
        # 明示的にクライアントをクローズすることで __del__ 内での asyncio エラーを回避
        vectorstore.client.close()

if __name__ == '__main__':
    main()
