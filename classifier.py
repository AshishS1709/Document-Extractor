from utils.groq_client import get_groq_client
from utils.parsing import parse_json_safely

def classify_doc_type(raw_text: str, model="llama3-70b-8192", temperature=0.0):
    client = get_groq_client()
    system = (
        "You are a precise document classifier. Only output JSON. "
        "Choose doc_type from: ['invoice','medical_bill','prescription']. "
        "Include confidence (0-1) and rationale."
    )
    user = f"Classify this document. Return JSON with keys: doc_type, confidence, rationale.\n\nTEXT:\n{raw_text[:4000]}"

    msg = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
    )
    return parse_json_safely(msg.choices[0].message.content)
