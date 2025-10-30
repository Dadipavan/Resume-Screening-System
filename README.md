# Intelligent Resume Screening System — How It Works

This document explains, step by step, how the Intelligent Resume Screening System (HRTech AI) works, so you can confidently present and explain it to anyone.

---

## 1. User Uploads
- The app provides a web interface (Streamlit) where users upload:
  - A Job Description (JD) — as a PDF or text file
  - A Resume — as a PDF or text file

## 2. Text Extraction
- The app extracts text from the uploaded files:
  - For PDFs: uses `pdfminer.six` to extract all readable text
  - For text files: reads the content directly
- The extracted text is previewed in the app for both JD and Resume

## 3. Entity Extraction (NLP)
- The app uses a spaCy-based NLP module to extract key entities from both JD and Resume:
  - **Skills** (e.g., Python, SQL, Machine Learning)
  - **Education** (e.g., Bachelor, Master, University names)
  - **Experience** (e.g., years, project roles, organizations)
- This is done using keyword matching and named entity recognition (NER)

## 4. Embedding & Similarity
- The app uses a pre-trained SBERT model (`all-MiniLM-L6-v2`) to convert both the JD and Resume text into high-dimensional vectors (embeddings)
- It computes the **cosine similarity** between the two embeddings:
  - A score close to 1.0 means the resume is very similar to the JD
  - A lower score means less similarity
- The similarity score is displayed in the app

## 5. Entity Comparison & Missing Items
- The app compares the extracted entities from the JD and Resume:
  - For each category (skills, education, experience), it shows:
    - What is present in the JD
    - What is present in the Resume
    - What is **missing** from the Resume (i.e., required by the JD but not found in the Resume)
- This helps recruiters or candidates quickly see gaps

## 6. User Experience
- All results (text previews, similarity score, entity comparison, missing items) are shown in a clean, interactive web UI
- No installation is needed for end users if deployed on Streamlit Cloud or Colab

## 7. Deployment
- The app can be run in Google Colab (for development/demo) or deployed live on Streamlit Cloud for public access
- All dependencies are listed in `requirements.txt` and the app is ready for one-click deployment

---

## Summary Table
| Step                | What Happens                                                                 |
|---------------------|------------------------------------------------------------------------------|
| Upload              | User uploads JD and Resume (PDF/text)                                        |
| Text Extraction     | App extracts and previews text from both files                                |
| Entity Extraction   | App uses NLP to extract skills, education, experience                         |
| Embedding           | App computes SBERT embeddings for both texts                                 |
| Similarity          | App calculates and displays similarity score                                  |
| Entity Comparison   | App shows what skills/education/experience are missing from the Resume        |
| Deployment          | App can be run in Colab or deployed live on Streamlit Cloud                   |

---

## How to Explain to Others
- "This app lets you upload a job description and a resume, then instantly tells you how closely the resume matches the job, and what skills or qualifications are missing. It uses advanced NLP and AI models, but is easy for anyone to use."

---

For more technical details, see the main `README.md` and `DEPLOYMENT_README.md` files.
