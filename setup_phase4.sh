#!/bin/bash
# Phase 4 Setup Script - Automated shell integration installation

set -e  # Exit on error

echo "🚀 macOS Dev Launcher - Phase 4 Shell Integration Setup"
echo "========================================================"
echo ""

# Get the script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$HOME/.config/macos-dev-launcher"
SHELL_INTEGRATION="$SCRIPT_DIR/shell_integration.sh"

# Detect shell from SHELL environment variable (more reliable)
CURRENT_SHELL="$SHELL"

if [[ "$CURRENT_SHELL" == *"zsh"* ]]; then
    SHELL_CONFIG="$HOME/.zshrc"
    SHELL_NAME="Zsh"
elif [[ "$CURRENT_SHELL" == *"bash"* ]]; then
    SHELL_CONFIG="$HOME/.bash_profile"
    if [[ ! -f "$SHELL_CONFIG" ]]; then
        SHELL_CONFIG="$HOME/.bashrc"
    fi
    SHELL_NAME="Bash"
else
    echo "❌ Unsupported shell: $CURRENT_SHELL"
    echo "Please manually add to your shell config:"
    echo "   source $SHELL_INTEGRATION"
    exit 1
fi

echo "📝 Detected Shell: $SHELL_NAME"
echo "📝 Shell Config: $SHELL_CONFIG"
echo ""

# Check if shell_integration.sh exists
if [[ ! -f "$SHELL_INTEGRATION" ]]; then
    echo "❌ Error: shell_integration.sh not found at $SHELL_INTEGRATION"
    echo "Make sure you're running this from the repository root"
    exit 1
fi

# Check if already sourced
if grep -q "source.*shell_integration.sh" "$SHELL_CONFIG" 2>/dev/null; then
    echo "✅ Shell integration already configured in $SHELL_CONFIG"
    echo ""
else
    echo "📋 Adding shell integration to $SHELL_CONFIG..."
    echo ""
    
    # Add blank line if file exists and doesn't end with newline
    if [[ -f "$SHELL_CONFIG" ]] && [[ $(tail -c 1 "$SHELL_CONFIG" | wc -l) -eq 0 ]]; then
        echo "" >> "$SHELL_CONFIG"
    fi
    
    # Add the source command
    cat >> "$SHELL_CONFIG" << EOF

# ===== macOS Dev Launcher (Phase 4) =====
source $SHELL_INTEGRATION
# ==========================================
EOF
    
    echo "✅ Added to $SHELL_CONFIG"
    echo ""
fi

# Make shell_integration.sh executable
chmod +x "$SHELL_INTEGRATION"
echo "✅ Made shell_integration.sh executable"
echo ""

# Show next steps
echo "🎉 Setup Complete!"
echo ""
echo "Next steps:"
echo "1. Reload your shell:"
echo "   source $SHELL_CONFIG"
echo ""
echo "2. Test it:"
echo "   dev --help"
echo "   dev --list"
echo "   dev ."
echo ""
echo "3. (Optional) Customize search paths by editing:"
echo "   $SHELL_INTEGRATION"
echo "   Look for PROJECT_SEARCH_PATHS variable"
echo ""
echo "📖 Full documentation:"
echo "   See PHASE4_INSTALL.md for detailed usage"
echo ""