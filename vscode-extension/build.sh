#!/bin/bash

# Build VSCode Extension
# Usage: ./build.sh

set -e

echo "🔨 Building Shanks Django VSCode Extension..."

# Check if vsce is installed
if ! command -v vsce &> /dev/null; then
    echo "📦 Installing vsce..."
    npm install -g @vscode/vsce
fi

# Convert SVG to PNG if needed
if [ -f "images/icon.svg" ]; then
    echo "🎨 Converting icon..."
    if command -v rsvg-convert &> /dev/null; then
        rsvg-convert -w 128 -h 128 images/icon.svg -o images/icon.png
    elif command -v convert &> /dev/null; then
        convert -background none -resize 128x128 images/icon.svg images/icon.png
    else
        echo "⚠️  Warning: Could not convert SVG to PNG. Install librsvg2-bin or imagemagick."
    fi
fi

# Build VSIX
echo "📦 Packaging extension..."
vsce package

# Get version
VERSION=$(node -p "require('./package.json').version")

echo ""
echo "✅ Build complete!"
echo "📦 File: shanks-django-${VERSION}.vsix"
echo ""
echo "To install:"
echo "  code --install-extension shanks-django-${VERSION}.vsix"
