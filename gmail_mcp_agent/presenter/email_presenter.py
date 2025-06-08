from typing import List, Dict, Any
from gmail_mcp_agent.model.email_model import Email
from gmail_mcp_agent.controller.email_controller import EmailController

class EmailPresenter:
    def __init__(self):
        self.controller = EmailController()
    
    def display_email(self, email: Email) -> str:
        """Format email for display."""
        priority_stars = "⭐" * email.priority
        attention_mark = "🔔" if email.requires_attention else ""
        
        return f"""
        From: {email.sender}
        Subject: {email.subject}
        Category: {email.category.upper()} {priority_stars} {attention_mark}
        Intent: {email.intent}
        Snippet: {email.snippet}
        Received: {email.received_at}
        Status: {'Processed' if email.is_processed else 'Unprocessed'}
        AI Analysis: {email.ai_analysis.get('suggested_response', 'No AI analysis available')}
        """
    
    def display_processing_status(self) -> str:
        """Format processing status for display."""
        status = self.controller.get_processing_status()
        return f"""
        Email Processing Status:
        - Total Emails: {status['total_emails']}
        - Unprocessed: {status['unprocessed_count']}
        - Processed: {status['processed_count']}
        - Requiring Attention: {status['attention_required']}
        - Start Time: {status['start_time']}
        - Last Check: {status['last_check_time']}
        """
    
    def process_new_emails(self) -> List[str]:
        """Process new emails and return status messages."""
        new_emails = self.controller.fetch_new_emails()
        status_messages = []
        
        if not new_emails:
            status_messages.append("No new emails to process.")
            return status_messages
        
        # Process emails by priority
        results = self.controller.process_emails_by_priority()
        
        for result in results:
            status_messages.append(
                f"Processed email (Priority: {result['priority']}, "
                f"Category: {result['template_used']}, "
                f"Intent: {result.get('intent', 'Unknown')}, "
                f"Attention: {'Required' if result['requires_attention'] else 'Not Required'})"
            )
        
        return status_messages
    
    def get_email_summary(self) -> str:
        """Get a summary of all emails."""
        unprocessed = self.controller.model.get_unprocessed_emails()
        if not unprocessed:
            return "No unprocessed emails."
            
        summary = ["Email Summary:"]
        
        # Group emails by category
        categories = {}
        for email in unprocessed:
            if email.category not in categories:
                categories[email.category] = []
            categories[email.category].append(email)
        
        # Display emails by category
        for category, emails in categories.items():
            summary.append(f"\n{category.upper()} Emails:")
            for email in sorted(emails, key=lambda x: x.priority, reverse=True):
                summary.append(self.display_email(email))
        
        return "\n".join(summary) 