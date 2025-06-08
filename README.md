# Gmail MCP Agent

An MCP (Model-Controller-Presenter) based agent for automating Gmail interactions.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up Google Cloud Project and OAuth 2.0:
   a. Create a Google Cloud Project:
      - Go to [Google Cloud Console](https://console.cloud.google.com/)
      - Click "Create Project" or select an existing project
      - Give your project a name and click "Create"

   b. Enable the Gmail API:
      - In your project, go to "APIs & Services" > "Library"
      - Search for "Gmail API"
      - Click "Enable"

   c. Configure OAuth Consent Screen:
      - Go to "APIs & Services" > "OAuth consent screen"
      - Select "External" user type (unless you have Google Workspace)
      - Fill in the required information:
        * App name: "Gmail MCP Agent"
        * User support email: Your email
        * Developer contact information: Your email
      - Click "Save and Continue"
      - Add the following scopes:
        * `https://www.googleapis.com/auth/gmail.modify`
      - Click "Save and Continue"
      - Add test users (your email address)
      - Click "Save and Continue"

   d. Create OAuth 2.0 Credentials:
      - Go to "APIs & Services" > "Credentials"
      - Click "Create Credentials" > "OAuth client ID"
      - Choose "Desktop application" as the application type
      - Name it "Gmail MCP Agent"
      - Click "Create"
      - Download the credentials (it will be a JSON file)
      - Rename the downloaded file to `credentials.json`
      - Place it in the root directory of the project

3. Create a `.env` file with your configuration:
```
GMAIL_CREDENTIALS_FILE=credentials.json
```

## Project Structure

```
gmail_mcp_agent/
├── model/
│   ├── __init__.py
│   └── email_model.py
├── controller/
│   ├── __init__.py
│   └── email_controller.py
├── presenter/
│   ├── __init__.py
│   └── email_presenter.py
├── utils/
│   ├── __init__.py
│   └── gmail_client.py
└── main.py
```

## Usage

1. First-time setup:
   - Run the agent:
   ```bash
   python main.py
   ```
   - A browser window will open asking you to sign in to your Google account
   - Grant the requested permissions
   - The agent will save the authentication token for future use

2. Subsequent runs:
   - Simply run:
   ```bash
   python main.py
   ```
   - The agent will use the saved token

## Features

- Read and process emails
- Send automated responses
- Manage email labels and organization
- Customizable response templates

## Troubleshooting

1. If you get authentication errors:
   - Delete the `token.json` file
   - Run the agent again to re-authenticate

2. If the browser doesn't open:
   - Make sure you're running the script in an environment with a browser
   - Check if the port 8080 is available

3. If you get "invalid_grant" error:
   - Delete the `token.json` file
   - Run the agent again to re-authenticate

## Security Notes

1. Never commit `credentials.json` or `token.json` to version control
2. Keep your OAuth credentials secure
3. Regularly rotate your credentials if needed
4. Use environment variables for sensitive information

## Authentication Methods

### OAuth2 (Recommended)
- Full access to Gmail API features
- Secure user-specific authentication
- Required for sending emails and accessing user data

### API Key (Limited)
- Limited functionality
- Cannot access user-specific data
- Cannot send emails
- Not recommended for Gmail automation

## Note
The Gmail API requires OAuth2 authentication for most operations. Using an API key alone will result in limited functionality and most operations will fail. It is recommended to use OAuth2 authentication for full functionality. 