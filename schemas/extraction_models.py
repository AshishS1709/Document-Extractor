from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class Source(BaseModel):
    page: int = 1
    bbox: List[float] = Field(default_factory=lambda: [0.0, 0.0, 0.0, 0.0])

class KVField(BaseModel):
    name: str
    value: Optional[str] = None
    confidence: float = 0.0
    source: Source = Field(default_factory=Source)

class QAReport(BaseModel):
    passed_rules: List[str] = Field(default_factory=list)
    failed_rules: List[str] = Field(default_factory=list)
    notes: str = ""

class ExtractionOutput(BaseModel):
    doc_type: str
    fields: List[KVField]
    overall_confidence: float
    qa: QAReport
