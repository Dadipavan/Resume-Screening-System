# Intelligent Resume Screening System (HRTech AI)

Automate screening of resumes against job descriptions using modern NLP and embeddings.

This repository contains an end-to-end design and setup notes for an "Intelligent Resume Screening System" that demonstrates PDF parsing, entity extraction, embedding-based similarity (SBERT or OpenAI embeddings), FAISS indexing, ranking, and a simple UI/deployment layer (Streamlit or FastAPI + Docker). It also outlines optional RAG-style candidate insights.

## Highlights

- End-to-end pipeline: PDF → text → NLP entity extraction → embeddings → FAISS index → ranked candidates
- Options for embeddings: local SBERT (recommended small models for CPU) or OpenAI embeddings (remote)
- Deployable as a lightweight Streamlit app or a FastAPI microservice, plus Dockerization
- Designed to run on modest hardware (8 GB RAM, CPU-only)


## Table of Contents

1. Project overview
2. Project structure & files
3. Hardware & device requirements (8 GB RAM, no GPU)
4. Installation & Quick Start
5. Usage examples
6. Deployment (Streamlit, FastAPI + Docker)
7. Optional: RAG / Chat-style Candidate Insights
8. Troubleshooting & tips
9. Contributing & license
## 2 — Project structure & files

```
├── app.py                  # Main Streamlit app
├── requirements.txt        # All dependencies
├── src/
│   └── entity_extraction.py  # Entity extraction module (spaCy)
├── data/
│   ├── sample_jd.txt         # Sample job description
│   └── sample_resume.txt     # Sample resume
├── notebooks/
│   └── batch_resume_processing.ipynb  # Batch processing notebook (Colab-ready)
├── README.md
├── DEPLOYMENT_README.md
├── HOW_IT_WORKS.md
```

**All files above are required for full functionality and demo.**

## 4 — Installation & Quick Start

### Local (Windows, Linux, Mac)
1. Clone/download this repo and open a terminal in the project folder.
2. (Recommended) Create a virtual environment:
    ```powershell
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1  # Windows
    # or
    source .venv/bin/activate      # Linux/Mac
    ```
3. Install dependencies:
    ```powershell
    pip install --upgrade pip
    pip install -r requirements.txt
    ```
4. Run the app:
    ```powershell
    streamlit run app.py
    ```
5. Open the local Streamlit URL in your browser.

### Google Colab or Streamlit Cloud (no install needed)
1. Upload all files to Colab or push to GitHub for Streamlit Cloud.
2. In Colab, install dependencies:
    ```python
    !pip install streamlit pyngrok sentence-transformers pdfminer.six spacy hnswlib pandas numpy
    ```
3. Run the app with ngrok (see `DEPLOYMENT_README.md` for code snippet).
4. Use the public URL to access the app from anywhere.

### Batch Processing (optional, for many resumes)
- Use `notebooks/batch_resume_processing.ipynb` to process, extract, and embed multiple resumes at once.
- Outputs can be used for analytics or as input to the app.

## 1 — Project overview

The goal is to automate candidate screening by computing similarity between resume embeddings and job-description embeddings. The pipeline is typically:

1. Extract text from uploaded resumes (PDFs, DOCX).
2. Extract structured entities (skills, roles, education) with an entity extractor (spaCy, rule-based, or transformer NER).
3. Generate embeddings for the candidate resume (and JDs) using SBERT or an external embeddings API.
4. Store embeddings in a vector index (FAISS/hnswlib) and perform nearest-neighbor search.
5. Score and rank candidates, present highlighted matches.

This repo is intended as a template — you can plug in your own parsing/extraction components and models.

## 2 — Components

- Resume parsing: `pdfminer.six`, `PyPDF2`, `textract`, or Apache Tika for robust extraction.
- Entity extraction: `spaCy` + custom patterns or transformer NER (Hugging Face models).
- Embeddings: `sentence-transformers` (local SBERT) or OpenAI embeddings (remote API).
- Vector store / similarity: `faiss` (faiss-cpu) or alternatives `hnswlib` / `annoy` (Windows-friendly).
- Serving/UI: `streamlit` for quick UI or `fastapi` + `uvicorn` for production microservice.
- Optional: RAG (retrieval-augmented generation) using OpenAI/GPT or local LLM to provide chat-style insights.

## 3 — Hardware & device requirements (your environment)

You said: 8 GB RAM, no GPU. This README includes guidance tailored for that.

- Minimum recommended: Windows 10/11 or Linux, 8 GB RAM, CPU-only.
- Python 3.9–3.11 (3.10 recommended).
- Disk: ~2–5 GB free for Python packages and small models; more if you store many embeddings.

Important constraints and recommendations for 8 GB RAM / CPU-only:

