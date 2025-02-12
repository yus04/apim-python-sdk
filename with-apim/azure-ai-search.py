import os
from dotenv import load_dotenv
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

load_dotenv()

apim_base_url_for_ai_search = os.getenv("APIM_BASE_URL_FOR_AI_SEARCH")
ai_search_index_name = os.getenv("AI_SEARCH_INDEX_NAME")
ai_search_api_key = os.getenv("AI_SEARCH_API_KEY")
ocp_apim_subscription_key = os.getenv("OCP_APIM_SUBSCRIPTION_KEY")
credential = AzureKeyCredential(ai_search_api_key)

# 以下を変更してください
search_text = ""

search_client = SearchClient(
    endpoint = apim_base_url_for_ai_search,
    index_name = ai_search_index_name,
    credential = credential
)

results = search_client.search(
    search_text = search_text,
    headers = {
        "Ocp-Apim-Subscription-Key": ocp_apim_subscription_key
    }
)

for result in results:
    print(result)
