# Paralegal AI Assistant (Flask)

Minimal scaffold of a Paralegal AI Assistant web app using GitHub-hosted models.

Important security note: Do NOT paste API tokens into source files or chat. Set the model API token as an environment variable `GITHUB_MODEL_API_TOKEN` and the model name in `GITHUB_MODEL_NAME`.

Quick start

1. Create and activate a Python virtual environment (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Set environment variables (example):

```powershell
setx GITHUB_MODEL_API_TOKEN "<your-token>"
setx GITHUB_MODEL_NAME "<owner/model-name>"
```

Then reopen your shell or `Get-ChildItem Env:` to see the variables.

3. Run the app:

```powershell
python -m paralegal_agent.app
```

Open `http://127.0.0.1:5000`.

Features in this scaffold
- Flask web UI with a simple chat form
- Model client wrapper with safe environment-variable based config
- Paralegal persona prompt templates and mandatory disclaimers
- Minimal tests with a mocked model client

Next steps
- Integrate actual GitHub Models API calls in `model_client.py` (do not use tokens in code)
- Add user authentication and secure file handling
- Add attorney review workflow and audit logging

Authentication

This scaffold supports a very small username/password authentication mechanism.
Set the following environment variables to enable login protection:

```powershell
setx AUTH_USERNAME "admin"
setx AUTH_PASSWORD "s3cret"
```

If `AUTH_USERNAME` is not set, the app will run without requiring authentication (convenient for local development and tests).

Do NOT store production passwords in plain environment variables. Use a secrets manager for production deployments.

Password Reset and Invite Flow

- **Invite Links**: Admins can generate invite links for new users (`/admin/invite`). Users click the link and set their password at `/join`.
- **Password Reset**: Users can request a password-reset link at `/reset`. Links expire after 1 hour. Reset at `/reset-password`.
- **Tokens**: One-time-use tokens are stored in SQLite with expiration timestamps.
- **Email Delivery**: Invite and reset links are sent via email (see Email Configuration below).

Email Configuration

This scaffold can send password-reset and invite emails using Flask-Mail. Configure the following environment variables:

```powershell
setx MAIL_SERVER "smtp.gmail.com"
setx MAIL_PORT "587"
setx MAIL_USE_TLS "true"
setx MAIL_USERNAME "your-email@gmail.com"
setx MAIL_PASSWORD "your-app-password"
setx MAIL_DEFAULT_SENDER "noreply@paralegal-agent.local"
```

For local testing without email delivery (e.g., using MailHog or a local fake SMTP server):

```powershell
setx MAIL_SERVER "localhost"
setx MAIL_PORT "1025"
```

If email is not configured, the app will log failures but continue operating.

Disclaimer
This app is a paralegal assistant prototype. It is NOT a substitute for attorney review. All work product must be reviewed by a supervising attorney.
