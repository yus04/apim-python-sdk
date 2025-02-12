import os
from dotenv import load_dotenv
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()

ai_search_service_name = os.getenv("AI_SEARCH_SERVICE_NAME")
ai_search_index_name = os.getenv("AI_SEARCH_INDEX_NAME")
ai_search_api_key = os.getenv("AI_SEARCH_API_KEY")
credential = AzureKeyCredential(ai_search_api_key)

# 以下を変更してください
search_text = ""

search_client = SearchClient(
    endpoint = f"https://{ai_search_service_name}.search.windows.net",
    index_name = ai_search_index_name,
    credential = credential
)

results = search_client.search(
    search_text = search_text
)

for result in results:
    print(result)
