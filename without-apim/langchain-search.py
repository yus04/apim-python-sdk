import os
from dotenv import load_dotenv
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import AzureSearch

def main():
    load_dotenv()

    # AOAI の埋め込みモデルの設定
    LANGCHAIN_AOAI_EMBEDDING_ENDPOINT = os.getenv("LANGCHAIN_AOAI_EMBEDDING_ENDPOINT")
    LANGCHAIN_AOAI_EMBEDDING_DEPLOYMENT = os.getenv("LANGCHAIN_AOAI_EMBEDDING_DEPLOYMENT")
    LANGCHAIN_AOAI_EMBEDDING_API_KEY = os.getenv("LANGCHAIN_AOAI_EMBEDDING_API_KEY")
    LANGCHAIN_AOAI_EMBEDDING_API_VERSION = os.getenv("LANGCHAIN_AOAI_EMBEDDING_API_VERSION")

    # Azure AI Search の認証情報を設定
    LANGCHAIN_AI_SEARCH_ENDPOINT = os.getenv("LANGCHAIN_AI_SEARCH_ENDPOINT")
    LANGCHAIN_AI_SEARCH_API_KEY = os.getenv("LANGCHAIN_AI_SEARCH_API_KEY")
    LANGCHAIN_AI_SEARCH_INDEX_NAME = os.getenv("LANGCHAIN_AI_SEARCH_INDEX_NAME")

    # 埋め込み関数の初期化
    embedding = AzureOpenAIEmbeddings(
        azure_endpoint = LANGCHAIN_AOAI_EMBEDDING_ENDPOINT,
        azure_deployment = LANGCHAIN_AOAI_EMBEDDING_DEPLOYMENT,
        api_key = LANGCHAIN_AOAI_EMBEDDING_API_KEY,
        api_version = LANGCHAIN_AOAI_EMBEDDING_API_VERSION
    )

    # LangChain の AzureSearch ベクトルストアラッパーを初期化
    vectorstore = AzureSearch(
        azure_search_endpoint = LANGCHAIN_AI_SEARCH_ENDPOINT,
        azure_search_key = LANGCHAIN_AI_SEARCH_API_KEY,
        index_name = LANGCHAIN_AI_SEARCH_INDEX_NAME,
        embedding_function = embedding.embed_query,
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
