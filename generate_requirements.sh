#!/bin/bash

echo "🔁 Starting dependency regeneration..."
echo "📍 Project Root: $(pwd)"

# Check that pipreqs is installed
if ! command -v pipreqs &> /dev/null
then
    echo "❌ pipreqs is not installed. Please run: pip install pipreqs"
    exit 1
fi

# Check that pip-compile is installed
if ! command -v pip-compile &> /dev/null
then
    echo "❌ pip-tools is not installed. Please run: pip install pip-tools"
    exit 1
fi

# Step 1: Rebuild requirements.in from codebase
echo "📄 Generating requirements.in using pipreqs..."
pipreqs . --force --savepath requirements.in

# Step 2: Compile full pinned requirements.txt from .in file
echo "📌 Compiling requirements.txt using pip-compile..."
pip-compile requirements.in --output-file=requirements.txt

echo "✅ requirements.txt and requirements.in updated successfully!"
