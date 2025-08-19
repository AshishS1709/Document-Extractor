import pdfplumber
from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL
from prompts import DOC_CLASSIFIER_PROMPT, EXTRACTION_PROMPT

client = Groq(api_key=GROQ_API_KEY)

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def classify_doc(text: str) -> str:
    resp = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": DOC_CLASSIFIER_PROMPT},
            {"role": "user", "content": text[:2000]}
        ]
    )
    return resp.choices[0].message.content.strip().lower()

def extract_fields(text: str, doc_type: str, fields: list = None):
    field_list = ", ".join(fields) if fields else "auto-detect relevant fields"
    prompt = EXTRACTION_PROMPT + f"\nDocument type: {doc_type}\nFields: {field_list}\nText:\n{text[:3000]}"

    resp = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return resp.choices[0].message.content
