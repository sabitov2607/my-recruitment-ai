from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
from parser import extract_text_from_file
from nlp import analyze_candidate

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/analyze", methods=["POST"])
def analyze():
    job_description = request.form.get("jobDescription", "")
    files = request.files.getlist("cvFiles")

    if not files:
        return jsonify({"error": "No files uploaded"}), 400

    results = []

    for file in files:
        unique_name = f"{uuid.uuid4()}_{file.filename}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_name)

        file.save(filepath)

        text = extract_text_from_file(filepath)
        analysis = analyze_candidate(text, job_description)

        analysis["candidate"] = file.filename
        results.append(analysis)

    return jsonify({"results": results})

if __name__ == "__main__":
    app.run(debug=True)
