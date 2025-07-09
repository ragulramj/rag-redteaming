"""Index synthetic documents in Azure Cognitive Search."""

import os
from dotenv import load_dotenv
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex, SimpleField, edm
from PyPDF2 import PdfReader

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

SEARCH_SERVICE_NAME = os.getenv('SEARCH_SERVICE_NAME')
SEARCH_INDEX_NAME = os.getenv('SEARCH_INDEX_NAME')
SEARCH_API_KEY = os.getenv('SEARCH_API_KEY')

endpoint = f"https://{SEARCH_SERVICE_NAME}.search.windows.net"
credential = AzureKeyCredential(SEARCH_API_KEY)

index_client = SearchIndexClient(endpoint=endpoint, credential=credential)

# Create index if it doesn't exist
if SEARCH_INDEX_NAME not in [x.name for x in index_client.list_indexes()]:
    fields = [
        SimpleField(name="id", type=edm.String, key=True),
        SimpleField(name="content", type=edm.String, searchable=True)
    ]
    index = SearchIndex(name=SEARCH_INDEX_NAME, fields=fields)
    index_client.create_index(index)

search_client = SearchClient(endpoint=endpoint, index_name=SEARCH_INDEX_NAME, credential=credential)

DOCS_PATH = os.path.join(os.path.dirname(__file__), '..', 'docs')

def index_pdfs():
    for name in os.listdir(DOCS_PATH):
        if name.lower().endswith('.pdf'):
            path = os.path.join(DOCS_PATH, name)
            text = extract_text(path)
            doc_id = os.path.splitext(name)[0]
            search_client.upload_documents([{"id": doc_id, "content": text}])
            print(f"Indexed {name}")


def extract_text(pdf_path: str) -> str:
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


if __name__ == '__main__':
    index_pdfs()
