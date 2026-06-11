#!/bin/bash
set -e

# Ensure we are in the right directory
cd /Users/jangjaeha/.gemini/antigravity/scratch/skill_converter

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run PyInstaller
# --windowed: Creates a Mac .app bundle without a console window
# --name: Specifies the name of the app
# --noconfirm: Overwrite output directory without asking
pyinstaller --windowed --name "SkillConverter" --noconfirm app.py

echo "Build complete! You can find SkillConverter.app in the dist/ folder."
