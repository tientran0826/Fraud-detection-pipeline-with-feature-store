#!/bin/bash
# Setup pre-commit hooks for the project

set -e

echo "═══════════════════════════════════════════════════════════════"
echo "🔧 Setting up pre-commit hooks"
echo "═══════════════════════════════════════════════════════════════"

# Check if pre-commit is installed
if ! command -v pre-commit &> /dev/null; then
    echo "📦 Installing pre-commit..."
    pip install pre-commit
else
    echo "✅ pre-commit is already installed"
fi

# Install git hooks
echo ""
echo "🪝 Installing git hooks..."
pre-commit install

# Run on all files initially (optional)
echo ""
echo "🔍 Running pre-commit on all files..."
echo "   (This may take a moment...)"
pre-commit run --all-files

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "✅ Pre-commit setup complete!"
echo ""
echo "📝 Next time you commit, pre-commit will automatically:"
echo "   • Format code with Black"
echo "   • Sort imports with isort"
echo "   • Lint with Ruff"
echo "   • Check types with mypy"
echo "   • Validate YAML files"
echo "   • Check for common issues"
echo ""
echo "💡 Tips:"
echo "   • Run manually: pre-commit run --all-files"
echo "   • Skip hooks: git commit --no-verify"
echo "   • Update hooks: pre-commit autoupdate"
echo "═══════════════════════════════════════════════════════════════"
