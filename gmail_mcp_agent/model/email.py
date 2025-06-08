from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime

class Email(BaseModel):
    id: str
    sender: str
    subject: str
    snippet: str
    received_at: datetime
    is_processed: bool = False
    category: str = "general"
    priority: int = 1
    requires_attention: bool = False
    intent: Optional[str] = None
    ai_analysis: Dict[str, Any] = {} 