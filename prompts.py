DOC_CLASSIFIER_PROMPT = """
You are a document classifier. Based on the text below, decide the document type:
- invoice
- medical_bill
- prescription
- other

Return only one word.
"""

EXTRACTION_PROMPT = """
You are an information extractor.
Given the document text and expected fields, return JSON in the following schema:

{
  "doc_type": "<invoice|medical_bill|prescription>",
  "fields": [
    {"name": "FieldName", "value": "ExtractedValue", "confidence": 0.0}
  ],
  "overall_confidence": 0.0
}

Rules:
- Estimate confidence between 0 and 1.
- Return only valid JSON.
"""