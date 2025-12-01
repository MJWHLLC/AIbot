#!/usr/bin/env bash
# Quick migration script to swap in new GitHub Models integration

set -e

PROJECT_DIR="${1:-.}"
cd "$PROJECT_DIR"

echo "🔄 Paralegal Agent - GitHub Models Integration Migration"
echo "========================================================"
echo ""

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: app.py not found. Are you in the right directory?"
    exit 1
fi

# Backup current files
echo "📦 Backing up current files..."
cp app.py app_backup_$(date +%s).py
cp model_client.py model_client_backup_$(date +%s).py
echo "✅ Backups created"
echo ""

# Verify new files exist
echo "🔍 Checking for new integration files..."
if [ ! -f "app_new.py" ]; then
    echo "❌ app_new.py not found"
    exit 1
fi
if [ ! -f "model_client_real.py" ]; then
    echo "❌ model_client_real.py not found"
    exit 1
fi
if [ ! -f "prompts_full.py" ]; then
    echo "❌ prompts_full.py not found"
    exit 1
fi
echo "✅ All integration files found"
echo ""

# Swap files
echo "🔄 Swapping files..."
cp app_new.py app.py
cp model_client_real.py model_client.py
echo "✅ Files swapped successfully"
echo ""

# Verify imports
echo "🔍 Verifying imports in app.py..."
if grep -q "from .prompts_full import" app.py; then
    echo "✅ Imports verified"
else
    echo "⚠️  Warning: Verify prompts_full import manually"
fi
echo ""

# Summary
echo "✅ Migration Complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Set GITHUB_MODEL_API_TOKEN environment variable:"
echo "   export GITHUB_MODEL_API_TOKEN='ghp_your_token_here'"
echo ""
echo "2. Restart the Flask app:"
echo "   python -m flask --app paralegal_agent.app run"
echo ""
echo "3. Test the integration:"
echo "   - Visit http://localhost:5000"
echo "   - Login (use existing credentials)"
echo "   - Submit a query via /ask"
echo "   - Should work with real GitHub Models API if token is set"
echo ""
echo "4. Run tests to verify:"
echo "   pytest tests/test_app.py -v"
echo ""
echo "📚 Documentation:"
echo "- GITHUB_MODELS_INTEGRATION.md - Full setup guide"
echo "- CHANGES.md - Detailed change summary"
echo "- prompts_full.py - Comprehensive paralegal templates"
echo ""
echo "🔙 To Rollback:"
echo "   ls -la app_backup_*.py model_client_backup_*.py"
echo "   cp app_backup_TIMESTAMP.py app.py"
echo "   cp model_client_backup_TIMESTAMP.py model_client.py"
echo ""
