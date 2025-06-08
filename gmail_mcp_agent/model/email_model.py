from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime
import re
from .email import Email
from ..utils.ollama_agent import OllamaAgent

class Email(BaseModel):
    id: str
    subject: str
    sender: str
    snippet: str
    received_at: datetime = datetime.now()
    is_processed: bool = False
    response_template: str = ""
    priority: int = 0
    category: str = "general"
    requires_attention: bool = False
    intent: str = ""
    ai_analysis: Dict[str, Any] = {}

class EmailModel:
    def __init__(self):
        self.emails: List[Email] = []
        self.last_check_time: datetime = datetime.now()
        self.ollama_agent = OllamaAgent(model_name="gemma3:4b")
        self.response_templates = {
            "default": "Thank you for your email. I will get back to you soon.",
            "urgent": "I understand this is urgent. I will prioritize your request and respond as soon as possible.",
            "inquiry": "Thank you for your inquiry. I will look into this matter and provide you with a detailed response.",
            "meeting": "Thank you for the meeting invitation. I will review the details and respond accordingly.",
            "follow_up": "Thank you for your follow-up. I will address this matter promptly."
        }
        
        # Keywords for categorization
        self.category_keywords = {
            "urgent": ["urgent", "asap", "immediately", "important", "priority"],
            "inquiry": ["question", "inquiry", "help", "how to", "what is"],
            "meeting": ["meeting", "schedule", "calendar", "appointment", "call"],
            "follow_up": ["follow up", "follow-up", "reminder", "checking in"]
        }
    
    def add_email(self, email_data: Dict[str, Any]) -> Email:
        """Add a new email to the model."""
        email = Email(**email_data)
        # Only process emails received after the last check
        if email.received_at > self.last_check_time:
            self.emails.append(email)
            self._analyze_email(email)
        return email
    
    def _analyze_email(self, email: Email) -> None:
        """Analyze email content using Ollama."""
        # Get AI analysis
        analysis = self.ollama_agent.analyze_email(email.subject, email.snippet)
        
        # Update email with AI analysis
        email.category = analysis['category']
        email.priority = analysis['priority']
        email.requires_attention = analysis['requires_attention']
        email.intent = analysis['intent']
        email.ai_analysis = analysis
        
        # Generate response using Ollama
        email.response_template = self.ollama_agent.generate_response({
            'category': email.category,
            'priority': email.priority,
            'subject': email.subject,
            'snippet': email.snippet
        })
    
    def get_unprocessed_emails(self) -> List[Email]:
        """Get all unprocessed emails."""
        return [email for email in self.emails if not email.is_processed]
    
    def get_emails_by_priority(self) -> List[Email]:
        """Get unprocessed emails sorted by priority."""
        unprocessed = self.get_unprocessed_emails()
        return sorted(unprocessed, key=lambda x: x.priority, reverse=True)
    
    def mark_as_processed(self, email_id: str) -> None:
        """Mark an email as processed."""
        for email in self.emails:
            if email.id == email_id:
                email.is_processed = True
                break
    
    def get_response_template(self, template_type: str = "default") -> str:
        """Get a response template based on type."""
        return self.response_templates.get(template_type, self.response_templates["default"])
    
    def update_last_check_time(self) -> None:
        """Update the last check time to current time."""
        self.last_check_time = datetime.now()
    
    def get_emails_requiring_attention(self) -> List[Email]:
        """Get emails that require immediate attention."""
        return [email for email in self.emails 
                if email.requires_attention and not email.is_processed] 