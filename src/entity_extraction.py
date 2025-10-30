import spacy
from typing import List, Dict

# Load spaCy model (en_core_web_sm or similar)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
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
    # Normalize tokens for better matching
    tokens = [t.text.lower().strip() for t in doc]
    # Multi-word skill matching
    text_lower = text.lower()
    for skill in SKILL_KEYWORDS:
        if skill in text_lower:
            skills.add(skill)
    for edu in EDU_KEYWORDS:
        if edu in text_lower:
            education.add(edu)
    for exp in EXP_KEYWORDS:
        if exp in text_lower:
            experience.add(exp)
    # Named entity recognition for organizations, dates, etc.
    for ent in doc.ents:
        if ent.label_ == "ORG":
            education.add(ent.text)
        if ent.label_ == "DATE":
            experience.add(ent.text)
    return {
        "skills": sorted(skills),
        "education": sorted(education),
        "experience": sorted(experience)
    }

if __name__ == "__main__":
    sample = """Sai Pavan has 5 years of experience in Python, machine learning, and AWS. He graduated from Stanford University with a Master's degree."""
    print(extract_entities(sample))
