# GitHub Models API Integration Guide

## Quick Start

### Option 1: Development (Mock Mode - No Token Required)
```bash
# Start without token - uses built-in mock responses
python -m flask --app paralegal_agent.app run --debug

# Visit http://localhost:5000
# Use demo account or create a user via admin UI
# Submit queries - get mock paralegal responses
```

### Option 2: Production (Real GitHub Models)
```bash
# 1. Get a GitHub token with 'read:models' scope
#    https://github.com/settings/personal-access-tokens/new
#    Scopes: read:models (that's all you need!)

# 2. Set environment variable
export GITHUB_MODEL_API_TOKEN="ghp_..."
export GITHUB_MODEL_NAME="gpt-4o-mini"  # Optional, defaults to gpt-4o-mini

# 3. Start the app
python -m flask --app paralegal_agent.app run

# 4. Visit http://localhost:5000
#    Real queries now call GitHub-hosted gpt-4o-mini model!
```

## What is GitHub Models?

GitHub Models is a service that lets you use cutting-edge AI models (like Claude, GPT-4, etc.) hosted by GitHub/Microsoft. The requests are routed through Azure's inference endpoints.

**Key Benefits**:
- ✅ Free tier available (rate-limited)
- ✅ No vendor lock-in (models from multiple providers)
- ✅ Serverless (no infrastructure to manage)
- ✅ Pay-as-you-go pricing available
- ✅ GitHub token authentication (no separate API account needed)

**Available Models** (examples):
- `gpt-4o-mini` - Fast, cheaper version of GPT-4 Omni (default for this app)
- `gpt-4o` - Full GPT-4 Omni
- `meta-llama-3-1-70b-instruct` - Open source Llama
- `claude-3-5-sonnet` - Anthropic's Claude
- And more...

See https://github.com/marketplace/models for the full list.

## Architecture

```
Your Query
    ↓
[Paralegal UI] (/ask route)
    ↓
[Prompt Builder] (prompts_full.py)
  - Constructs system prompt (paralegal role, boundaries)
  - Adds document template (complaint, motion, discovery, etc.)
  - Includes jurisdiction rules (Federal, State-specific)
  - Embeds checklist for that document type
    ↓
[Model Client] (model_client.py)
    ↓
    IF GITHUB_MODEL_API_TOKEN is set:
        → POST to https://models.inference.ai.azure.com/chat/completions
        → Bearer token: GITHUB_MODEL_API_TOKEN
        → Model: gpt-4o-mini (or your configured model)
        → Returns: Real LLM response
    ELSE:
        → Mock response (built-in, no API call)
    ↓
[Response] + Mandatory Disclaimer
    ↓
User sees: "⚠️ This response requires attorney review"
```

## Configuration

### Environment Variables

#### Required for Real API
```bash
GITHUB_MODEL_API_TOKEN="ghp_..."  # GitHub token with read:models scope
```

#### Optional (Defaults Provided)
```bash
GITHUB_MODEL_NAME="gpt-4o-mini"   # Can be any GitHub Models available model
FLASK_SECRET_KEY="your-secret"     # Flask session key
```

#### Optional (Email Delivery)
```bash
MAIL_SERVER="smtp.gmail.com"
MAIL_PORT="587"
MAIL_USE_TLS="true"
MAIL_USERNAME="your-email@gmail.com"
MAIL_PASSWORD="your-app-password"
MAIL_DEFAULT_SENDER="noreply@yourorg.com"
```

### Where to Set Variables

**Linux/Mac**:
```bash
# In shell profile (~/.bashrc, ~/.zshrc)
export GITHUB_MODEL_API_TOKEN="ghp_..."

# Or in .env file (auto-loaded by app)
echo 'GITHUB_MODEL_API_TOKEN=ghp_...' > .env
```

**Windows PowerShell**:
```powershell
$env:GITHUB_MODEL_API_TOKEN = "ghp_..."

# Or in .env file (app auto-loads from it)
```

**Docker**:
```dockerfile
# In docker-compose.yml
environment:
  - GITHUB_MODEL_API_TOKEN=ghp_...
  - GITHUB_MODEL_NAME=gpt-4o-mini
```

## Getting a GitHub Token

