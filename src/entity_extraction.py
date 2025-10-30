import spacy
from typing import List, Dict

# Load spaCy model (en_core_web_sm or similar)
try:
    nlp = spacy.load("en_core_web_sm")
except:
    import os
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Example skill/education/experience patterns (expand as needed)
SKILL_KEYWORDS = ["python", "java", "sql", "machine learning", "nlp", "deep learning", "react", "aws", "docker", "kubernetes"]
EDU_KEYWORDS = ["bachelor", "master", "phd", "b.sc", "m.sc", "btech", "mtech", "degree", "university", "college"]
EXP_KEYWORDS = ["year", "experience", "worked", "managed", "led", "project", "team"]

def extract_entities(text: str) -> Dict[str, List[str]]:
    doc = nlp(text)
    skills = set()
    education = set()
    experience = set()
    # Simple keyword matching (expand for production)
    for token in doc:
        t = token.text.lower()
        if t in SKILL_KEYWORDS:
            skills.add(t)
        if t in EDU_KEYWORDS:
            education.add(t)
        if t in EXP_KEYWORDS:
            experience.add(t)
    # Named entity recognition for organizations, dates, etc.
    for ent in doc.ents:
        if ent.label_ == "ORG":
            education.add(ent.text)
        if ent.label_ == "DATE":
            experience.add(ent.text)
    return {
        "skills": list(skills),
        "education": list(education),
        "experience": list(experience)
    }

if __name__ == "__main__":
    sample = """John Doe has 5 years of experience in Python, machine learning, and AWS. He graduated from Stanford University with a Master's degree."""
    print(extract_entities(sample))
