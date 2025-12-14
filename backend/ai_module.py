# backend/ai_module.py

import os
import re
import spacy
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from PyPDF2 import PdfReader

# MODELS
nlp = spacy.load("en_core_web_sm")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# SKILLS
DEFAULT_SKILLS = [
    "python", "java", "sql", "react", "nodejs", "django", "fastapi",
    "docker", "aws", "nlp", "computer vision", "pytorch", "tensorflow"
]

# ----------------------------
# TEXT EXTRACTION
# ----------------------------
def extract_text_from_file(file_path):
    ext = file_path.split(".")[-1].lower()

    if ext == "pdf":
        text = ""
        reader = PdfReader(file_path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


# ----------------------------
# SKILL EXTRACTION
# ----------------------------
def extract_skills(text):
    text_lower = text.lower()
    return sorted({skill for skill in DEFAULT_SKILLS if skill in text_lower})


# ----------------------------
# MATCH SCORE (FIXED)
# ----------------------------
def calculate_match_score(cv_text, vacancy_text):
    embeddings = embedder.encode([cv_text, vacancy_text])

    sim = cosine_similarity(
        embeddings[0].reshape(1, -1),
        embeddings[1].reshape(1, -1)
    )[0][0]

    return round(float(sim) * 100, 2)  # ✅ PURE PYTHON FLOAT


# ----------------------------
# FULL PIPELINE
# ----------------------------
def process_candidate(cv_path, vacancy_text):
    cv_text = extract_text_from_file(cv_path)
    skills = extract_skills(cv_text)
    match_score = calculate_match_score(cv_text, vacancy_text)

    return {
        "skills": skills,
        "match_score": match_score,
        "cv_text": cv_text[:500]
    }
