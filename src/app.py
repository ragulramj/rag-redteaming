import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential
import openai

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
SEARCH_SERVICE_NAME = os.getenv('SEARCH_SERVICE_NAME')
SEARCH_INDEX_NAME = os.getenv('SEARCH_INDEX_NAME')
SEARCH_API_KEY = os.getenv('SEARCH_API_KEY')

if not all([OPENAI_API_KEY, SEARCH_SERVICE_NAME, SEARCH_INDEX_NAME, SEARCH_API_KEY]):
    raise RuntimeError('Missing environment configuration')

openai.api_key = OPENAI_API_KEY

search_endpoint = f"https://{SEARCH_SERVICE_NAME}.search.windows.net"
search_client = SearchClient(
    endpoint=search_endpoint,
    index_name=SEARCH_INDEX_NAME,
    credential=AzureKeyCredential(SEARCH_API_KEY)
)

class Query(BaseModel):
    query: str

app = FastAPI()

@app.post('/rag')
async def rag_endpoint(item: Query):
    results = search_client.search(item.query)
    docs = [r['content'] for r in results]
    context = "\n".join(docs)
    prompt_template = open(os.path.join('prompts', 'base_prompt.txt')).read()
    prompt = prompt_template.format(context=context, question=item.query)
    try:
        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': prompt}]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    answer = completion['choices'][0]['message']['content']
    return {'answer': answer, 'documents': docs}
