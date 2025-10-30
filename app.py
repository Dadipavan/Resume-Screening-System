


import streamlit as st
import numpy as np
from sentence_transformers import SentenceTransformer
from src.entity_extraction import extract_entities


st.title("Intelligent Resume Screening System (Upload & Compare)")
st.write("Upload a Job Description and a Resume (PDF or text). Get similarity score, missing skills/requirements, and entity comparison.")

# Load SBERT model once for speed
@st.cache_resource(show_spinner=False)
def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')
model = load_model()

def extract_text_from_pdf(file):
    try:
        from pdfminer.high_level import extract_text
        text = extract_text(file)
        return text
    except Exception:
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
    jd_emb = model.encode([jd_text], convert_to_numpy=True)
    resume_emb = model.encode([resume_text], convert_to_numpy=True)
    sim = 1 - np.dot(jd_emb, resume_emb.T) / (np.linalg.norm(jd_emb) * np.linalg.norm(resume_emb))
    similarity = 1 - sim[0][0]

    # --- Creative Results UI ---
    st.markdown("---")
    st.markdown("## :sparkles: Results Overview")
    # Similarity Score

    st.markdown(
        f"<h4 style='margin-bottom:0;'>Similarity Score</h4>", unsafe_allow_html=True
    )
    similarity_clamped = min(max(similarity, 0.0), 1.0)
    st.progress(similarity_clamped)
    if similarity > 0.8:
        st.success(f"Excellent match! ({similarity:.2f})")
    elif similarity > 0.6:
        st.info(f"Good match. ({similarity:.2f})")
    else:
        st.warning(f"Low match. ({similarity:.2f})")

    # Entity extraction
    jd_entities = extract_entities(jd_text)
    resume_entities = extract_entities(resume_text)

    st.markdown("---")
    st.markdown("## :mag: Entity Comparison")
    col1, col2, col3 = st.columns(3)
    entity_labels = {"skills": "🛠️ Skills", "education": "🎓 Education", "experience": "💼 Experience"}
    for key in ["skills", "education", "experience"]:
        with col1 if key == "skills" else col2 if key == "education" else col3:
            st.markdown(f"<b>{entity_labels[key]} in JD</b>", unsafe_allow_html=True)
            if jd_entities[key]:
                st.markdown(
                    " ".join([
                        f"<span style='background-color:#e0e0e0;border-radius:8px;padding:4px 8px;margin:2px;display:inline-block;'>{item}</span>"
                        for item in jd_entities[key]
                    ]), unsafe_allow_html=True
                )
            else:
                st.write("None")
            st.markdown(f"<b>{entity_labels[key]} in Resume</b>", unsafe_allow_html=True)
            if resume_entities[key]:
                st.markdown(
                    " ".join([
                        f"<span style='background-color:#d1ffd6;border-radius:8px;padding:4px 8px;margin:2px;display:inline-block;'>{item}</span>"
                        for item in resume_entities[key]
                    ]), unsafe_allow_html=True
                )
            else:
                st.write("None")
            missing = set(jd_entities[key]) - set(resume_entities[key])
            st.markdown(f"<b>Missing from Resume</b>", unsafe_allow_html=True)
            if missing:
                st.markdown(
                    " ".join([
                        f"<span style='background-color:#ffd6d6;border-radius:8px;padding:4px 8px;margin:2px;display:inline-block;'>{item}</span>"
                        for item in missing
                    ]), unsafe_allow_html=True
                )
            else:
                st.success("None! All covered.")
