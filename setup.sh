#!/bin/bash

# AI Business Scout - Setup and Demo Script

echo "🚀 AI Business Scout - Setup"
echo "================================"

# Check Python version
echo ""
echo "Checking Python version..."
python3 --version

# Install core dependencies only for demo
echo ""
echo "Installing core dependencies..."
pip3 install --user pydantic python-dotenv pyyaml rich 2>&1 | grep -v "Requirement already satisfied" || true

echo ""
echo "✅ Setup complete!"
echo ""
echo "📚 Quick Start:"
echo "  1. Copy .env.example to .env"
echo "  2. Add at least one AI API key (OpenAI or Anthropic)"
echo "  3. Run: python3 -m src.main"
echo ""
echo "🧪 Test individual agents:"
echo "  python3 -m src.agents.web_scanner"
echo "  python3 -m src.agents.idea_generator"
echo "  python3 -m src.agents.analyst"
echo "  python3 -m src.agents.validator"
echo ""
echo "📖 See QUICKSTART.md for full documentation"
echo ""