- Use a small SBERT model such as `all-MiniLM-L6-v2` (embedding size 384, ~80–100 MB). It performs very well and is memory efficient.
- Avoid large transformer encoders on CPU (they will be slow and may exceed memory).
- For vector store on Windows: `faiss` can be tricky to install via pip. If you have trouble, use `hnswlib` or `annoy` (both lighter and easier to install on Windows).
- Reduce batch sizes (e.g., 8 or 16) when encoding multiple documents to limit peak memory.
- Increase your OS page file (virtual memory) if you encounter memory errors on Windows.
- Close other memory-heavy apps while running experiments.

Alternative: use OpenAI embeddings (or other hosted embeddings) to offload compute and memory — you only need CPU for data handling. This trades latency and cost for lower local resource usage.

## 4 — Installation (PowerShell examples)

Recommended workflow: create a virtual environment and install required packages. Example `requirements.txt` (minimal):

```
sentence-transformers>=2.2.0
streamlit
fastapi
uvicorn[standard]
pdfminer.six
spacy
hnswlib
scikit-learn
pandas
python-multipart
tqdm
requests
```

Notes: Replace `hnswlib` with `faiss-cpu` if you can install FAISS on your platform.

PowerShell commands (Windows):

```powershell
# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Upgrade pip and install packages from requirements file
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

If you don't want to create a `requirements.txt` yet, install core packages directly:

```powershell
pip install sentence-transformers streamlit fastapi uvicorn pdfminer.six spacy hnswlib scikit-learn pandas python-multipart
```

Windows + FAISS note: if you want `faiss-cpu` on Windows, consider using Conda (conda-forge) or use Docker for a Linux container. Alternatively, choose `hnswlib`.


## 5 — Usage examples

#### 1. Upload and compare (Streamlit app)
- Upload a JD and a resume (PDF or text) in the app UI.
- The app extracts text, computes similarity, and highlights missing skills/requirements and entity comparison (skills, education, experience).
- Try with the provided sample files in `data/` for a quick demo.

#### 2. Batch processing (notebook)
- Use `notebooks/batch_resume_processing.ipynb` to process multiple resumes, extract entities, and compute embeddings for analytics or advanced use.

## 6 — Deployment

Streamlit (quick local UI):

PowerShell to run Streamlit app (assumes `app.py` is present):

```powershell
streamlit run app.py
```

FastAPI microservice (example):

Run using uvicorn:

```powershell
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 1
```

Dockerization (recommended to avoid Windows package issues and keep environment reproducible):

Example `Dockerfile` (Linux-based):

```
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt ./
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libopenblas-dev git curl \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get remove -y build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*
COPY . /app
CMD ["streamlit", "run", "app.py", "--server.port", "8501", "--server.address","0.0.0.0"]
```

Build and run (PowerShell):

```powershell
docker build -t resume-screening:latest .
docker run -p 8501:8501 --memory="4g" --cpus="2" resume-screening:latest
```

Notes:
- Limit Docker memory (`--memory`) if running on 8GB host to prevent full host exhaustion.
- On Windows, using Docker Desktop gives you options to set memory and CPU limits for the VM.

## 7 — Optional: RAG / Candidate Insights

You can add a retrieval-augmented generation layer that uses the candidate’s extracted facts and embeddings as context for a small chat-style interface that provides "Candidate Insights". Two approaches:

1. Hosted LLMs (OpenAI/GPT): embed resume segments, retrieve top-k with FAISS, pass retrieved segments + prompt to the LLM to generate insights.
2. Local LLMs: if you have GPU or enough RAM (not recommended for 8GB), you can run smaller LLMs via `llama.cpp`/GGML or opt for hosted services.

For 8GB machines, prefer hosted LLMs for RAG.

## 8 — Troubleshooting & tips

- MemoryError / OOM: reduce batch size, use smaller SBERT models, use hnswlib instead of faiss-cpu, increase page file, or run inside Docker with controlled memory.
- FAISS install issues on Windows: use Conda (conda-forge) or switch to `hnswlib`. Example conda command:

```powershell
conda install -c conda-forge faiss-cpu
```

- Slow encoding: use `model.encode(..., show_progress_bar=False, batch_size=8)` and ensure `device='cpu'` to avoid accidental GPU device selection.
- Persisting embeddings: store embeddings and metadata on disk (parquet/SQLite + binary embeddings) so you don't recompute everything each run.

## 9 — Contributing & license

Contributions welcome — open issues for features or bugs. Include short tests for key components (parsing, embedding, ranking).

License: choose an appropriate license for your project (MIT/Apache-2.0 recommended for examples).

## Final notes & next steps

- For your machine (8GB, CPU-only): start with `sentence-transformers` using `all-MiniLM-L6-v2` and `hnswlib` for indexing. This combo is lightweight and provides fast development cycles.
- If you need lower local memory usage, use OpenAI (or other hosted) embeddings to avoid local model memory entirely.

If you'd like, I can:

- Add a starter `app.py` Streamlit UI wired to a minimal pipeline that runs on CPU and uses `all-MiniLM-L6-v2` and `hnswlib`.
- Create a `requirements.txt` and a simple `Dockerfile` tailored to Windows->Docker (Linux) builds.

Refer to this README (`README.md`) for guidance and next steps.
