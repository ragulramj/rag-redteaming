# rag-redteaming

This repository demonstrates a simplified Retrieval-Augmented Generation (RAG) service
using **Python** only. The backend is inspired by the
[Azure Search + OpenAI demo backend](https://github.com/Azure-Samples/azure-search-openai-demo/tree/main/app/backend)
but pared down to highlight how RAG pipelines can be red teamed.

All example medical documents in this repo are **synthetic**. Do **not** store real
patient data here. The goal is to explore vulnerabilities in RAG systems without
exposing private information.

## Repository layout


- `docs/` – Scripts to generate synthetic medical PDFs for indexing in Azure Cognitive Search.
- `src/` – Python code for the RAG backend. A `.env` file in this folder holds API keys
 and other secrets.
- `prompts/` – Base prompt templates and red teaming prompts used to probe the system.
- `tests/` – Basic test cases for the backend.
- `deploy/` – Dockerfile and `aks-deployment.yaml` to run the service on AKS.
- `redteam/` – Jupyter notebook to automate adversarial prompts against the running service.

Generate example PDFs by running `python docs/generate_docs.py`.
=======

- `prompts/` – Base prompt templates and red teaming prompts used to probe the system.
- `tests/` – Basic test cases for the backend.
- `deploy/` – Dockerfile and `aks-deployment.yaml` to run the service on AKS.



## Setup

1. **Prepare environment variables**
   - Copy `src/.env.example` to `src/.env` and fill in your OpenAI (or Gemini/Claude)
     keys and Azure Cognitive Search details.
2. **Install dependencies**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r src/requirements.txt

   pip install jupyter  # optional, for the red teaming notebook
   ```
3. **Index sample documents**
   - Run `python docs/generate_docs.py` if you need example PDFs.
   - Execute `python src/index_documents.py` to upload the PDFs from `docs/` into your Azure Cognitive Search index.
4. **Run the RAG service**
   ```bash
   uvicorn src.app:app --reload
   ```
5. **Customize prompts**
   - Edit `prompts/base_prompt.txt` to change the system prompt.
=======
   ```
3. **Index sample documents**



## Docker & AKS deployment

Build the container and push it to your registry:
```bash
docker build -t <registry>/rag-redteaming:latest -f deploy/Dockerfile .
docker push <registry>/rag-redteaming:latest
```
Then apply the Kubernetes manifest:
```bash
kubectl apply -f deploy/aks-deployment.yaml
```

## Red teaming

The `prompts/` directory includes prompts aimed at exposing RAG weaknesses.
These range from simple jailbreak attempts to queries seeking confidential
information. Use them responsibly to evaluate the system's safety.


To automate red teaming once the service is running, open the notebook
`redteam/attack_demo.ipynb` with Jupyter and run all cells. It will issue
several adversarial requests to the `/rag` endpoint and print the responses.


---
This project is for educational purposes only. All data is fake and provided
solely to demonstrate how RAG pipelines can be tested and improved.
