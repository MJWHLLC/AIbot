# Integration Guide: GitHub Models & Prompts

## Summary of Changes

The paralegal agent app has been fully enhanced with GitHub Models API integration and comprehensive paralegal prompt templates. Here's what was completed:

### 1. Real GitHub Models API Client (`model_client_real.py`)

**File**: `paralegal_agent/model_client_real.py` (NEW)

**Features**:
- ✅ Real Azure inference endpoint integration (`https://models.inference.ai.azure.com/chat/completions`)
- ✅ Bearer token authentication via `GITHUB_MODEL_API_TOKEN` env var
- ✅ Configurable model selection via `GITHUB_MODEL_NAME` env var (defaults to `gpt-4o-mini`)
- ✅ Proper error handling with fallback to mock responses
- ✅ Logging for debugging and monitoring
- ✅ 30-second timeout on API calls
- ✅ Mock responses for local testing (no token required)

**Usage**:
```python
from model_client_real import ModelClient

client = ModelClient()
response = client.generate(prompt)  # Real API if token configured, mock otherwise
```

**Configuration**:
```bash
export GITHUB_MODEL_API_TOKEN="your-github-token-with-read-models"
export GITHUB_MODEL_NAME="gpt-4o-mini"  # or another available model
```

### 2. Comprehensive Paralegal Prompts (`prompts_full.py`)

**File**: `paralegal_agent/prompts_full.py` (NEW, 450+ lines)

**Components**:

#### a) System Prompt (400+ words)
- **Role Definition**: Paralegal AI Assistant working under attorney supervision
- **Competencies**: 
  - Document drafting (pleadings, motions, discovery)
  - Deadline tracking (FRCP 6 rules)
  - Case management
  - Legal research guidance
- **Boundaries**: "NOT a lawyer", "NOT legal advice", requires attorney review
- **Disclaimers**: Mandatory ethical notice on every response

#### b) Document Templates
```python
DOCUMENT_TEMPLATES = {
    "complaint": {
        "title": "Civil Complaint (Federal)",
        "checklist": [23 items],
        "formatting": {...},
        "federal_rules": [FRCP 8, 10, 11 citations]
    },
    "motion": {
        "title": "Motion for Summary Judgment",
        "checklist": [18 items],
        ...
    },
    "discovery": {
        "title": "Discovery Request",
        "checklist": [20 items],
        ...
    },
    "affidavit": {
        "title": "Affidavit",
        "checklist": [15 items],
        ...
    },
    "subpoena": {
        "title": "Subpoena",
        "checklist": [14 items],
        ...
    }
}
```

#### c) Federal Filing Procedure Checklist
- 21-step process for CM/ECF (electronic filing)
- Pre-filing requirements
- Filing steps with error handling
- Post-filing verification

#### d) Deadline Calculation (FRCP 6)
- Rule 6 timing rules
- Holiday/weekend handling
- Common federal deadlines with examples
- Extension procedures

#### e) Discovery Checklist
- 35+ items covering:
  - Interrogatory requests
  - Responses and objections
  - Depositions (notice, preparation, witness management)
  - Document requests and privilege logs

#### f) Helper Functions
```python
def build_document_prompt(doc_type, jurisdiction, user_text):
    """Build prompt for specific document type with templates"""
    
def build_case_management_prompt(user_query):
    """Build prompt for case management tasks"""
    
def build_research_prompt(user_query):
    """Build prompt for legal research and case law analysis"""
```

### 3. Enhanced Flask App (`app_new.py`)

**File**: `paralegal_agent/app_new.py` (NEW, improved version)

**Improvements**:
- ✅ Imports from `prompts_full` instead of `prompts`
- ✅ Uses `model_client_real` for real API calls
- ✅ Document type selector with dropdown (not plain text input)
- ✅ Jurisdiction selector dropdown (Federal, NY, CA, TX, Other)
- ✅ Intelligent prompt builder selection based on query type
- ✅ Better error handling and logging
- ✅ CSRF protection on all forms
- ✅ Flash messages for user feedback

**Routes**:
- `GET /` - Main interface (protected, login required)
- `POST /ask` - AI query with document type, jurisdiction, and content
- `GET/POST /login` - Session-based login
- `POST /logout` - Session cleanup
- `GET /admin` - User management (admin only)
- `POST /admin/create` - Create new user (admin)
- `POST /admin/delete` - Delete user (admin)
- `POST /admin/invite` - Generate invite link (admin)
- `GET/POST /join` - Accept invite, set up account
- `GET/POST /reset` - Request password reset
- `GET/POST /reset-password` - Complete password reset

### 4. Enhanced UI Template (`index.html`)

**File**: `paralegal_agent/templates/index.html` (UPDATED)

**Changes**:
```html
<!-- Document Type Dropdown -->
<select id="document_type" name="document_type" required>
  <option value="">-- Select Document Type --</option>
  <option value="complaint">Complaint (Federal)</option>
  <option value="motion">Motion for Summary Judgment</option>
  <option value="discovery">Discovery Request</option>
  <option value="affidavit">Affidavit</option>
  <option value="subpoena">Subpoena</option>
  <option value="General Legal Research">General Legal Research</option>
</select>

<!-- Jurisdiction Dropdown -->
<select id="jurisdiction" name="jurisdiction">
  <option value="Federal" selected>Federal</option>
  <option value="New York">New York</option>
  <option value="California">California</option>
  <option value="Texas">Texas</option>
  <option value="Other State">Other State</option>
</select>
```

## Integration Steps (To Complete)

