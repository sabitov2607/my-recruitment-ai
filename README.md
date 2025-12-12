# AI Recruitment Assistant

This is a simple AI-powered recruitment system that analyzes uploaded CVs (PDF or DOCX), compares them with a job description, extracts skills, calculates match percentage, detects missing skills, and generates a short summary.

The project consists of two parts:
- **Frontend** (HTML/CSS/JS), opened directly in the browser.
- **Backend** (Python Flask), used for processing CVs and performing NLP.

---

## 📁 Project Structure

my-recruitment-ai/
│
├── frontend/
│   ├── index.html
│   ├── styles.css
│   ├── app.js
│   ├── bg-main.jpg
│   ├── logo.png
│   └── smile.jpg
│
├── backend/
│   ├── app.py
│   ├── parser.py
│   ├── nlp.py
│   ├── utils.py
│   └── uploads/
│
├── skills.txt
├── requirements.txt
└── README.md

---

## 🚀 How to Run the Project

### 1. Install dependencies  
Navigate to the project root (where requirements.txt is located) and run:

pip3 install -r requirements.txt

### 2. Start the backend server  

cd backend
python3 app.py


The backend will start at:

http://127.0.0.1:5000


### 3. Start the frontend  
Open this file by double-clicking:

my-recruitment-ai/frontend/index.html


The page will open in your browser.

---

## 📌 How to Use

1. Upload one or multiple CV files (PDF or DOCX).  
2. Paste the job description into the text area.  
3. Click **Analyze**.  
4. The results will appear in the table:
   - Candidate name  
   - Skill match percentage  
   - Found skills  
   - Missing skills  
   - Short summary  

---

## ✔ Technologies Used
- HTML / CSS / JavaScript (frontend)
- Python / Flask (backend)
- NLP based on keyword matching
- Skills database in `skills.txt`

---

## 📄 Notes
- Everything works locally (no internet hosting required).
- Frontend can be opened directly (no server needed).
- Backend must be running during use.
