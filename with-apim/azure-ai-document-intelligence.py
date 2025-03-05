import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult

load_dotenv()

apim_base_url_for_ai_document_intelligence = os.getenv("APIM_BASE_URL_FOR_AI_DOCUMENT_INTELLIGENCE")
ai_document_intelligence_api_key = os.getenv("AI_DOCUMENT_INTELLIGENCE_API_KEY")
ocp_apim_subscription_key = os.getenv("OCP_APIM_SUBSCRIPTION_KEY")

# 以下のように AzureKeyCredential で設定した認証情報は、
# リクエスト時に Ocp-Apim-Subscription-Key ヘッダーとして付与される
credential = AzureKeyCredential(ai_document_intelligence_api_key)

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
        # APIM 認証用のサブスクリプションキー設定
        headers = {
            "Ocp-Apim-Subscription-Key-Added": ocp_apim_subscription_key
        }
    )

result: AnalyzeResult = poller.result()

for page in result.pages:
    if page.lines:
        for line_idx, line in enumerate(page.lines):
            if page.words:
                print(f"Line {line_idx} has content: '{line.content}'")
