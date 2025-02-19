import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult

load_dotenv()

apim_base_url_for_ai_document_intelligence = os.getenv("APIM_BASE_URL_FOR_AI_DOCUMENT_INTELLIGENCE")
ai_document_intelligence_api_key = os.getenv("AI_DOCUMENT_INTELLIGENCE_API_KEY")
ocp_apim_subscription_key = os.getenv("OCP_APIM_SUBSCRIPTION_KEY")

# 通常は以下のように AzureKeyCredential を使って認証情報を設定
# credential = AzureKeyCredential(ai_document_intelligence_api_key)

# ただし、APIM を経由する場合は以下のように AzureKeyCredential を使って認証情報を設定
credential = AzureKeyCredential(ocp_apim_subscription_key)

# 以下を変更してください
document_name = "sample.pdf"

current_dir = os.path.dirname(os.path.abspath(__file__))
path_to_sample_documents = os.path.join(current_dir, "..", "data", document_name)

ai_document_intelligence_client = DocumentIntelligenceClient(
    apim_base_url_for_ai_document_intelligence,
    credential
)

with open(path_to_sample_documents, "rb") as f:
    poller = ai_document_intelligence_client.begin_analyze_document(
        "prebuilt-layout",
        body = f,
        # 以下のようにヘッダーを指定することはできない (credential で上書きされる)
        # headers = {
        #     "Ocp-Apim-Subscription-Key": ocp_apim_subscription_key
        # }
    )

result: AnalyzeResult = poller.result()

for page in result.pages:
    if page.lines:
        for line_idx, line in enumerate(page.lines):
            if page.words:
                print(f"Line {line_idx} has content: '{line.content}'")
