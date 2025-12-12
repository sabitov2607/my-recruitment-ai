import docx2txt
import PyPDF2

def extract_text_from_file(filepath):
    if filepath.lower().endswith(".pdf"):
        return extract_pdf(filepath)
    elif filepath.lower().endswith(".docx"):
        return docx2txt.process(filepath)
    return ""

def extract_pdf(filepath):
    text = ""
    with open(filepath, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
    return text
