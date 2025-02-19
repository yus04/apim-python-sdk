import os
from dotenv import load_dotenv
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import AzureSearch
from azure.search.documents.indexes.models import SimpleField, SearchableField, SearchFieldDataType

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
        # 保存後、テキストに基づいて類似度検索を実行
        query = "青空"
        documents = vectorstore.similarity_search(query, k=3, search_type="similarity")
        print("検索結果:")
        for doc in documents:
            print(doc.page_content)
    finally:
        # 明示的にクライアントをクローズすることで __del__ 内での asyncio エラーを回避
        vectorstore.client.close()

if __name__ == '__main__':
    main()
