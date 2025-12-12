def load_skills():
    with open("../skills.txt", "r") as f:
        return [s.strip().lower() for s in f.readlines()]

SKILLS = load_skills()

def analyze_candidate(cv_text, job_text):
    cv_text = cv_text.lower()
    job_text = job_text.lower()

    found = [s for s in SKILLS if s in cv_text]
    required = [s for s in SKILLS if s in job_text]

    missing = [s for s in required if s not in found]

    score = 0
    if required:
        score = int(len(found) / len(required) * 100)
        score = min(score, 100)

    summary = f"Found {len(found)} skills, missing {len(missing)}."

    return {
        "match": score,
        "found": found,
        "missing": missing,
        "summary": summary,
    }
