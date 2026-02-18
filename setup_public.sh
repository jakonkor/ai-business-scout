#!/bin/bash

echo "================================================"
echo "🚀 AI Business Scout - Public API Setup"
echo "================================================"
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements-public.txt
echo "✅ Dependencies installed"
echo ""

# Check for .env file
if [ -f ".env" ]; then
    echo "✅ .env file found"
else
    echo "📝 Creating .env file from template..."
    cp .env.public.example .env
    echo "⚠️  Please edit .env and add your GITHUB_TOKEN"
    echo ""
    echo "Get a token at: https://github.com/settings/tokens"
    echo "Required scopes: 'public_repo' or 'repo'"
    echo ""
fi

# Test imports
echo "Testing imports..."
python3 -c "
import sys
try:
    import requests
    import bs4
    from openai import OpenAI
    from pydantic import BaseModel
    from dotenv import load_dotenv
    print('✅ All imports successful')
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
"
echo ""

# Check for GitHub token
echo "Checking configuration..."
python3 -c "
import os
from dotenv import load_dotenv

load_dotenv()

github_token = os.getenv('GITHUB_TOKEN')
news_api_key = os.getenv('NEWS_API_KEY')

if github_token and github_token != 'your_github_token_here':
    print('✅ GITHUB_TOKEN configured')
else:
    print('⚠️  GITHUB_TOKEN not configured')
    print('   Get one at: https://github.com/settings/tokens')

if news_api_key and news_api_key != 'your_newsapi_key_here':
    print('✅ NEWS_API_KEY configured (optional)')
else:
    print('ℹ️  NEWS_API_KEY not configured (optional)')
    print('   Get one at: https://newsapi.org/')
"
echo ""

echo "================================================"
echo "Setup Complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your GITHUB_TOKEN"
echo "2. Run: python3 run_public.py"
echo ""
echo "For detailed instructions, see: README-PUBLIC.md"
echo ""
