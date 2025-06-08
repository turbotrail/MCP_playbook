import time
from datetime import datetime
from gmail_mcp_agent.presenter.email_presenter import EmailPresenter

def main():
    presenter = EmailPresenter()
    
    print("Gmail MCP Agent Started")
    print(f"Start Time: {datetime.now().isoformat()}")
    print("Press Ctrl+C to exit")
    
    try:
        while True:
            print("\n" + "="*50)
            print(presenter.display_processing_status())
            
            # Process new emails
            status_messages = presenter.process_new_emails()
            for message in status_messages:
                print(message)
            
            # Display email summary
            print("\n" + presenter.get_email_summary())
            
            # Wait for 1 minute before next check
            print("\nWaiting for 1 minute before next check...")
            time.sleep(60)
            
    except KeyboardInterrupt:
        print("\nShutting down Gmail MCP Agent...")
        print(f"End Time: {datetime.now().isoformat()}")

if __name__ == "__main__":
    main() 