from typing import List, Dict, Any
from gmail_mcp_agent.model.email_model import EmailModel, Email
from gmail_mcp_agent.utils.gmail_client import GmailClient
from datetime import datetime

class EmailController:
    def __init__(self):
        self.model = EmailModel()
        self.gmail_client = GmailClient()
        self.start_time = datetime.now()
    
    def fetch_new_emails(self) -> List[Email]:
        """Fetch new unread emails from Gmail."""
        unread_emails = self.gmail_client.get_unread_emails()
        new_emails = []
        
        for email_data in unread_emails:
            # Add received_at timestamp if not present
            if 'received_at' not in email_data:
                email_data['received_at'] = datetime.now()
            
            # Only process emails received after script start
            if email_data['received_at'] > self.start_time:
                email = self.model.add_email(email_data)
                new_emails.append(email)
        
        return new_emails
    
    def process_email(self, email: Email) -> Dict[str, Any]:
        """Process an email and generate a response."""
        # Use the email's category for response template
        response_template = self.model.get_response_template(email.category)
        
        # Extract email address from sender string (e.g., "John Doe <john@example.com>")
        sender_email = email.sender.split('<')[-1].strip('>')
        
        # Customize response based on email category
        if email.category == "urgent":
            response_template = f"URGENT: {response_template}"
        elif email.category == "meeting":
            response_template = f"RE: Meeting: {response_template}"
        
        # Send response
        response = self.gmail_client.send_email(
            to=sender_email,
            subject=f"Re: {email.subject}",
            body=response_template
        )
        
        # Mark email as processed
        self.model.mark_as_processed(email.id)
        
        return {
            'email_id': email.id,
            'response_sent': True,
            'template_used': email.category,
            'priority': email.priority,
            'requires_attention': email.requires_attention
        }
    
    def get_processing_status(self) -> Dict[str, Any]:
        """Get the current processing status."""
        unprocessed = self.model.get_unprocessed_emails()
        attention_required = self.model.get_emails_requiring_attention()
        
        return {
            'total_emails': len(self.model.emails),
            'unprocessed_count': len(unprocessed),
            'processed_count': len(self.model.emails) - len(unprocessed),
            'attention_required': len(attention_required),
            'start_time': self.start_time.isoformat(),
            'last_check_time': self.model.last_check_time.isoformat()
        }
    
    def process_emails_by_priority(self) -> List[Dict[str, Any]]:
        """Process emails in order of priority."""
        results = []
        priority_emails = self.model.get_emails_by_priority()
        
        for email in priority_emails:
            result = self.process_email(email)
            results.append(result)
        
        return results 