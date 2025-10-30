

import streamlit as st
import numpy as np
from sentence_transformers import SentenceTransformer
import io
from src.entity_extraction import extract_entities

st.title("Intelligent Resume Screening System (Upload & Compare)")

st.write("Upload a Job Description and a Resume (PDF or text). Get similarity score, missing skills/requirements, and entity comparison.")

def extract_text_from_pdf(file):
    try:
        from pdfminer.high_level import extract_text
        text = extract_text(file)
        return text
    except Exception as e:
        return ""

# Uploaders
jd_file = st.file_uploader("Upload Job Description (PDF or .txt)", type=["pdf", "txt"], key="jd")
resume_file = st.file_uploader("Upload Resume (PDF or .txt)", type=["pdf", "txt"], key="resume")

jd_text = ""
resume_text = ""

if jd_file is not None:
    if jd_file.type == "application/pdf":
        jd_text = extract_text_from_pdf(jd_file)
    else:
        jd_text = jd_file.read().decode("utf-8", errors="ignore")
    st.subheader("Job Description Preview:")
    st.write(jd_text[:1000] + ("..." if len(jd_text) > 1000 else ""))

if resume_file is not None:
    if resume_file.type == "application/pdf":
        resume_text = extract_text_from_pdf(resume_file)
    else:
        resume_text = resume_file.read().decode("utf-8", errors="ignore")
    st.subheader("Resume Preview:")
    st.write(resume_text[:1000] + ("..." if len(resume_text) > 1000 else ""))

if st.button("Compare Resume to JD") and jd_text and resume_text:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    jd_emb = model.encode([jd_text], convert_to_numpy=True)
    resume_emb = model.encode([resume_text], convert_to_numpy=True)
    sim = 1 - np.dot(jd_emb, resume_emb.T) / (np.linalg.norm(jd_emb) * np.linalg.norm(resume_emb))
    similarity = 1 - sim[0][0]
    st.subheader(f"Similarity Score: {similarity:.2f}")

    # Entity extraction
    jd_entities = extract_entities(jd_text)
    resume_entities = extract_entities(resume_text)
    st.write("## Entity Comparison")
    for key in ["skills", "education", "experience"]:
        st.write(f"**{key.capitalize()} in JD:** {', '.join(jd_entities[key]) if jd_entities[key] else 'None'}")
        st.write(f"**{key.capitalize()} in Resume:** {', '.join(resume_entities[key]) if resume_entities[key] else 'None'}")
        missing = set(jd_entities[key]) - set(resume_entities[key])
        st.write(f"**Missing from Resume:** {', '.join(missing) if missing else 'None!'}")