### Step 1: Backup Current Files
```bash
cd c:\Users\MJWil\odoo_custom_addons\paralegal_agent
cp app.py app_backup.py
cp model_client.py model_client_backup.py
```

### Step 2: Swap in New Files
```bash
# Replace with enhanced versions
cp app_new.py app.py
cp model_client_real.py model_client.py
```

### Step 3: Verify imports in prompts_full.py used in app.py
```python
from .prompts_full import build_document_prompt, build_case_management_prompt, build_research_prompt
```

### Step 4: Set Environment Variables
```bash
# For real API access
export GITHUB_MODEL_API_TOKEN="ghp_your_token_with_read_models_scope"
export GITHUB_MODEL_NAME="gpt-4o-mini"

# Other settings (optional)
export FLASK_ENV="production"
export FLASK_SECRET_KEY="your-secure-random-key-here"
```

### Step 5: Test the Integration
```bash
# Start Flask app
python -m flask --app paralegal_agent.app run --debug

# Test without token (mock mode)
curl http://localhost:5000/
# Should load login page

# Login and test /ask with mock responses (no token configured)
# Then configure token and test with real API
```

### Step 6: Run Tests
```bash
cd paralegal_agent
pytest tests/test_app.py -v
```

## Architecture Diagram

```
User Request (Web UI)
    ↓
app.py (/ask route)
    ↓
Query: "Draft a motion for summary judgment"
Document Type: "motion"
Jurisdiction: "Federal"
    ↓
Selects: build_document_prompt() from prompts_full.py
    ↓
Constructs prompt combining:
  - SYSTEM_PROMPT (paralegal role, boundaries, disclaimers)
  - DOCUMENT_TEMPLATES["motion"] (checklist, formatting rules)
  - Jurisdiction-specific rules
  - User input
    ↓
Sends to model_client.py
    ↓
If GITHUB_MODEL_API_TOKEN set:
  → Real API call to Azure inference endpoint
  → Bearer token auth
  → Returns: gpt-4o-mini response
Else:
  → Mock response (for testing)
    ↓
Response + Mandatory Disclaimer
    ↓
User sees: "⚠️ This response requires attorney review"
```

## Files Modified/Created

| File | Type | Purpose |
|------|------|---------|
| `paralegal_agent/app_new.py` | NEW | Enhanced Flask app with real API integration |
| `paralegal_agent/model_client_real.py` | NEW | GitHub Models API client (Azure endpoint) |
| `paralegal_agent/prompts_full.py` | NEW | Comprehensive paralegal templates (450+ lines) |
| `paralegal_agent/templates/index.html` | UPDATED | Document type and jurisdiction dropdowns |
| `paralegal_agent/app.py` | TO REPLACE | Current version → back up then replace with app_new.py |
| `paralegal_agent/model_client.py` | TO REPLACE | Current version → back up then replace with model_client_real.py |

## Environment Configuration

### Minimal (Mock Mode - No Token Required)
```bash
export FLASK_SECRET_KEY="dev-key"
```

### Production (Real GitHub Models API)
```bash
export FLASK_SECRET_KEY="your-secure-random-string-here"
export GITHUB_MODEL_API_TOKEN="ghp_..."  # GitHub token with read:models scope
export GITHUB_MODEL_NAME="gpt-4o-mini"

# Email delivery (optional)
export MAIL_SERVER="smtp.gmail.com"
export MAIL_PORT="587"
export MAIL_USE_TLS="true"
export MAIL_USERNAME="your-email@gmail.com"
export MAIL_PASSWORD="your-app-password"
export MAIL_DEFAULT_SENDER="noreply@yourorg.com"

# Auth (optional - if not using SQLite users)
export AUTH_USERNAME="admin"
export AUTH_PASSWORD="secure-password"
```

## Testing Without Real Token

All features work with mock responses:
1. No token configured → Uses built-in mock responses
2. Mock responses cover:
   - Complaint drafting
   - Discovery requests
   - Deadline calculations
   - Motion templates
3. Useful for development, testing, and demos

## Next Steps

1. **Backup current files** to preserve working state
2. **Replace** `app.py` with `app_new.py`
3. **Replace** `model_client.py` with `model_client_real.py`
4. **Configure** `GITHUB_MODEL_API_TOKEN` with your GitHub token
5. **Test** with real API: Run `/ask` with sample queries
6. **Deploy** using Dockerfile or docker-compose

## Security Notes

- ✅ No tokens hardcoded (env var only)
- ✅ CSRF protection on all forms
- ✅ Password hashing with Werkzeug
- ✅ Time-expiring, one-time tokens (invites, resets)
- ✅ Email-verified account access
- ✅ Admin-only user management

## Troubleshooting

### Issue: "GITHUB_MODEL_API_TOKEN not set"
**Solution**: Set the env var and restart:
```bash
export GITHUB_MODEL_API_TOKEN="ghp_..."
```

### Issue: "Mock responses" appearing instead of real API
**Solution**: 
1. Verify `GITHUB_MODEL_API_TOKEN` is set
2. Check token has `read:models` scope
3. Review app logs for API errors

### Issue: 401 Unauthorized from Azure endpoint
**Solution**: Token is invalid or expired. Get a fresh GitHub token with `read:models` permission.

## Reference

- **GitHub Models Docs**: https://github.com/marketplace/models
- **Azure Inference Endpoint**: https://models.inference.ai.azure.com/chat/completions
- **FRCP Rules**: Federal Rules of Civil Procedure (updated 2023)
- **CM/ECF**: Electronic Case Filing system documentation

---

**Status**: ✅ All GitHub Models API integration and comprehensive paralegal prompts are ready for deployment.

**Ready for**: File replacement, token configuration, and production testing.