1. Go to https://github.com/settings/personal-access-tokens/new
2. Token name: "Paralegal Agent - GitHub Models"
3. Expiration: 90 days (or your preference)
4. Permissions: Check ☑️ `read:models` (that's ALL you need)
5. Click "Generate token"
6. Copy the token and save it:
   ```bash
   export GITHUB_MODEL_API_TOKEN="ghp_..."
   ```

**Security Note**: Never commit tokens to git. Use `.env` file or environment variables only.

## Paralegal Prompt System

The app uses a sophisticated prompt system that builds paralegal-specific guidance:

### Document Types Supported
- **Complaint** - Federal civil complaint with 23-item checklist
- **Motion** - Motion for Summary Judgment with formatting rules
- **Discovery** - Discovery requests with FRCP 6 rules
- **Affidavit** - Affidavit template with notarization rules
- **Subpoena** - Subpoena with service rules

### What Each Response Includes

1. **System Role** (from SYSTEM_PROMPT):
   ```
   You are a paralegal assistant working under attorney supervision.
   This is NOT legal advice and requires attorney review.
   [Full role definition, competencies, boundaries]
   ```

2. **Document Template** (from DOCUMENT_TEMPLATES):
   ```
   Complaint (Federal):
   ✓ Caption with proper formatting
   ✓ Numbered paragraphs
   ✓ Jurisdiction statement
   ✓ 23-item checklist (allegations, claims, prayer for relief)
   ✓ FRCP 8, 10, 11 compliance rules
   ```

3. **Jurisdiction Rules**:
   ```
   Federal Rules of Civil Procedure (FRCP) 6:
   - 30-day response deadline
   - Rule 6(a) timing exceptions
   - Holiday/weekend handling
   ```

4. **Checklists** (Federal Filing Procedure, Discovery Management):
   ```
   21 steps for CM/ECF filing
   35+ discovery management items
   ```

5. **Mandatory Disclaimer** (every response):
   ```
   ⚠️ DISCLAIMER: This response requires attorney review.
   I am a paralegal AI assistant, not a lawyer.
   ```

## Example Queries

### Query 1: Draft a Complaint
```
Document Type: Complaint (Federal)
Jurisdiction: Federal
Query: "Draft a complaint for breach of contract. 
       Plaintiff is ABC Corp, Defendant is XYZ Ltd.
       Contract value: $500,000. 
       Breach occurred Jan 1, 2024."

Response: Full complaint template with:
- Proper caption
- Numbered allegations
- Legal theories
- Prayer for relief
- 23-item compliance checklist
```

### Query 2: Discovery Help
```
Document Type: Discovery Request
Jurisdiction: Federal
Query: "Generate interrogatories for a contract dispute.
       Focus on communication between parties
       and contract interpretation."

Response: 10-15 interrogatories with:
- Proper FRCP 33 format
- Scope and definitions section
- Instructions to responding party
- Privilege log considerations
```

### Query 3: Deadline Calculation
```
Document Type: General Legal Research
Jurisdiction: Federal
Query: "A complaint was served on me Jan 15.
       What's my response deadline under FRCP 12?"

Response: Full FRCP 6 analysis with:
- Applicable rule citations
- Exact deadline calculation
- Holiday exceptions
- Extension procedures
- Service method considerations
```

## Testing the Integration

### Test 1: Verify Mock Mode Works
```bash
# Clear token (if set)
unset GITHUB_MODEL_API_TOKEN

# Start app
python -m flask --app paralegal_agent.app run --debug

# Visit http://localhost:5000
# Login with demo account
# Submit /ask query
# Should get mock response (works without token!)
```

### Test 2: Verify Real API Works
```bash
# Set token
export GITHUB_MODEL_API_TOKEN="ghp_your_real_token"

# Check it's set
echo $GITHUB_MODEL_API_TOKEN  # Should show ghp_...

# Start app
python -m flask --app paralegal_agent.app run --debug

# Check app startup logs (should not say "GITHUB_MODEL_API_TOKEN not set")

# Submit /ask query
# Should call real GitHub Models API
# Response should be from actual gpt-4o-mini model
# Look for real content (not mock template)
```

### Test 3: Run Full Test Suite
```bash
cd paralegal_agent
pytest tests/test_app.py -v

# Should see:
# test_index.py PASSED
# test_ask_mock.py PASSED
# test_invite_flow.py PASSED
# test_password_reset_flow.py PASSED
```

## Performance

| Operation | Time | Notes |
|-----------|------|-------|
| Mock response | ~50ms | No API call |
| Real API (gpt-4o-mini) | 2-5s | Network latency + model inference |
| Page load | <100ms | Flask render |

**Tip**: gpt-4o-mini is fast and cheap compared to full gpt-4o. Perfect for paralegal tasks.

## Pricing (Informational)

GitHub Models pricing varies by model. As of this writing:
- **Free tier**: Limited requests, rate-limited
- **Paid tier**: ~$0.50-$3.00 per 1M tokens depending on model
- **gpt-4o-mini**: Lower cost, faster, ideal for paralegal tasks

Visit https://github.com/marketplace/models for current pricing.

## Troubleshooting

### Issue: Getting mock responses when I set token

**Diagnosis**:
```bash
echo $GITHUB_MODEL_API_TOKEN  # Check if set
```

**Solution**:
1. Token may not be in PATH. Set it in code:
   ```python
   os.environ['GITHUB_MODEL_API_TOKEN'] = 'ghp_...'
   ```
2. Restart Flask app after setting token
3. Check app logs for:
   ```
   Calling GitHub Models API endpoint: https://models.inference.ai.azure.com/chat/completions
   Using model: gpt-4o-mini
   ```

### Issue: 401 Unauthorized from Azure

**Diagnosis**: Token is invalid or expired.

**Solution**:
1. Generate a new token: https://github.com/settings/personal-access-tokens/new
2. Ensure it has `read:models` scope
3. Token hasn't expired
4. Set new token and restart app

### Issue: 429 Rate Limited

**Diagnosis**: Exceeded GitHub Models rate limits.

**Solution**:
1. On free tier: Wait or upgrade to paid tier
2. On paid tier: Contact GitHub support
3. Batch requests if possible
4. Use mock mode for development/testing

### Issue: Model not found

**Diagnosis**: GITHUB_MODEL_NAME value doesn't exist.

**Solution**:
```bash
# Check available models
# Visit https://github.com/marketplace/models

# Common models:
export GITHUB_MODEL_NAME="gpt-4o-mini"  # Fast, cheap (default)
export GITHUB_MODEL_NAME="gpt-4o"       # More capable
export GITHUB_MODEL_NAME="claude-3-5-sonnet"  # Anthropic Claude
```

## Security Best Practices

✅ **DO**:
- Store token in environment variables
- Use `.env` file with `.gitignore` entry
- Rotate tokens regularly (90 day expiry recommended)
- Use minimal scope (`read:models` only)
- Log API calls for auditing

❌ **DON'T**:
- Commit tokens to git
- Hardcode tokens in code
- Share tokens across projects
- Use tokens with more permissions than needed
- Log full responses containing sensitive info

## Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_APP=paralegal_agent.app
CMD ["flask", "run", "--host=0.0.0.0"]
```

```yaml
# docker-compose.yml
version: '3.8'
services:
  paralegal-agent:
    build: .
    ports:
      - "5000:5000"
    environment:
      - GITHUB_MODEL_API_TOKEN=ghp_your_token
      - GITHUB_MODEL_NAME=gpt-4o-mini
      - FLASK_SECRET_KEY=your-random-secret
    volumes:
      - ./paralegal_agent/users.db:/app/paralegal_agent/users.db
```

```bash
# Deploy
docker-compose up --build

# Visit http://localhost:5000
```

## Next Steps

1. ✅ Set `GITHUB_MODEL_API_TOKEN` environment variable
2. ✅ Restart Flask app
3. ✅ Test /ask route with real API
4. ✅ Configure other settings (email, auth, etc.)
5. ✅ Run pytest suite
6. ✅ Deploy to production
7. ✅ Monitor logs for errors

## References

- **GitHub Models Marketplace**: https://github.com/marketplace/models
- **GitHub Models Documentation**: https://docs.github.com/en/github-models
- **Azure Inference API**: https://models.inference.ai.azure.com
- **FRCP Rules**: Federal Rules of Civil Procedure (updated 2023)
- **Paralegal Ethics**: NFPA Model Code of Ethics

## Support

For issues or questions:
1. Check `CHANGES.md` for what changed
2. Review `GITHUB_MODELS_INTEGRATION.md` for detailed setup
3. Check app logs: `app.run(debug=True)` shows verbose output
4. Review `prompts_full.py` for paralegal template details
5. Run `pytest tests/test_app.py -v` to verify functionality

---

**Status**: ✅ GitHub Models API integration ready for production use.
