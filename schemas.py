from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class A2AMessage(BaseModel):
    role: str
    content: str

class A2ARequest(BaseModel):
    messages: List[A2AMessage]
    context: Optional[Dict[str, Any]] = None

class A2AResponse(BaseModel):
    role: str = "assistant"
    content: str

class FactCheckResult(BaseModel):
    fact: str
    verdict: str  # "True", "False", "Partially True", "Unverifiable"
    explanation: str
    confidence: str  # "high", "medium", "low"
    sources: List[str] 