# rag-redteaming

This repository demonstrates a simplified Retrieval-Augmented Generation (RAG) service
using **Python** only. The backend is inspired by the
[Azure Search + OpenAI demo backend](https://github.com/Azure-Samples/azure-search-openai-demo/tree/main/app/backend)
but pared down to highlight how RAG pipelines can be red teamed.

All example medical documents in this repo are **synthetic**. Do **not** store real
patient data here. The goal is to explore vulnerabilities in RAG systems without
exposing private information.

## Repository layout


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

---
This project is for educational purposes only. All data is fake and provided
solely to demonstrate how RAG pipelines can be tested and improved.
