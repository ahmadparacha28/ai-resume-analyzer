from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_match(resume_text, job_description):
    documents = [resume_text, job_description]

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(vectors[0], vectors[1])
    match_score = round(similarity[0][0] * 100, 2)

    return match_score


def find_missing_skills(resume_skills, job_description):
    job_description = job_description.lower()
    missing = []

    for skill in resume_skills:
        if skill not in job_description:
            missing.append(skill)

    return missing