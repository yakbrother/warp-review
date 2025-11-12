#!/bin/bash
# Install warp-review CLI

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLI_FILE="$SCRIPT_DIR/warp-review"
INSTALL_DIR="$HOME/.local/bin"

# Create install directory if it doesn't exist
mkdir -p "$INSTALL_DIR"

# Create symlink
ln -sf "$CLI_FILE" "$INSTALL_DIR/warp-review"

echo "✓ Installed warp-review to $INSTALL_DIR/warp-review"

# Check if directory is in PATH
if [[ ":$PATH:" == *":$INSTALL_DIR:"* ]]; then
    echo "✓ $INSTALL_DIR is already in your PATH"
else
    echo ""
    echo "⚠ Add $INSTALL_DIR to your PATH by adding this to your ~/.zshrc:"
    echo ""
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
fi

echo ""
echo "Usage:"
echo "  warp-review run              # Run full review"
echo "  warp-review status           # Check PR status"
echo "  warp-review agent test       # Generate test coverage prompt"
echo "  warp-review view final       # View final checklist"
echo "  warp-review --help           # Show all commands"
