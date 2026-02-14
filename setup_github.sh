#!/bin/bash

# Initialize git repository and push to GitHub

echo "🚀 Setting up Git repository for Monad Agent Dating Economy"
echo "============================================================"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Initialize git if not already initialized
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Add all files
echo "📝 Adding files to git..."
git add .

# Commit
echo "💾 Creating initial commit..."
git commit -m "Initial commit: AI Agent Dating Economy on Monad

- Smart contract with Prisoner's Dilemma escrow system
- Autonomous agents with psychological attachment styles
- Rich agent profiles (goals, skills, ethics)
- Compatibility-based partner matching
- Interactive Streamlit dashboard
- Comprehensive test suite
- Deployment scripts for Monad testnet"

# Add remote (user will need to create the repo on GitHub first)
echo ""
echo "📡 Next steps:"
echo "1. Go to https://github.com/river2spring"
echo "2. Click 'New repository'"
echo "3. Name it: monad-agent-dating"
echo "4. Do NOT initialize with README (we already have one)"
echo "5. Click 'Create repository'"
echo ""
echo "Then run these commands:"
echo "  git remote add origin https://github.com/river2spring/monad-agent-dating.git"
echo "  git branch -M main"
echo "  git push -u origin main"
echo ""
echo "Or if you've already created the repo, just run:"
echo "  git remote add origin https://github.com/river2spring/monad-agent-dating.git"
echo "  git push -u origin main"
