# 🚀 Candidate Evaluator API (FastAPI)

A FastAPI-based backend service for evaluating candidate CVs and projects using LLMs (OpenAI / OpenRouter).  
It supports background evaluation tasks, document ingestion to ChromaDB, and structured scoring using Llama or Mistral models.

---

## 📦 1. Setup Project

### 🧰 Prerequisites
Make sure you have installed:
- Python 3.10+
- pip
- virtualenv (optional but recommended)
- PostgreSQL / SQLite (depending on configuration)

---

### 🏗️ Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 📦 Install Dependencies
```bash
pip install -r requirements.txt
```

### 🔑 Environment Variables
```bash
cp .env.example .env
vi .env
```
get your OpenAI API key from https://platform.openai.com/account/api-keys or Openrouter API key from https://openrouter.ai/ and get cohere api key


### Migrate Database
```bash
alembic upgrade head
```

###  Ingest Documents
```bash
python src/ingest_reference_docs.py

```

### 🚀 Run Application
```bash
fastapi run src\main.py
```

or 

```bash
fastapi dev src\main.py