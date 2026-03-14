import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_sm")

# Basic skill list (we will improve later)
SKILLS = [
    "python", "java", "c++", "machine learning",
    "deep learning", "react", "flask",
    "sql", "html", "css", "javascript"
]

def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in SKILLS:
        if skill in text:
            found_skills.append(skill)

    return list(set(found_skills))