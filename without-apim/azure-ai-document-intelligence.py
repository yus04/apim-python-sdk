import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult

load_dotenv()

ai_document_intelligence_endpoint = os.getenv("AI_DOCUMENT_INTELLIGENCE_ENDPOINT")
ai_document_intelligence_api_key = os.getenv("AI_DOCUMENT_INTELLIGENCE_API_KEY")
credential = AzureKeyCredential(ai_document_intelligence_api_key)

# 以下を変更してください
document_name = "sample.pdf"

current_dir = os.path.dirname(os.path.abspath(__file__))
path_to_sample_documents = os.path.join(current_dir, "..", "data", document_name)

ai_document_intelligence_client = DocumentIntelligenceClient(
    ai_document_intelligence_endpoint,
    credential
)

with open(path_to_sample_documents, "rb") as f:
        poller = ai_document_intelligence_client.begin_analyze_document(
        "prebuilt-layout",
        body = f
    )

result: AnalyzeResult = poller.result()

for page in result.pages:
    if page.lines:
        for line_idx, line in enumerate(page.lines):
            if page.words:
                print(f"Line {line_idx} has content: '{line.content}'")
