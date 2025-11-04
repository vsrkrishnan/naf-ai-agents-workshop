#!/bin/bash
# Setup git filters to auto-clean Jupyter notebook outputs on commit
#
# This ensures that:
# 1. Notebook outputs are never committed to the repo
# 2. Students always see clean notebooks ready to execute
# 3. Git diffs only show code changes, not output changes

set -e

echo "🔧 Setting up git filters for Jupyter notebooks..."

# Configure the filter to clean outputs when staging files
git config filter.jupyter_clear_output.clean 'jupyter nbconvert --ClearOutputPreprocessor.enabled=True --stdin --stdout --to=notebook'

# Configure the filter to do nothing when checking out files (smudge)
git config filter.jupyter_clear_output.smudge cat

# Verify the configuration
echo ""
echo "✅ Git filter configured successfully!"
echo ""
echo "📋 Configuration:"
git config --get filter.jupyter_clear_output.clean
git config --get filter.jupyter_clear_output.smudge

echo ""
echo "💡 How it works:"
echo "   - When you 'git add' a notebook, outputs are automatically removed"
echo "   - When you 'git commit', only the code is committed (no outputs)"
echo "   - When others 'git clone', they get clean notebooks"
echo ""
echo "🧪 To test it:"
echo "   1. Run a notebook cell and save the file"
echo "   2. Run: git add notebook.ipynb"
echo "   3. Run: git diff --cached notebook.ipynb"
echo "   4. You should see outputs removed in the diff"
echo ""
echo "Done! 🎉"
