import os
import re
import spacy
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from PyPDF2 import PdfReader

nlp = spacy.load("en_core_web_sm")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

DEFAULT_SKILLS = [
    "HTML5", "CSS3", "SCSS", "SASS", "JavaScript (ES6+)", "TypeScript", "React.js", "Next.js",
    "Redux", "Redux Toolkit", "React Hooks", "React Context API", "JSX", "Component-based Architecture",
    "Responsive Web Design", "Cross-browser Compatibility", "Tailwind CSS", "Bootstrap", "Material UI",
    "Ant Design", "CSS Grid", "Flexbox", "BEM Methodology", "Styled Components", "PostCSS",
    "UI/UX Implementation", "REST API Integration", "Axios", "Fetch API", "JSON Handling", "Form Validation",
    "Client-side Caching", "Next.js App Router", "Next.js Pages Router", "Server-Side Rendering (SSR)",
    "Static Site Generation (SSG)", "Client Components", "Server Components", "React Performance Optimization",
    "Code Splitting", "Lazy Loading", "Odoo Framework", "Odoo 16", "Odoo 17", "OWL JS", "Odoo Web Client",
    "Odoo Views (Tree, Form, Kanban)", "Odoo Controllers", "Odoo REST API", "Odoo QWeb Templates",
    "Odoo Frontend Customization", "Odoo Module Development", "Git", "GitHub", "GitLab", "Git Flow",
    "Version Control", "VS Code", "NPM", "Yarn", "Vite", "Webpack", "Debugging", "Error Handling",
    "ESLint", "Prettier", "Code Refactoring", "Performance Optimization", "CI/CD Basics", "Build Optimization",
    "Environment Variables", "Production Builds", "Deployment with Vercel", "Deployment with Netlify",
    "Problem Solving", "Clean Code", "SOLID Principles", "Agile", "Scrum", "Team Collaboration",
    "Time Management", "Documentation Writing"
]
DEFAULT_SKILLS = [skill.lower() for skill in DEFAULT_SKILLS]

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


def extract_skills(text):
    text_lower = text.lower()
    return sorted({skill for skill in DEFAULT_SKILLS if skill in text_lower})


def calculate_match_score(cv_text, vacancy_text):
    embeddings = embedder.encode([cv_text, vacancy_text])

    sim = cosine_similarity(
        embeddings[0].reshape(1, -1),
        embeddings[1].reshape(1, -1)
    )[0][0]

    return round(float(sim) * 100, 2)


def process_candidate(cv_path, vacancy_text):
    cv_text = extract_text_from_file(cv_path)
    skills = extract_skills(cv_text)
    match_score = calculate_match_score(cv_text, vacancy_text)

    return {
        "skills": skills,
        "match_score": match_score,
        "cv_text": cv_text[:500]
    }
