# Intelligent Resume Screening System — Streamlit & Colab Deployment Guide

This guide explains how to deploy and demo the Intelligent Resume Screening System using Streamlit, fully in Google Colab (no local setup required). Suitable for product-based company demos and real-world candidate screening.

---

## 1. Project Overview
- Upload a Job Description (JD) and a Resume (PDF or text) via the web UI.
- The app extracts text, computes semantic similarity, and highlights missing skills/requirements from the JD.
- No precomputed embeddings or local installation needed—everything runs in Colab and is accessible via a public link.

---

## 2. Files Needed
- `app.py` — Streamlit app (latest version with upload/compare logic)
- (Optional) `notebooks/batch_resume_processing.ipynb` — for advanced batch processing, not needed for basic demo

---

## 3. Deploying in Google Colab

### Step 1: Upload Files
- Open a new Google Colab notebook.
- Upload `app.py` using the file upload tool or this code cell:
  ```python
  from google.colab import files
  files.upload()  # Select app.py
  ```

### Step 2: Install Dependencies
  ```python
  !pip install streamlit pyngrok sentence-transformers pdfminer.six
  ```

### Step 3: Run Streamlit with ngrok
  ```python
  from pyngrok import ngrok
  import threading
  import time
  import os

  def run():
      os.system('streamlit run app.py --server.port 8501')

  thread = threading.Thread(target=run)
  thread.start()
  time.sleep(5)
  public_url = ngrok.connect(8501)
  print('Streamlit app URL:', public_url)
  ```

### Step 4: Use the App
- Open the printed public URL.
- Upload a JD and a resume (PDF or text) in the app UI.
- The app will show a similarity score and highlight missing skills/requirements.

---

## 4. For Product-Based Company Demos
- No local installation or cloud VM required—everything runs in Colab, using free GPU/TPU if available.
- Secure: files are processed in the Colab session, not uploaded to third-party servers.
- Fast iteration: update `app.py` and rerun the deployment cell to demo new features instantly.
- Suitable for technical and non-technical audiences—just share the Colab notebook and public app link.

---

## 5. Advanced: Batch Processing (Optional)
- Use `notebooks/batch_resume_processing.ipynb` to process many resumes at once, extract entities, generate embeddings, and analyze at scale.
- For most demos, the upload-and-compare app is sufficient.

---

## 6. Troubleshooting
- If the app does not start, restart the Colab runtime and repeat the steps.
- If you update `app.py`, re-upload and rerun the deployment cell.
- For PDF extraction issues, ensure `pdfminer.six` is installed.

---

## 7. Security & Privacy
- All processing happens in your Colab session. No data is stored after the session ends.
- For production, consider deploying on a secure cloud VM or private server.

---

## 8. Contact & Contribution
- For improvements, open issues or pull requests in your project repository.
- For company-specific customization, contact the project maintainer.

---

**This guide ensures a smooth, no-installation-required demo for product-based companies and real-world users.**
